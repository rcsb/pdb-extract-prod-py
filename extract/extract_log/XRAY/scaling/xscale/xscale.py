#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2021-11-11
# Updates:
#   2022-06-10 CS refactor
# =============================================================================
"""
Extract scaling statistics from Xscale log fille
"""
import re
import logging
from extract.extract_log.XRAY.scaling import LogScaling  # initiate data dictionary for scaling process

logger = logging.getLogger(__name__)


class LogXscale(LogScaling):  # parent class in parent folder's __init__.py
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

    def orderShell(self):
        """
        order shell from high to low resolution

        Returns
        -------
        None.
        
        Outcomes
        -------
        self.d_["reflns_shell"] may be reordered

        """
        l_high_resolution = []
        if self.d_["reflns_shell"]:
            l_high_resolution = self.d_["reflns_shell"]['_reflns_shell.d_res_high']
            try:
                if float(l_high_resolution[0]) > float(l_high_resolution[-1]):
                    for item in self.d_["reflns_shell"]:
                        self.d_["reflns_shell"][item].reverse()
            except ValueError:
                pass

    def parse(self, filepath):
        """
        parse Scalepack log file

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

        self.orderShell()  # order shell from high resolution to low
        self.verifyData()  # verify cat integrity and remove empty row
        
        if self.d_:
            logger.info("data parsed successfully from log file %s" % filepath)
            return True
        else:
            logger.warning("no data parsed from log file %s" % filepath)
            return False

    def getLineIndex(self, l_pattern_to_search):
        l_index = list(range(self.n_lines))
        # l_index.reverse()
        for i in l_index:
            line = self.l_file[i]
            for pattern in l_pattern_to_search:
                if line.strip() == pattern:
                    i_start = i+3
                    return (pattern, i_start)
        return (None, None)
        
    def parseSummary(self):
        """
        Parse Summary section

        Returns
        -------
        None.

        """
        l_summary_line_header = []
        l_summary_line_header.append("RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano")
        l_summary_line_header.append("RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  Rmrgd-F  S_norm/")

        (header, i_start) = self.getLineIndex(l_summary_line_header)
        
        if not i_start:
            logger.warning("cannot find suitable XSCAlE header for the summary table, skip parsing")
            return False
        
        ll_shell_matrix = []
        l_all = []
        l_resolution = []
        
        for i in range(i_start, self.n_lines):
            line = self.l_file[i]
            if line.strip():
                l_line = line.strip().split()
                try: 
                    l_resolution.append(str(float(l_line[0])))
                    ll_shell_matrix.append(l_line)
                except ValueError:
                    if l_line[0] == "total":
                        l_all = l_line
                    break
        
        if l_all:
            if header == "RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  CC(1/2)  Anomal  SigAno   Nano":
                try:
                    self.d_["reflns"]["_reflns.d_resolution_high"].append(l_resolution[-1])
                    self.d_["reflns"]["_reflns.d_resolution_low"].append('?')
                    self.d_["reflns"]["_reflns.pdbx_number_measured_all"].append(l_all[1].strip())
                    self.d_["reflns"]["_reflns.number_obs"].append(l_all[2].strip())
                    self.d_["reflns"]["_reflns.percent_possible_obs"].append(l_all[4].strip('%'))
                    self.d_["reflns"]["_reflns.pdbx_Rmerge_I_obs"].append(str(round(float(l_all[5].strip('%'))/100,3)))
                    self.d_["reflns"]["_reflns.pdbx_netI_over_sigmaI"].append(l_all[8].strip())
                    self.d_["reflns"]["_reflns.pdbx_Rrim_I_all"].append(str(round(float(l_all[9].strip('%'))/100,3)))
                    self.d_["reflns"]["_reflns.pdbx_CC_half"].append(str(round(float(l_all[10].strip('*'))/100,3)))
                except Exception as msg:
                    logger.warning(msg)
                try:
                    l_resolution.insert(0, "?")  # add unknown low resolution limit
                    for i in range(len(ll_shell_matrix)):
                        l_shell = ll_shell_matrix[i]
                        self.d_["reflns_shell"]["_reflns_shell.d_res_high"].append(l_shell[0].strip())
                        self.d_["reflns_shell"]["_reflns_shell.d_res_low"].append(l_resolution[i])
                        self.d_["reflns_shell"]["_reflns_shell.number_measured_obs"].append(l_shell[1].strip())
                        self.d_["reflns_shell"]["_reflns_shell.number_unique_obs"].append(l_shell[2].strip())
                        self.d_["reflns_shell"]["_reflns_shell.percent_possible_obs"].append(l_shell[4].strip('%'))
                        self.d_["reflns_shell"]["_reflns_shell.Rmerge_I_obs"].append(str(round(float(l_shell[5].strip('%'))/100,3)))
                        self.d_["reflns_shell"]["_reflns_shell.pdbx_netI_over_sigmaI_obs"].append(l_shell[8].strip())
                        self.d_["reflns_shell"]["_reflns_shell.pdbx_Rrim_I_all"].append(str(round(float(l_shell[9].strip('%'))/100,3)))
                        self.d_["reflns_shell"]["_reflns_shell.pdbx_CC_half"].append(str(round(float(l_shell[10].strip('*'))/100,3)))
                except Exception as msg:
                    logger.warning(msg)
            elif header == "RESOLUTION     NUMBER OF REFLECTIONS    COMPLETENESS R-FACTOR  R-FACTOR COMPARED I/SIGMA   R-meas  Rmrgd-F  S_norm/":
                try:
                    self.d_["reflns"]["_reflns.d_resolution_high"].append(l_resolution[-1])
                    self.d_["reflns"]["_reflns.d_resolution_low"].append('?')
                    self.d_["reflns"]["_reflns.pdbx_number_measured_all"].append(l_all[1].strip())
                    self.d_["reflns"]["_reflns.number_obs"].append(l_all[2].strip())
                    self.d_["reflns"]["_reflns.percent_possible_obs"].append(l_all[4].strip('%'))
                    self.d_["reflns"]["_reflns.pdbx_Rmerge_I_obs"].append(str(round(float(l_all[5].strip('%'))/100,3)))
                    self.d_["reflns"]["_reflns.pdbx_netI_over_sigmaI"].append(l_all[8].strip())
                    self.d_["reflns"]["_reflns.pdbx_Rrim_I_all"].append(str(round(float(l_all[9].strip('%'))/100,3)))
                except Exception as msg:
                    logger.warning(msg)
                try:
                    l_resolution.insert(0, "?")  # add unknown low resolution limit
                    for i in range(len(ll_shell_matrix)):
                        l_shell = ll_shell_matrix[i]
                        self.d_["reflns_shell"]["_reflns_shell.d_res_high"].append(l_shell[0].strip())
                        self.d_["reflns_shell"]["_reflns_shell.d_res_low"].append(l_resolution[i])
                        self.d_["reflns_shell"]["_reflns_shell.number_measured_obs"].append(l_shell[1].strip())
                        self.d_["reflns_shell"]["_reflns_shell.number_unique_obs"].append(l_shell[2].strip())
                        self.d_["reflns_shell"]["_reflns_shell.percent_possible_obs"].append(l_shell[4].strip('%'))
                        self.d_["reflns_shell"]["_reflns_shell.Rmerge_I_obs"].append(str(round(float(l_shell[5].strip('%'))/100,3)))
                        self.d_["reflns_shell"]["_reflns_shell.pdbx_netI_over_sigmaI_obs"].append(l_shell[8].strip())
                        self.d_["reflns_shell"]["_reflns_shell.pdbx_Rrim_I_all"].append(str(round(float(l_shell[9].strip('%'))/100,3)))
                except Exception as msg:
                    logger.warning(msg)
        return True

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
                    if len(d_cat[item]) != num_values:  # for any other rows
                        return False  # if any other rows differ from the 1st
        if num_values == 0:  # if entire cat is empty
            return False
        else:
            return True



def main(): 
    #filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_XDS_Xscale_2021_10_11_2_16188/file_scl_1"
    filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_XDS_Xscale_2021_10_11_2_16188/file_index_1"
    # filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_XDS_Xscale_2021_10_13_8_10408/file_scl_1"
    log = LogXscale()
    log.parse(filepath)
    print(log.d_)


if __name__ == "__main__":
    main()
