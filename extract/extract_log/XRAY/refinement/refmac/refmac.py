# =============================================================================
# Author:  Chenghua Shao
# Date:    2025-03-25
# Updates:
#   
# =============================================================================
"""
Extract refinement statistics from refmac log file
Cannot parse shell information from refmac log because M(4SSQ/LL) is the
Middle of resolution bins in 4 sin^2(theta)/lambda^2 = 1/d^2
One can estimate the highest resolution bin based on the high resolution and 
middle point, but it's inaccurate. The refmac output mmCIF and PDB file does
have the full shell range.

"""
import re
import logging

# import sys
# sys.path.insert(0, "/Users/chenghua/Projects/pdb_extract/pdb-extract-prod-py/")

from extract.extract_log.XRAY.refinement import LogRefinement  # initiate data dictionary for refinement process
# all versions are imported and handled internally using the versioned python file in this folder

logger = logging.getLogger(__name__)


class LogRefmac(LogRefinement):  # parent class in parent folder's __init__.py
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
        parse refmac log file

        Returns
        -------
        None.

        Outcomes
        -------
        self.d_["refine"] to record refinement statistics
        self.d_["refine_ls_shell"] to record refinement shell statistics, but will be empty for refmac log
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
            self.parseRefine()
            self.parseBondAngleDev()

            # add static  record for refine
            if not self.isCatEmpty(self.d_["refine"]):
                self.d_["refine"]["_refine.entry_id"].append("UNNAMED")
                self.d_["refine"]["_refine.pdbx_diffrn_id"].append("1")
                self.d_["refine"]["_refine.pdbx_refine_id"].append("X-RAY DIFFRACTION")

            # add pdbx_refine_id for _refine_ls_restr
            if not self.isCatEmpty(self.d_["refine_ls_restr"]):
                for i in range(len(self.d_["refine_ls_restr"]["_refine_ls_restr.type"])):
                    self.d_["refine_ls_restr"]["_refine_ls_restr.pdbx_refine_id"].append("X-RAY DIFFRACTION")

        except Exception as e:
            logger.exception(e)
            return False

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
        re_finish = re.compile(r"WRITTEN OUTPUT MTZ FILE")  # pattern of finishing refinement
        re_end = re.compile(r"End of Refmac_")  # pattern of end of refmac run. REFMACAT will continue serval
        index_finish = -1
        index_end = -1

        self.l_final = []  # list of file lines after Final line
        # Search for finish and end lines
        for i in range(self.n_lines):
            line = self.l_file[i]
            if re_finish.search(line):
                index_finish = i
            if re_end.search(line):
                index_end = i

        if index_finish >=0 and index_end > index_finish:
            self.l_final = self.l_file[index_finish+2:index_end+1]

    def parseRefine(self):
        """parse R factor information based on RE in self.l_final section
        """
        re_resolution = re.compile(r"^Resolution limits\s*=\s*(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_refine = {}
        d_re_refine["_refine.ls_number_reflns_obs"] = re.compile(r"^Number of used reflections\s*=\s*(\d+)")
        d_re_refine["_refine.ls_percent_reflns_obs"] = re.compile(r"^Percentage observed\s*=\s*(\d+\.\d+)")
        d_re_refine["_refine.ls_percent_reflns_R_free"] = re.compile(r"^Percentage of free reflections\s*=\s*(\d+\.\d+)")
        d_re_refine["_refine.ls_R_factor_R_work"] = re.compile(r"^Overall R factor\s*=\s*(\d+\.\d+)")
        d_re_refine["_refine.ls_R_factor_R_free"] = re.compile(r"^Free R factor\s*=\s*(\d+\.\d+)")
        d_re_refine["_refine.correlation_coeff_Fo_to_Fc"] = re.compile(r"^Overall correlation coefficient\s*=\s*(\d+\.\d+)")
        d_re_refine["_refine.correlation_coeff_Fo_to_Fc_free"] = re.compile(r"^Free correlation coefficient\s*=\s*(\d+\.\d+)")
        d_re_refine["_refine.pdbx_overall_ESU_R"] = re.compile(r"^Cruickshanks DPI for coordinate error\s*=\s*(\d+\.\d+)")
        d_re_refine["_refine.pdbx_overall_ESU_R_Free"] = re.compile(r"^DPI based on free R factor\s*=\s*(\d+\.\d+)")
        d_re_refine["_refine.overall_SU_ML"] = re.compile(r"^ML based su of positional parameters\s*=\s*(\d+\.\d+)")
        d_re_refine["_refine.overall_SU_B"] = re.compile(r"^ML based su of thermal parameters\s*=\s*(\d+\.\d+)")

        for i in range(len(self.l_final)):
            line = self.l_final[i]
            if re_resolution.search(line):
                (low, high) = re_resolution.search(line).groups()
                self.d_["refine"]["_refine.ls_d_res_low"].append(low)
                self.d_["refine"]["_refine.ls_d_res_high"].append(high)
            for item in d_re_refine:
                if d_re_refine[item].search(line):
                    self.d_["refine"][item].append(d_re_refine[item].search(line).groups()[0])

    def parseBondAngleDev(self):
        """parse bond length and angle deviation information based on RE in self.l_final section
        """
        d_re_restr = {}
        d_re_restr["r_bond_refined_d"] = re.compile(r"^Bond distances: refined atoms\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_bond_other_d"] = re.compile(r"^Bond distances: others\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_angle_refined_deg"] = re.compile(r"^Bond angles  : refined atoms\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_angle_other_deg"] = re.compile(r"^Bond angles  : others\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_dihedral_angle_1_deg"] = re.compile(r"^Torsion angles, period  1. refined\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_dihedral_angle_2_deg"] = re.compile(r"^Torsion angles, period  2. refined\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_dihedral_angle_3_deg"] = re.compile(r"^Torsion angles, period  3. refined\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_chiral_restr"] = re.compile(r"^Chiral centres: refined atoms\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_gen_planes_refined"] = re.compile(r"^Planar groups: refined atoms\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_gen_planes_other"] = re.compile(r"^Planar groups: others\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_mcbond_it"] = re.compile(r"^M\. chain bond B values: refined atoms\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_mcbond_other"] = re.compile(r"^M\. chain bond B values: others\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_mcangle_it"] = re.compile(r"^M\. chain angle B values: refined atoms\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_mcangle_other"] = re.compile(r"^M\. chain angle B values: others\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_scbond_it"] = re.compile(r"^S\. chain bond B values: refined atoms\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_scbond_other"] = re.compile(r"^S\. chain bond B values: others\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_scangle_it"] = re.compile(r"^S\. chain angle B values: refined atoms\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_scangle_other"] = re.compile(r"^S\. chain angle B values: others\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_long_range_B_refined"] = re.compile(r"^Long range B values: refined atoms\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        d_re_restr["r_long_range_B_other"] = re.compile(r"^Long range B values: others\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
        for i in range(len(self.l_final)):
            line = self.l_final[i]
            for restr_type in d_re_restr:
                if d_re_restr[restr_type].search(line):
                    (n, dev, target) = d_re_restr[restr_type].search(line).groups()
                    self.d_["refine_ls_restr"]["_refine_ls_restr.type"].append(restr_type)
                    self.d_["refine_ls_restr"]["_refine_ls_restr.number"].append(n)
                    self.d_["refine_ls_restr"]["_refine_ls_restr.dev_ideal"].append(dev)
                    self.d_["refine_ls_restr"]["_refine_ls_restr.dev_ideal_target"].append(target)


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
