#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2021-11-11
# Updates:
#   2022-06-10 CS refactor
# =============================================================================
"""
Extract scaling statistics from d*Trek log fille
"""
import re
import logging
from extract.extract_log.XRAY.scaling import LogScaling  # initiate data dictionary for scaling process

logger = logging.getLogger(__name__)


class LogDtrek(LogScaling):  # parent class in parent folder's __init__.py
    """class for parsing d*Trek log file
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
        except UnicodeDecodeError:
            with open(filepath, encoding = "ISO-8859-1") as file:
                self.l_file = file.read().splitlines() #read file into a list

        try:
            self.n_lines = len(self.l_file)  # number of lines
            self.parseCompleteness() # processs completeness section
            self.parseRfactors()  # process R factors section

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

    def parseDataSection(self, i_start):
        """
        Parse out data section with number line only

        Parameters
        ----------
        i_start : TYPE
            starting index of list of lines for the fline.

        Returns
        -------
        ll_data_matrix : list
            list of list, with each component being a list of row values

        """
        re_separator = re.compile(r'^----------------------------------')
        re_char = re.compile(r'[a-zA-Z]')
        ll_data_matrix = []
        for i in range(i_start, self.n_lines):
            line = self.l_file[i]
            if line.strip():
                if not re_separator.search(line.strip()):
                    if re_char.search(line):  # if seeing non-number letters
                        if ll_data_matrix:
                            break  # break to finish reading of shell stats
                        else:
                            continue  # continue to read next line
                    else:  # find shell stat row with only numbers
                        l_line = line.strip().split()
                        l_value = []
                        for each in l_line:
                            l_value.append(each.strip())
                        if l_value:
                            ll_data_matrix.append(l_value)
        return ll_data_matrix

    def parseCompleteness(self):
        """
        Parse Completeness setion to get unique obs reflns, redundancy,
        and completeness

        Returns
        -------
        None.

        """
        pattern = r'^\s*Completeness vs Resolution\s*$'
        i_start = self.getStartingIndex(pattern)
        ll_data_matrix = self.parseDataSection(i_start)
        if ll_data_matrix and len(ll_data_matrix) >= 3:
            l_all = ll_data_matrix[-1]
            ll_shell = ll_data_matrix[:-1]
            if len(l_all) == 12:
                self.d_["reflns"]["_reflns.d_resolution_low"].append(l_all[0])
                self.d_["reflns"]["_reflns.d_resolution_high"].append(l_all[2])
                self.d_["reflns"]["_reflns.pdbx_number_measured_all"].append(l_all[4])
                self.d_["reflns"]["_reflns.number_obs"].append(l_all[8])
                self.d_["reflns"]["_reflns.pdbx_redundancy"].append(l_all[9])
                self.d_["reflns"]["_reflns.percent_possible_obs"].append(l_all[10])
            for l_each_shell in ll_shell:
                if len(l_each_shell) == 12:
                    self.d_["reflns_shell"]["_reflns_shell.d_res_low"].append(l_each_shell[0])
                    self.d_["reflns_shell"]["_reflns_shell.d_res_high"].append(l_each_shell[2])
                    self.d_["reflns_shell"]["_reflns_shell.number_measured_all"].append(l_each_shell[4])
                    self.d_["reflns_shell"]["_reflns_shell.number_unique_obs"].append(l_each_shell[8])
                    self.d_["reflns_shell"]["_reflns_shell.pdbx_redundancy"].append(l_each_shell[9])
                    self.d_["reflns_shell"]["_reflns_shell.percent_possible_obs"].append(l_each_shell[10])             

    def parseRfactors(self):
        """
        Parse R-factors section to get Rmerge, Chi**2, and resolution limits

        Returns
        -------
        None.

        """
        pattern = r'^\s*Merging R factors vs Resolution\s*$'
        i_start = self.getStartingIndex(pattern)
        ll_data_matrix = self.parseDataSection(i_start)
        if ll_data_matrix and len(ll_data_matrix) >= 3:
            l_all = ll_data_matrix[-1]
            ll_shell = ll_data_matrix[:-1]
            if len(l_all) == 13:
                self.d_["reflns"]["_reflns.pdbx_netI_over_sigmaI"].append(l_all[4])
                self.d_["reflns"]["_reflns.pdbx_chi_squared"].append(l_all[8])
                self.d_["reflns"]["_reflns.pdbx_Rmerge_I_obs"].append(l_all[9])
                self.d_["reflns"]["_reflns.pdbx_Rrim_I_all"].append(l_all[11])
            for l_each_shell in ll_shell:
                if len(l_each_shell) == 13:
                    self.d_["reflns_shell"]["_reflns_shell.pdbx_netI_over_sigmaI_obs"].append(l_each_shell[4])
                    self.d_["reflns_shell"]['_reflns_shell.pdbx_chi_squared'].append(l_each_shell[8])
                    self.d_["reflns_shell"]["_reflns_shell.Rmerge_I_obs"].append(l_each_shell[9])
                    self.d_["reflns_shell"]["_reflns_shell.pdbx_Rrim_I_all"].append(l_each_shell[11])

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
    filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_dTREK_2021_10_16_16_7040/file_scl_1"
    log = LogDtrek()
    log.parse(filepath)
    for item in log.d_["reflns"]:
        print(item, log.d_["reflns"][item])
    print()
    for item in log.d_["reflns_shell"]:
        print(item, log.d_["reflns_shell"][item])
    print(log.d_)


if __name__ == "__main__":
    main()