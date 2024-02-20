#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2023-12-01
# Updates:
#
# =============================================================================
"""
Extract scaling statistics from cctbx.xfel log fille
"""
import re
import logging

from extract.util.findPattern import getStartingIndex
from extract.extract_log.XRAY.scaling import LogScaling  # initiate class data dictionary

logger = logging.getLogger(__name__)


class LogCctbx_xfel(LogScaling):  # parent class in parent folder's __init__.py
    """class for parsing cctbx.xfel log file
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
        """parse cctbx.xfel log file

        Args:
            filepath (_type_): cctbx.xfel log file path

        Returns:
            True: parse OK
            False: parse failed

        Outcomes: class dict self.d_
            self.d_["reflns"] to record reflection statistics
            self.d_["reflns_shell"] to record reflection shell statistics
            also added wavelength, number of lattices, and xfel marker
        """
        logger.info("start reading cctbx_xfel log file at %s", filepath)
        try:
            with open(filepath, 'r', errors='ignore') as file:
                self.l_file = file.read().splitlines() #read file into a list
        except IOError as e:
            logger.exception("fail to read cctbx_xfel log file at %s with error %s", filepath, e)
            return False

        # parse reflns and reflns_shell categories
        logger.info("start to parse Table of Scaling Results")
        if not self.parseScale():
            return False  # a parse failure means format change, stop
        
        logger.info("start to parse Intensity Statistics (all accepted experiments)")
        if not self.parseMerge():
            return False  # a parse failure means format change, stop
        
        logger.info("further process of reflns and reflns_shell")
        if not self.orderShell():  # order shell from high resolution to low
            return False  # a re-order failure means format change, stop
        
        # process overall low resolution
        low_res_overall = self.parseLowResolution() # find overall low resolution if present
        if self.d_["reflns_shell"]["_reflns_shell.d_res_low"]:
            try:
                low_res = self.d_["reflns_shell"]["_reflns_shell.d_res_low"][-1]
                if float(low_res) < 0:
                    if float(low_res_overall) > 0:
                        low_res = low_res_overall
                    else:
                        low_res = '?'
                self.d_["reflns_shell"]["_reflns_shell.d_res_low"][-1] = low_res
                self.d_["reflns"]["_reflns.d_resolution_low"].append(low_res)
            except Exception as e:
                logger.warning("cannot convert low resolution data in the lowest resolution shell with error '%s'", e)
    
        # process overall high resolution
        if self.d_["reflns_shell"]["_reflns_shell.d_res_high"]:
            self.d_["reflns"]["_reflns.d_resolution_high"].append(self.d_["reflns_shell"]["_reflns_shell.d_res_high"][0])

        # add static ordinal record for reflns
        self.d_["reflns"]["_reflns.entry_id"].append("UNNAMED")
        self.d_["reflns"]["_reflns.pdbx_diffrn_id"].append("1")
        self.d_["reflns"]["_reflns.pdbx_ordinal"].append("1")

        # add static ordinal record for reflns_shell
        n_shell = len(self.d_["reflns_shell"]["_reflns_shell.d_res_high"])
        for i in range(n_shell):
            self.d_["reflns_shell"]["_reflns_shell.pdbx_diffrn_id"].append("1")
            self.d_["reflns_shell"]["_reflns_shell.pdbx_ordinal"].append(str(i+1))
        # END of reflns and reflns_shell process

        logger.info("start to parse wavelength")
        self.parseWavelength()

        logger.info("start to parse number of lattices")
        self.parseLattices()

        # add xfel marker
        self.d_["diffrn"] = {}
        self.d_["diffrn"]["_diffrn.id"] = ['1']
        self.d_["diffrn"]["_diffrn.pdbx_serial_crystal_experiment"] = ['Y']

        self.verifyData()  # verify cat integrity and remove empty row

        if self.d_:
            for cat, d_cat in self.d_.items():
                for key, value in d_cat.items():
                    if value:
                        logger.debug("%s cat dict %s: %s", cat, key, value)
            return True
        else:
            logger.warning("no data parsed from log file %s" % filepath)
            return False

    def parseScale(self):
        """
        Parse Table of Scaling Results into class dictionary

        Returns
        -------
        True: Parse OK
        False: Parse failed

        """
        pattern = r"^\s*Table of Scaling Results\:"
        i_start = getStartingIndex(self.l_file, pattern)
        if i_start < 0:
            logger.warning("cannot find Table of Scaling Results, stop")
            return False
        logger.info("find Table of Scaling Results from line index %s", i_start)


        i_start_value = -1  # set line index where the value starts
        re_line_of_attr = re.compile(r'^\s*Bin\s+')
        for i in range(i_start, i_start+15):
            line = self.l_file[i]
            if re_line_of_attr.search(line):
                i_start_value = i+2
                logger.info("find table header from line index %s", i_start_value)
                break
        if i_start_value < 0:
            logger.warning("cannot find value in Table of Scaling Results, stop")
            return False
        
        i_overall_value = -1  # set line index for all reflection values
        re_overall_value = re.compile(r'^\s*All\s+') 
        for i in range(i_start_value, i_start_value+60):
            line = self.l_file[i]               
            if re_overall_value.search(line):
                i_overall_value = i
                break
        if i_overall_value < 0:
            logger.warning("cannot find overall value in Table of Scaling Results, stop")
            return False
        
        # process overall stats
        l_row_overall = self.l_file[i_overall_value].strip().split()
        logger.info("parse overall scaling stats into %s", l_row_overall)
        if len(l_row_overall) == 12:
            try:
                [n_obs, n_full] = l_row_overall[1].strip('[').strip(']').split('/')
                completeness = round(int(n_obs)/int(n_full), 3)
                cc_half = round(float(l_row_overall[2].strip('%'))/100, 3)
                r_split = round(float(l_row_overall[7].strip('%'))/100, 3)
                self.d_["reflns"]["_reflns.percent_possible_obs"].append(str(completeness))
                self.d_["reflns"]["_reflns.pdbx_CC_half"].append(str(cc_half))
                self.d_["reflns"]["_reflns.number_obs"].append(n_obs)
                self.d_["reflns"]["_reflns.pdbx_R_split"].append(str(r_split))
            except Exception as e:
                logger.warning("Log file line #%s, cannot parse overall stats in Table of Scaling Results wth error '%s'",
                               i_overall_value, e)

        # process shells
        for i in range(i_start_value, i_overall_value):
            l_row = self.l_file[i].strip().split()
            if len(l_row) == 15:
                try:
                    [n_obs, n_full] = l_row[4].strip('[').strip(']').split('/')
                    completeness = round(int(n_obs)/int(n_full), 3)
                    cc_half = round(float(l_row[5].strip('%'))/100, 3)
                    r_split = round(float(l_row[10].strip('%'))/100, 3)
                    self.d_["reflns_shell"]["_reflns_shell.d_res_low"].append(l_row[1])
                    self.d_["reflns_shell"]["_reflns_shell.d_res_high"].append(l_row[3])
                    self.d_["reflns_shell"]["_reflns_shell.number_unique_obs"].append(n_obs)
                    self.d_["reflns_shell"]["_reflns_shell.percent_possible_obs"].append(str(completeness))
                    self.d_["reflns_shell"]["_reflns_shell.pdbx_CC_half"].append(str(cc_half))
                    self.d_["reflns_shell"]["_reflns_shell.pdbx_R_split"].append(str(r_split))
                except Exception as e:
                    logger.warning("Log file line #%s, cannot parse shell stats in Table of Scaling Results wth error %s",i,e)
        return True

    def parseMerge(self):
        """
        Parse Intensity Statistics (all accepted experiments) and add into class dict

        Returns
        -------
        True: Parse OK
        False: Parse failed

        """
        pattern = r"^\s*Intensity Statistics \(all accepted experiments\)"
        i_start = getStartingIndex(self.l_file, pattern)
        if i_start < 0:
            logger.warning("cannot find Intensity Statistics (all accepted experiments), stop")
            return False        
        logger.info("find Intensity Statistics (all accepted experiments) from line index %s", i_start)


        i_start_value = -1  # set line index where the value starts
        re_line_of_attr = re.compile(r'^\s*Bin\s+')
        for i in range(i_start, i_start+15):
            line = self.l_file[i]
            if re_line_of_attr.search(line):
                i_start_value = i+2
                logger.info("find table header from line index %s", i_start_value)
                break
        if i_start_value < 0:
            logger.warning("cannot find value in Intensity Statistics (all accepted experiments), stop")
            return False

        i_overall_value = -1  # set line index for all reflection values
        re_overall_value = re.compile(r'^\s*All\s+') 
        for i in range(i_start_value, i_start_value+60):
            line = self.l_file[i]               
            if re_overall_value.search(line):
                i_overall_value = i
                break
        if i_overall_value < 0:
            logger.warning("cannot find overall value in Intensity Statistics (all accepted experiments), stop")
            return False

        # process overall stats
        l_row_overall = self.l_file[i_overall_value].strip().split()
        logger.info("parse overall merge stats into %s", l_row_overall)
        if len(l_row_overall) == 12:
            # self.d_["reflns"]["_reflns.percent_possible_obs"].append(l_row_overall[2])
            self.d_["reflns"]["_reflns.pdbx_redundancy"].append(l_row_overall[3])
            self.d_["reflns"]["_reflns.pdbx_number_measured_all"].append(l_row_overall[5])
            self.d_["reflns"]["_reflns.number_all"].append(l_row_overall[6])
            self.d_["reflns"]["_reflns.pdbx_netI_over_sigmaI"].append(l_row_overall[8])

        # process shells
        for i in range(i_start_value, i_overall_value):
            l_row = self.l_file[i].strip().split()
            if len(l_row) == 15:
                self.d_["reflns_shell"]["_reflns_shell.pdbx_redundancy"].append(l_row[6])
                self.d_["reflns_shell"]["_reflns_shell.number_measured_all"].append(l_row[8])
                self.d_["reflns_shell"]["_reflns_shell.number_unique_all"].append(l_row[9])
                self.d_["reflns_shell"]["_reflns_shell.pdbx_netI_over_sigmaI_obs"].append(l_row[11])
        return True

    def orderShell(self):
        """
        order shell from high to low resolution

        Returns
        -------
        True: re-order OK
        False: re-order failed, something must be wrong with the log

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
                return False
        return True

    def parseLowResolution(self):
        """find overall low resolution from the log

        Returns:
            low_res_overall: str
        """        
        re_ = re.compile(r"^\s*\d+\s+indices\: An asymmetric unit in the resolution interval\s+(\d+\.*\d*)\s+\-\s+\d+\.*\d*\s+Angstrom")
        low_res_overall = -1
        for line in self.l_file:
            if re_.search(line):
                low_res_overall = re_.search(line).groups()[0]
                logger.info("find overall low resolution of %s", low_res_overall )
        return low_res_overall

    def verifyData(self):
        """
        Verify number of values for each row and remove empty row

        Returns
        -------
        None.

        """
        d_clean = {}
        for cat, d_cat in self.d_.items():
            if self.verifySameNumOfValuesPerRow(d_cat):
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

    def parseWavelength(self):
        """find wavelength if present
        """        
        re_ = re.compile(r"^\s*Wavelength\:\s+(\d+\.\d+)")
        wavelength = -1
        try:
            for line in self.l_file:
                if re_.search(line):
                    wavelength = re_.search(line).groups()[0]
                    logger.info("find wavelength of %s", wavelength)
            if float(wavelength) > 0:
                self.d_["diffrn_source"] = {}
                self.d_["diffrn_source"]["_diffrn_source.diffrn_id"] = ['1']
                self.d_["diffrn_source"]["_diffrn_source.pdbx_wavelength_list"] = [wavelength]
        except Exception as e:
            logger.warning("Fail to parse wavelength with error '%s'", e)

    def parseLattices(self):
        """
        Parse number of lattices

        Returns
        -------
        bool
            True if parse OK
            False if parse failed

        """
        pattern = r"^\s*Image Statistics"
        i_start = getStartingIndex(self.l_file, pattern)
        logger.info("find Image Statistics from line index %s", i_start)
        if i_start < 0:
            return False

        i_start_value = -1  # set line index where the value starts
        re_line_of_attr = re.compile(r'^\s*Bin\s+')
        for i in range(i_start, i_start+15):
            line = self.l_file[i]
            if re_line_of_attr.search(line):
                i_start_value = i+2
                logger.info("find table header from line index %s", i_start_value)
                break
        if i_start_value < 0:
            return False
        
        i_overall_value = -1  # set line index for all reflection values
        re_overall_value = re.compile(r'^\s*All\s+') 
        for i in range(i_start_value, i_start_value+60):
            line = self.l_file[i]               
            if re_overall_value.search(line):
                i_overall_value = i
                break
        if i_overall_value < 0:
            return False
        
        # process overall stats
        l_row_overall = self.l_file[i_overall_value].strip().split()
        logger.info("parse overall scaling stats into %s", l_row_overall)
        if len(l_row_overall) == 2:
            n_lattices = l_row_overall[1]
            self.d_["pdbx_serial_crystallography_data_reduction"] = {}
            self.d_["pdbx_serial_crystallography_data_reduction"]["_pdbx_serial_crystallography_data_reduction.diffrn_id"] = ['1']
            self.d_["pdbx_serial_crystallography_data_reduction"]["_pdbx_serial_crystallography_data_reduction.lattices_merged"] = [str(n_lattices)]
