#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-28
# Updates:  2022-02-11 improved the general parser to process all types of logs
# =============================================================================
"""
Extract scaling statistics from Aimless log fille.
Deal with CCP4, HTML, and autoPROC logs
For CCP4 log format, Aimless stats may be only in part of the log file that
has output from other upstream or downstream softwares, the parsing focuses
on Aimless output only
"""
import os
import sys
import re
import logging
from extract.extract_log.XRAY.scaling import LogScaling  # initiate data dictionary for scaling process
from extract.util.findPattern import getStartingIndex

# all versions are imported and handled internally using the versioned python file in this folder

logger = logging.getLogger(__name__)


class LogAimless(LogScaling):  # parent class in parent folder's __init__.py
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
        # pattern = r'^Summary\s+data\s+for\s+Project:\s+'
        pattern = r'^\s*Overall\s+InnerShell\s+OuterShell\s*$'
        i_start = getStartingIndex(self.l_file, pattern) + 1
        i_end = i_start + 17 # truncate the summary section
        l_summary_section = self.l_file[i_start:i_end]
        # print(l_summary_section)
        d_re = {}
        d_re["Low resolution limit"] = ("_reflns.d_resolution_low", '_reflns_shell.d_res_low')
        d_re["High resolution limit"] = ("_reflns.d_resolution_high", '_reflns_shell.d_res_high')
        d_re["Total number unique"] = ("_reflns.number_obs", '_reflns_shell.number_unique_obs')
        d_re["Completeness"] = ("_reflns.percent_possible_obs", '_reflns_shell.percent_possible_obs')
        d_re["Mean\(+I\)\/sd\(I\)+"] = ("_reflns.pdbx_netI_over_sigmaI", '_reflns_shell.pdbx_netI_over_sigmaI_obs')
        d_re["Multiplicity"] = ("_reflns.pdbx_redundancy", '_reflns_shell.pdbx_redundancy')
        d_re["Rmeas\s+\(all I\+"] = ("_reflns.pdbx_Rrim_I_all", '_reflns_shell.pdbx_Rrim_I_all')
        d_re["Rpim\s+\(all I\+"] = ("_reflns.pdbx_Rpim_I_all", '_reflns_shell.pdbx_Rpim_I_all')
        d_re["Mn\(I\) half-set correlation CC\(1\/2\)"] = ("_reflns.pdbx_CC_half", '_reflns_shell.pdbx_CC_half')
        d_re["Total number of observations"] = ("_reflns.pdbx_number_measured_all", '_reflns_shell.number_measured_all')
        d_re["Mean\(Chi\^2\)"] = ("_reflns.pdbx_chi_squared", '_reflns_shell.pdbx_chi_squared')
        # The following two rows set up alternate parsing for Rmerge, the Rmerge could be in either way, but not both
        # Only one of them will return Rmerge value
        d_re["Rmerge\s+\(all I\+"] = ("_reflns.pdbx_Rmerge_I_obs", '_reflns_shell.Rmerge_I_obs') 
        d_re["Rmerge\s+\d"] = ("_reflns.pdbx_Rmerge_I_obs", '_reflns_shell.Rmerge_I_obs')

        for each in d_re:
            re_ = re.compile(r"^\s*%s" % each)
            for line in l_summary_section:
                if re_.search(line):
                    try:
                        l_line = line.strip().split()
                        item_overall = d_re[each][0]
                        item_shell = d_re[each][1]
                        value_overall = l_line[-3]
                        value_shell = l_line[-1]
                        self.d_["reflns"][item_overall].append(value_overall)
                        self.d_["reflns_shell"][item_shell].append(value_shell)
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
    filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_XDS_Aimless_Phaser_Phenix_2021_10_8_18_16442/file_scl_1"
    # filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_Scala_2021_10_2_9_13794/file_scl_1"    
    log = LogAimless()
    log.parse(filepath)
    print(log.d_)


if __name__ == "__main__":
    main()