# =============================================================================
# Author:  Chenghua Shao
# Date:    2025-03-22
# Updates:
#   
# =============================================================================
"""
Extract refinement statistics from phenix log file
"""
import re
import logging

# import sys
# sys.path.insert(0, "/Users/chenghua/Projects/pdb_extract/pdb-extract-prod-py/")

from extract.util.findPattern import getStartingIndex
from extract.extract_log.XRAY.refinement import LogRefinement  # initiate data dictionary for refinement process
# all versions are imported and handled internally using the versioned python file in this folder

logger = logging.getLogger(__name__)


class LogPhenix(LogRefinement):  # parent class in parent folder's __init__.py
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
        LogRefinement.__init__(self)

    def parse(self, filepath):
        """
        parse phenix log file

        Returns
        -------
        None.

        Outcomes
        -------
        self.d_["refine"] to record refinement statistics
        self.d_["refine_ls_shell"] to record refinement shell statistics
        self.d_["refine_ls_restr"] to record refinement restraints statistics
        """
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as file:  #replace non-utf char with a placeholder char
                self.l_file = file.read().splitlines() #read file into a list
        except IOError as e:
            logger.exception(e)
            return False

        try:
            self.n_lines = len(self.l_file)  # number of lines
            self.truncate()
            self.parseResolution()
            self.parseRfactor()
            self.parseShell()
            self.parseBondAngleDev()

            # add static  record for refine
            if not self.isCatEmpty(self.d_["refine"]):
                self.d_["refine"]["_refine.entry_id"].append("UNNAMED")
                self.d_["refine"]["_refine.pdbx_diffrn_id"].append("1")
                self.d_["refine"]["_refine.pdbx_refine_id"].append("X-RAY DIFFRACTION")
                # if self.d_["refine"]["_refine.ls_R_factor_R_free"]:
                #     self.d_["refine"]["_refine.pdbx_ls_cross_valid_method"].append("FREE R-VALUE")

            # add pdbx_refine_id for _refine_ls_shell
            n_shell = len(self.d_["refine_ls_shell"]["_refine_ls_shell.d_res_high"])
            for i in range(n_shell):
                self.d_["refine_ls_shell"]["_refine_ls_shell.pdbx_refine_id"].append("X-RAY DIFFRACTION")

            # add pdbx_refine_id for _refine_ls_restr
            if not self.isCatEmpty(self.d_["refine_ls_restr"]):
                for i in range(len(self.d_["refine_ls_restr"]["_refine_ls_restr.type"])):
                    self.d_["refine_ls_restr"]["_refine_ls_restr.pdbx_refine_id"].append("X-RAY DIFFRACTION")

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
    
    def isCatEmpty(self, d_):
        """test if a d_cat has empty list for all data items

        Args:
            d_ (dict): d_cat

        Returns:
            bool: True if all empty
        """        
        for key in d_:
            if not d_[key]:
                return False
        return True
        
    def truncate(self):
        """truncate self.l_file of all lines into 
        self.l_final: from Final line to the end, with overall refinement stats
        self.l_shell: from X-ray data summary line to Final line, with shell data
        """        
        re_Final = re.compile(r"=====\s*Final\s*=====")  # pattern of the Final line
        reverse_index = range(self.n_lines-1, -1, -1)  # search from bottom up
        index_Final_line = -1

        self.l_final = []  # list of file lines after Final line
        self.l_shell = []  # list of shell data lines between final X-ray data line and Final line
        # Search for Final line
        for i in reverse_index:
            line = self.l_file[i]
            if re_Final.search(line):
                index_Final_line = i
                break
        if index_Final_line >= 0:
            self.l_final = self.l_file[index_Final_line:]

            # Search for shell data right above Final line
            # no need to search if there is no Final line
            re_shell_data = re.compile(r"-----X-ray data-----")
            reverse_index_shell = range(index_Final_line, -1, -1)
            index_shell_data = -1
            for i in reverse_index_shell:
                line = self.l_file[i]
                if re_shell_data.search(line):
                    index_shell_data = i
                    break
            if index_shell_data >= 0 and index_Final_line > index_shell_data:
                self.l_shell = self.l_file[index_shell_data:index_Final_line]

    def parseResolution(self):
        """parse resolution information based on RE in self.l_shell section
        """        
        re_resolution = re.compile(r"\(resolution:\s*(\d+\.\d+)\s*-\s*(\d+\.\d+)\s+A,\s+n_refl\.=(\d+)\s*\(all\),\s*(\d+\.\d+)\s+\%\s+free\)")
        for i in range(len(self.l_shell)):
            line = self.l_shell[i]
            if re_resolution.search(line):
                (high, low, n_reflection, percent_free) = re_resolution.search(line).groups()
                self.d_["refine"]["_refine.ls_d_res_high"].append(high)
                self.d_["refine"]["_refine.ls_d_res_low"].append(low)
                # self.d_["refine"]["_refine.ls_number_reflns_obs"].append(n_reflection) # use parseRfactor at the Final section
                self.d_["refine"]["_refine.ls_percent_reflns_R_free"].append(percent_free)
                break

    def parseRfactor(self):
        """parse R factor information based on RE in self.l_final section
        """        
        # re_Rfactor = re.compile(r"^\s*Final\s+R-work\s*=\s*(0.\d+),\s*R-free\s*=\s*(0.\d+)")
        re_Rfactor = re.compile(r"r\(all,work,free\)=(0.\d+)\s+(0.\d+)\s+(0.\d+)\s+n_refl\.:\s*(\d+)")
        reverse_index = range(len(self.l_final)-1, -1, -1)  # search from bottom up
        for i in reverse_index:
            line = self.l_final[i]
            if re_Rfactor.search(line):
                (Rall, Rwork, Rfree, n_reflection) = re_Rfactor.search(line).groups()
                self.d_["refine"]["_refine.ls_R_factor_obs"].append(Rall)
                self.d_["refine"]["_refine.ls_R_factor_R_work"].append(Rwork)
                self.d_["refine"]["_refine.ls_R_factor_R_free"].append(Rfree)
                self.d_["refine"]["_refine.ls_number_reflns_obs"].append(n_reflection)
                break

    def parseShell(self):
        """parse shell information based on RE in self.l_shell section
        """
        pattern = r"Bin\s+Resolution\s+Compl\.\s+No\.\s+Refl\.\s+R-factors\s+Targets"
        i_start = getStartingIndex(self.l_shell, pattern)
        for i in range(i_start+2, len(self.l_shell)):
            line = self.l_shell[i]
            l_line = line.strip().strip('|').strip().split()
            if len(l_line) != 11:
                break
            low = l_line[1]
            high = l_line[3]
            completeness = l_line[4]
            try:
                percent = str(float(completeness) * 100)
            except Exception as e:
                logger.warning("failed to convert completeness %s in log to percent with error %s", completeness, e)
                percent = "?"
            n_work = l_line[5]
            n_free = l_line[6]
            Rwork = l_line[7]
            Rfree = l_line[8]
            self.d_["refine_ls_shell"]["_refine_ls_shell.d_res_low"].append(low)
            self.d_["refine_ls_shell"]["_refine_ls_shell.d_res_high"].append(high)
            self.d_["refine_ls_shell"]["_refine_ls_shell.percent_reflns_obs"].append(percent)
            self.d_["refine_ls_shell"]["_refine_ls_shell.number_reflns_R_work"].append(n_work)
            self.d_["refine_ls_shell"]["_refine_ls_shell.number_reflns_R_free"].append(n_free)
            self.d_["refine_ls_shell"]["_refine_ls_shell.R_factor_R_work"].append(Rwork)
            self.d_["refine_ls_shell"]["_refine_ls_shell.R_factor_R_free"].append(Rfree)
        try:
            l_percent = self.d_["refine_ls_shell"]["_refine_ls_shell.percent_reflns_obs"]
            l_n_work = self.d_["refine_ls_shell"]["_refine_ls_shell.number_reflns_R_work"]
            l_n_free = self.d_["refine_ls_shell"]["_refine_ls_shell.number_reflns_R_free"]
            n_all = 0
            n_theoritical = 0
            if len(l_percent) >= 1:
                for i in range(len(l_percent)):
                    percent = l_percent[i]
                    n_work = int(l_n_work[i])
                    n_free = int(l_n_free[i])
                    n_shell = n_work + n_free
                    n_all += n_shell
                    n_theoritical_shell = int(n_shell/(float(percent)/100))
                    n_theoritical += n_theoritical_shell
                completeness_all = round(n_all/n_theoritical, 4)
                if completeness_all <= 1:
                    percent_all = str(completeness_all * 100)
                    self.d_["refine"]["_refine.ls_percent_reflns_obs"].append(percent_all)
        except Exception as e:
            logger.warning("failed to compute _refine.ls_percent_reflns_obs, skip")

    def parseBondAngleDev(self):
        """parse bond length and angle deviation information based on RE in self.l_final section
        """        
        re_step_stats = re.compile(r"^\s+end:\s*\d")
        reverse_index = range(len(self.l_final)-1, -1, -1)  # search from bottom up
        for i in reverse_index:  # find bond and angle dev value under REFINEMENT STATISTICS STEP BY STEP
            line = self.l_final[i]
            if re_step_stats.search(line):
                l_line = line.strip().split()
                if len(l_line) == 10:
                    bond_dev = l_line[3]
                    angle_dev = l_line[4]
                    b_iso_mean = l_line[7]
                    n_water = l_line[8]
                # self.d_["refine"]["_refine.B_iso_mean"].append(b_iso_mean)
                self.d_["refine_ls_restr"]["_refine_ls_restr.dev_ideal"].append(bond_dev)
                self.d_["refine_ls_restr"]["_refine_ls_restr.type"].append("f_bond_d")
                self.d_["refine_ls_restr"]["_refine_ls_restr.dev_ideal"].append(angle_dev)
                self.d_["refine_ls_restr"]["_refine_ls_restr.type"].append("f_angle_d")
                break
        
        re_bond_restr = re.compile(r"^\s*Bond restraints:\s+(\d+)")
        for i in reverse_index:  # find bond restraints number
            line = self.l_final[i]
            if re_bond_restr.search(line):
                n_bond_restr = re_bond_restr.search(line).groups()[0]
                self.d_["refine_ls_restr"]["_refine_ls_restr.number"].append(n_bond_restr)
                break

        re_angle_restr = re.compile(r"^\s*Bond angle restraints:\s+(\d+)")
        for i in reverse_index:  # find angle restraints number
            line = self.l_final[i]
            if re_angle_restr.search(line):
                n_angle_restr = re_angle_restr.search(line).groups()[0]
                self.d_["refine_ls_restr"]["_refine_ls_restr.number"].append(n_angle_restr)
                break            


    def orderShell(self):
        """
        order shell from high to low resolution

        Returns
        -------
        None.

        Outcomes
        -------
        self.d_["refine_ls_shell"] may be reordered

        """
        l_high_resolution = []
        if self.d_["refine_ls_shell"]:
            l_high_resolution = self.d_["refine_ls_shell"]['_refine_ls_shell.d_res_high']
            try:
                if float(l_high_resolution[0]) > float(l_high_resolution[-1]):
                    for item in self.d_["refine_ls_shell"]:
                        self.d_["refine_ls_shell"][item].reverse()
            except ValueError:
                pass

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
#     filepath = "/Users/chenghua/Projects/pdb_extract/Refine_log/phenix_1.21.2_XRAY_2025_2_27_3_9_2670933"
#     filepath = "/Users/chenghua/Projects/pdb_extract/Refine_log/phenix_1.20.1_XRAY_2025_3_22_8_31_3200069"
#     filepath = "/Users/chenghua/Projects/pdb_extract/Refine_log/phenix_1.18_XRAY_2025_3_9_23_31_2919757"
#     filepath = "/Users/chenghua/Projects/pdb_extract/Refine_log/phenix_1.10.1_XRAY_2025_3_7_1_36_2855597"
#     filepath = "/Users/chenghua/Projects/pdb_extract/Refine_log/phenix_2.0rc1_5617_XRAY_2025_3_7_8_51_2862763"
#     log = LogPhenix()
#     log.parse(filepath)
#     d_ = log.d_
#     for item in d_["refine"]:
#         print(item, d_["refine"][item])
#     print()
#     for item in d_["refine_ls_shell"]:
#         print(item, d_["refine_ls_shell"][item])
#     print()
#     for item in d_["refine_ls_restr"]:
#         print(item, d_["refine_ls_restr"][item])
#     print()
# if __name__ == "__main__":
#     main()
