#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-28
# =============================================================================
"""
Extract scaling statistics from Xia2 log fille.
Deal with both DIALS log file format long and short output
"""
import os
import sys
import re
import logging
from extract.extract_log.XRAY.scaling import LogScaling  # initiate data dictionary for scaling process

# all versions are imported and handled internally using the versioned python file in this folder

logger = logging.getLogger(__name__)


class LogXia2(LogScaling):  # parent class in parent folder's __init__.py
    """class for parsing Scalepack log file
    """

    def __init__(self):
        """
        Initiate class variable of data dictionary.

        Returns
        -------
        None.

        """
        self.d_ = {}
        # Use the parent class LogScaling to add mmCIF items for scaling
        LogScaling.__init__(self)

    def getStartingIndex(self, pattern, n_occur=1):
        """
        Find the starting index of the self.l_file for a particular section
        Scalepack log file organizes in sections, so need to find section start

        Parameters
        ----------
        pattern : str
            text pattern of the section start
        n_occur : int, optional
            take the 1st/2nd/3rd appearance of the pattern. The default is 1.

        Returns
        -------
        int
            starting line number (index) of the pattern.

        """
        re_pattern = re.compile(pattern)
        i_occur = 0
        for i in range(self.n_lines):
            line = self.l_file[i]
            if re_pattern.search(line):
                i_occur += 1
                if i_occur == n_occur:
                    return i
        else:
            return -1

    def parse(self, filepath):
        """
        parse Aimless log file

        Returns
        -------
        None.

        Outcomes
        -------
        self.d_["reflns"] to record reflection statistics
        self.d_["reflns_shell"] to record reflection shell statistics

        """
        try:
            with open(filepath) as file:
                self.l_file = file.read().splitlines() #read file into a list
        except IOError as e:
            logger.exception(e)
            return False
        
        try:
            self.n_lines = len(self.l_file)  # number of lines
            self.parseSummary()  # process summary section
    
            # add static ordinal record for reflns
            self.d_["reflns"]["_reflns.entry_id"].append("UNNAMED")
            self.d_["reflns"]["_reflns.pdbx_diffrn_id"].append("1")
            self.d_["reflns"]["_reflns.pdbx_ordinal"].append("1")
    
            # add static ordinal record for _reflns_shell
            n_shell = len(self.d_["reflns_shell"]["_reflns_shell.Rmerge_I_obs"])
            for i in range(n_shell):
                self.d_["reflns_shell"]["_reflns_shell.pdbx_diffrn_id"].append("1")
                self.d_["reflns_shell"]["_reflns_shell.pdbx_ordinal"].append(str(i+1))
        except Exception as e:
            logger.exception(e)
            return False

        self.verifyData()  # do before adding static value to remove empty row
        
        if self.d_:
            logger.info("data parsed successfully from log file %s" % filepath)
            return True
        else:
            logger.warning("no data parsed from log file %s" % filepath)
            return False
    
    def parseSummary(self):
        """
        Parse summary.

        Returns
        -------
        None.

        """
        pattern = r'^\s*High resolution limit\s+(\d+\.?\d+)\s+(\d+.?\d+)\s+(\d+.?\d+)\s*$'
        i_start = self.getStartingIndex(pattern)
        i_end = i_start + 21 # truncate the summary section
        l_summary_section = self.l_file[i_start:i_end]
        # print(l_summary_section)
        d_re = {}
        d_re["High resolution limit"] = ("_reflns.d_resolution_high", '_reflns_shell.d_res_high')
        d_re["Low resolution limit"] = ("_reflns.d_resolution_low", '_reflns_shell.d_res_low')
        d_re["Completeness"] = ("_reflns.percent_possible_obs", '_reflns_shell.percent_possible_obs')
        d_re["Multiplicity"] = ("_reflns.pdbx_redundancy", '_reflns_shell.pdbx_redundancy')
        d_re["I/sigma"] = ("_reflns.pdbx_netI_over_sigmaI", '_reflns_shell.pdbx_netI_over_sigmaI_obs')
        d_re["Rmerge\(I\)"] = ("_reflns.pdbx_Rmerge_I_obs", '_reflns_shell.Rmerge_I_obs')
        d_re["Rmeas\(I\)"] = ("_reflns.pdbx_Rrim_I_all", '_reflns_shell.pdbx_Rrim_I_all')
        d_re["Rpim\(I\)"] = ("_reflns.pdbx_Rpim_I_all", '_reflns_shell.pdbx_Rpim_I_all')
        d_re["CC half"] = ("_reflns.pdbx_CC_half", '_reflns_shell.pdbx_CC_half')
        d_re["Total observations"] = ("_reflns.pdbx_number_measured_all", '_reflns_shell.number_measured_all')
        d_re["Total unique"] = ("_reflns.number_obs", '_reflns_shell.number_unique_obs')

        for each in d_re:
            re_ = re.compile(r"^\s*%s\s+(\d+\.?\d+)\s+(\d+.?\d+)\s+(\d+.?\d+)\s*$" % each)
            for line in l_summary_section:
                if re_.search(line):
                    try:
                        self.d_["reflns"][d_re[each][0]].append(re_.search(line).groups()[0])
                        self.d_["reflns_shell"][d_re[each][1]].append(re_.search(line).groups()[2])
                        break
                    except IndexError as msg:
                        logger.warning(msg)

    def verifyData(self):
        """
        Verify number of values for each row and remove empty row

        Returns
        -------
        None.

        """
        d_clean = {}
        for cat in self.d_:
            if self.verifySameNumValuesPerRow(self.d_[cat]):
                d_clean[cat] = {}
                for item in self.d_[cat]:
                    if len(self.d_[cat][item]) != 0:  # only if row is not emtpy
                        d_clean[cat][item] = self.d_[cat][item]
        self.d_ = d_clean

    def verifySameNumValuesPerRow(self, d_cat):
        """
        Verify each row has same num of values

        Parameters
        ----------
        d_cat : dict
            dict for each mmCIF data category.

        Returns
        -------
        bool
            True if each row is either empty of having same num of values.

        """
        num_values = 0
        for item in d_cat:
            if len(d_cat[item]) > 0:
                if num_values == 0:  # for first non-empty row
                    num_values = len(d_cat[item])  # assign number of values
                else:
                    if len(d_cat[item]) != num_values:  # for either other rows
                        return False  # if any other rows differ from the 1st
        if num_values == 0:  # if entire cat is empty
            return False
        else:
            return True

 
def main():
    filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_Xia2long_2021_9_18_5_1293/file_scl_1"
    log = LogXia2()
    log.parse(filepath)
    print(log.d_)

    filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_Xia2short_2021_10_9_7_7004/file_scl_1"
    log = LogXia2()
    log.parse(filepath)
    print(log.d_)


if __name__ == "__main__":
    main()