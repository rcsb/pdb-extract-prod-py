#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2021-11-11
# Updates:
#   2022-06-10 CS refactor
# =============================================================================
"""
Extract scaling statistics from Scalepack log fille
"""
import re
import logging
# currentdir = os.getcwd()
# parentdir = os.path.dirname(currentdir)
# sys.path.insert(0, parentdir)
# sys.path.insert(0, "/Users/chenghua/Projects/pdb_extract/Dev_20211015/pdb_extract")
from extract.extract_log.XRAY.scaling import LogScaling  # initiate data dictionary for scaling process
# import extract.extract_log.XRAY.scaling.scalepack.ver_9_9_9
# all versions are imported and handled internally using the versioned python file in this folder

logger = logging.getLogger(__name__)


class LogScalepack(LogScaling):  # parent class in parent folder's __init__.py
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

    def getStartingIndex(self, pattern, n_occur="last"):
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
        index_line = -1
        if n_occur == "last":
            for i in range(self.n_lines):
                line = self.l_file[i]
                if re_pattern.search(line):
                    index_line = i
        else:
            i_occur = 0
            for i in range(self.n_lines):
                line = self.l_file[i]
                if re_pattern.search(line):
                    i_occur += 1
                    if i_occur == n_occur:
                        index_line = i
                        break
        return index_line

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
            self.parseBatch()  # process batch section to get average I/Sig and obs reflns
            self.parseRedundancy()  # process redundancy section to get redundancy
            self.parseIsig1()  # process I/Sig 1st section to get unique obs reflns
            self.parseIsig2()  # process I/Sig 2nd section to get data completeness
            self.parseRmerge()  # process R section to get Rmerge, Chi**2, and resolution limits

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

    def parseBatch(self):
        """
        Parse batch stats section to get average I/Sig and obs reflns.

        Returns
        -------
        True if parsed;
        False if not parsed

        """
        pattern = r'Summary of reflection intensities and R-factors by batch number'
        i_start = self.getStartingIndex(pattern)
        line_of_column_attr = self.l_file[i_start+2] # check the line of column attr list
        if line_of_column_attr.strip() != "Batch     # obs # obs > 1   <I/sigma> N. Chi**2    R-fac":
            self.d_["reflns"]["_reflns.pdbx_netI_over_sigmaI"].append('?')
            self.d_["reflns"]["_reflns.pdbx_number_measured_all"].append('?')
            logger.warning("batch statistics column attr row not recognized")
            return False

        re_value = re.compile(r'^\s*All films')
        for i in range(i_start+3, self.n_lines): # start with line under column attr
            line = self.l_file[i]
            if re_value.search(line):
                try:
                    self.d_["reflns"]["_reflns.pdbx_netI_over_sigmaI"].append(line.strip().split()[-3])
                    self.d_["reflns"]["_reflns.pdbx_number_measured_all"].append(line.strip().split()[-5])
                    return True
                except IndexError as msg:
                    logger.warning(msg)
        return False

    def parseRedundancy(self):
        """
        Parse redundancy stats section to get redundancy

        Returns
        -------
        None.

        """
        pattern = r"Average Redundancy Per Shell"
        i_start = self.getStartingIndex(pattern)
        re_value = re.compile(r'All hkl')
        for i in range(i_start, self.n_lines):
            line = self.l_file[i]
            if re_value.search(line):
                try:
                    self.d_["reflns"]["_reflns.pdbx_redundancy"].append(line.strip().split()[-1])
                    break
                except IndexError as msg:
                    logger.warning(msg)

        ll_shell_matrix = self.parseShell(i_start)
        for i in range(len(ll_shell_matrix)):
            l_shell = ll_shell_matrix[i]
            self.d_["reflns_shell"]["_reflns_shell.pdbx_redundancy"].append(l_shell[2])

    def parseIsig1(self):
        """
        Parse 1st I/Sigma section to get unique obs reflns

        Returns
        -------
        None.

        """
        # pattern = r'I/Sigma in resolution shells'
        pattern = r'Lower Upper      No. of reflections with I / Sigma less than'
        i_start = self.getStartingIndex(pattern)
        re_value = re.compile(r'^\s*All hkl')
        for i in range(i_start, self.n_lines):
            line = self.l_file[i]
            if re_value.search(line):
                try:
                    self.d_["reflns"]["_reflns.number_obs"]\
                        .append(line.strip().split()[-1])
                    break
                except IndexError as msg:
                    logger.warning(msg)

        ll_shell_matrix = self.parseShell(i_start)
        for i in range(len(ll_shell_matrix)):
            l_shell = ll_shell_matrix[i]
            self.d_["reflns_shell"]["_reflns_shell.number_unique_obs"].append(l_shell[-1])

    def parseIsig2(self):
        """
        Parse 2nd I/Sigma section to get data completeness

        Returns
        -------
        None.

        """
        # pattern = r'I/Sigma in resolution shells'
        pattern = r'Lower Upper      % of of reflections with I / Sigma less than'
        i_start = self.getStartingIndex(pattern)
        re_value = re.compile(r'^\s*All hkl')
        for i in range(i_start, self.n_lines):
            line = self.l_file[i]
            if re_value.search(line):
                try:
                    self.d_["reflns"]["_reflns.percent_possible_obs"]\
                        .append(line.strip().split()[-1])
                    break
                except IndexError as msg:
                    logger.warning(msg)

        ll_shell_matrix = self.parseShell(i_start)
        for i in range(len(ll_shell_matrix)):
            l_shell = ll_shell_matrix[i]
            self.d_["reflns_shell"]["_reflns_shell.percent_possible_all"].append(l_shell[-1])

    def parseRmerge(self):
        """
        Parse R-factors section to get R factors, Chi**2, and resolution limits

        Returns
        -------
        None.

        """
        pattern = r"Summary of reflections intensities and R-factors by shells"
        i_start = self.getStartingIndex(pattern)

        # first need to find the row with column attr and collect attr into a list
        # old scalepack has less attr than HKL2000/HKL3000
        l_attr = []
        i_start_value = -1
        re_line_of_attr = re.compile(r'^\s*limit\s+')
        for i in range(i_start, i_start+10):
            line = self.l_file[i]
            if re_line_of_attr.search(line):
                i_start_value = i+1
                n_R_fac = 0
                for each in line.strip().split():
                    if each == "limit":
                        l_attr.append("lower limit")
                    elif each == "Angstrom":
                        l_attr.append("higher limit")
                    elif each == "R-fac":
                        if n_R_fac == 0:
                            n_R_fac += 1
                            l_attr.append("Linear R-fac")
                        else:
                            l_attr.append("Square R-fac")
                    else:
                        l_attr.append(each)
                break

        if not l_attr:
            return False

        l_attr2check = ['lower limit', 'higher limit', 'I', 'error', 'stat.', 'Chi**2', 'Linear R-fac', 'Square R-fac', 'Rmeas', 'Rpim', 'CC1/2', 'CC*']

        l_item_overall = ["_reflns.pdbx_Rmerge_I_obs",
                          "_reflns.pdbx_chi_squared",
                          "_reflns.pdbx_CC_star",
                          "_reflns.pdbx_CC_half",
                          "_reflns.pdbx_Rpim_I_all",
                          "_reflns.pdbx_Rrim_I_all"]
        d_item_overall = {}
        d_item_overall["_reflns.pdbx_Rmerge_I_obs"] = "Linear R-fac"
        d_item_overall["_reflns.pdbx_chi_squared"] = "Chi**2"
        d_item_overall["_reflns.pdbx_CC_star"] = "CC*"
        d_item_overall["_reflns.pdbx_CC_half"] = "CC1/2"
        d_item_overall["_reflns.pdbx_Rpim_I_all"] = "Rpim"
        d_item_overall["_reflns.pdbx_Rrim_I_all"] = "Rmeas"

        re_value = re.compile(r'All reflections')
        for i in range(i_start_value, self.n_lines):
            line = self.l_file[i]
            if re_value.search(line):
                l_value_overall = line.strip().split()
                if len(l_attr) == len(l_value_overall):
                    d_value_overall = {}
                    for j in range(len(l_attr)):
                        d_value_overall[l_attr[j]] = [l_value_overall[j]]
                    for item_overall in l_item_overall:
                        attr = d_item_overall[item_overall]
                        if attr in d_value_overall:
                            self.d_["reflns"][item_overall] = d_value_overall[attr]
                    break

        # process shell data
        l_item_shell = ["_reflns_shell.d_res_low",
                        "_reflns_shell.d_res_high",
                        "_reflns_shell.Rmerge_I_obs",
                        "_reflns_shell.pdbx_chi_squared",
                        "_reflns_shell.pdbx_CC_star",
                        "_reflns_shell.pdbx_CC_half",
                        "_reflns_shell.pdbx_Rpim_I_all",
                        "_reflns_shell.pdbx_Rrim_I_all"]

        d_item_shell = {}
        d_item_shell["_reflns_shell.d_res_low"] = "lower limit"
        d_item_shell["_reflns_shell.d_res_high"] = "higher limit"
        d_item_shell["_reflns_shell.Rmerge_I_obs"] = "Linear R-fac"
        d_item_shell["_reflns_shell.pdbx_chi_squared"] = "Chi**2"
        d_item_shell["_reflns_shell.pdbx_CC_star"] = "CC*"
        d_item_shell["_reflns_shell.pdbx_CC_half"] = "CC1/2"
        d_item_shell["_reflns_shell.pdbx_Rpim_I_all"] = "Rpim"
        d_item_shell["_reflns_shell.pdbx_Rrim_I_all"] = "Rmeas"

        d_value_shell = {}
        for i in range(len(l_attr)):
            d_value_shell[l_attr[i]] = []

        ll_shell_matrix = self.parseShell(i_start_value) # parse shell stats into a matrix
        for l_each_shell in ll_shell_matrix:
            if len(l_attr) == len(l_each_shell):
                for j in range(len(l_attr)):
                    d_value_shell[l_attr[j]].append(l_each_shell[j]) # convert values into a dictionary

        for item_shell in l_item_shell:
            attr = d_item_shell[item_shell]
            if attr in d_value_shell:
                self.d_["reflns_shell"][item_shell] = d_value_shell[attr]

        # finally add the high and low resolution for overall stats
        self.d_["reflns"]["_reflns.d_resolution_low"].append(d_value_shell["lower limit"][0])
        self.d_["reflns"]["_reflns.d_resolution_high"].append(d_value_shell["higher limit"][-1])

    def parseShell(self, i_start):
        """
        parse structured reflection shell stats into a matrix-like list

        Parameters
        ----------
        i_start : int
            starting line number (index) of the pattern.

        Returns
        -------
        ll_shell_matrix : list
            shell stats as list of list, each element is a list of a shell

        """
        ll_shell_matrix = []
        re_char = re.compile(r'[a-zA-Z]')
        for i in range(i_start, self.n_lines):
            line = self.l_file[i]
            if line.strip():
                if re_char.search(line):  # section ends if non-number occurs
                    if ll_shell_matrix:
                        break  # break to finish reading of shell stats
                    else:
                        continue  # continue to read next line
                else:  # find shell stat row with only numbers
                    l_line = line.strip().split()
                    l_value = []
                    for each in l_line:
                        l_value.append(each.strip())
                    if l_value:
                        ll_shell_matrix.append(l_value)
        return ll_shell_matrix

    # def replaceMissingValues(self):
    #     for cat in self.d_:
    #         n_rows = 0
    #         for item in self.d_[cat]:
    #             l_value = self.d_[cat][item]
    #             if n_rows < len(l_value):  # find the maximal n_rows
    #                 n_rows = len(l_value)
    #         if n_rows:
    #             for item in self.d_[cat]:
    #                 if not self.d_[cat][item]:
    #                     self.d_[cat][item] = ['?'] * n_rows

    def verifyData(self):
        """
        Verify number of values for each row and remove empty row

        Returns
        -------
        None.

        """
        d_clean = {}
        for cat in self.d_:
            if self.verifySameNumOfValuesPerRow(self.d_[cat]):
                d_clean[cat] = {}
                for item in self.d_[cat]:
                    if len(self.d_[cat][item]) != 0:  # only if row is not emtpy
                        d_clean[cat][item] = self.d_[cat][item]
        self.d_ = d_clean

    def verifySameNumOfValuesPerRow(self, d_cat):
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



# def main():
#     # filepath = "/Users/chenghua/Projects/pdb-extract-prod-py/tests/test_data/PDB_Template_Scalepack_1/scalepack.log"
#     # filepath = "/Users/chenghua/Projects/pdb-extract-prod-py/tests/test_data/PDB_HKL2000_Phaser_Refmac_2021_9_28_13_26368/file_scl_1"
#     filepath = "/Users/chenghua/Projects/pdb-extract-prod-py/tests/test_data/PDB_HKL3000_Phaser_Refmac_2023_01_12/file_scl_1"
#     log = LogScalepack()
#     log.parse(filepath)
#     for item in log.d_["reflns"]:
#         print(item, log.d_["reflns"][item])
#     print()
#     for item in log.d_["reflns_shell"]:
#         print(item, log.d_["reflns_shell"][item])
#     print(log.d_)


# if __name__ == "__main__":
#     main()
