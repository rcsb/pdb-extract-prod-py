#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2023-12-01
# Updates:
#
# =============================================================================
"""
Extract scaling statistics from CrystFEL log fille
"""
import re
import logging

from extract.util.findPattern import getStartingIndex
from extract.extract_log.XRAY.scaling import LogScaling  # initiate class data dictionary

logger = logging.getLogger(__name__)


class LogCrystfel(LogScaling):  # parent class in parent folder's __init__.py
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
        """parse CrystFEL log file

        Args:
            filepath (_type_): CrystFEL log file path

        Returns:
            True: parse OK
            False: parse failed

        Outcomes: class dict self.d_
            self.d_["reflns"] to record reflection statistics
            self.d_["reflns_shell"] to record reflection shell statistics
            also added wavelength, number of lattices, and xfel marker
        """
        logger.info("start reading CrystFEL log file at %s", filepath)
        try:
            with open(filepath, 'r', errors='ignore') as file:
                self.l_file = file.read().splitlines() #read file into a list
        except IOError as e:
            logger.exception("fail to read CrystFEL log file at %s with error %s", filepath, e)
            return False

        logger.info("start to parse overall stats")
        self.parseOverall()
        
        logger.info("look for measurment table")
        d_cat1 = self.parseMeasurement()

        logger.info("look for CC1/2 table")
        d_cat2 = self.parseCchalf()

        logger.info("look for Rsplit table")
        d_cat3 = self.parseRsplit()

        logger.info("merge all tables based on resolution shell")
        d_cat = self.combineCat(d_cat1, d_cat2)
        d_cat = self.combineCat(d_cat, d_cat3)
        for item in d_cat:
            self.d_["reflns_shell"][item] = d_cat[item]
 
        if not self.orderShell():  # order shell from high resolution to low
            return False  # a re-order failure means format change, stop
        
        # process overall  high and low resolution
        if self.d_["reflns_shell"]["_reflns_shell.d_res_high"] and self.d_["reflns_shell"]["_reflns_shell.d_res_low"]:
            self.d_["reflns"]["_reflns.d_resolution_high"].append(self.d_["reflns_shell"]["_reflns_shell.d_res_high"][0])
            self.d_["reflns"]["_reflns.d_resolution_low"].append(self.d_["reflns_shell"]["_reflns_shell.d_res_low"][-1])
        else:
            t_resolution = self.parseResolution() # find overall low and high resolution if present
            if t_resolution and len(t_resolution) == 2:
                self.d_["reflns"]["_reflns.d_resolution_low"].append(t_resolution[0])
                self.d_["reflns"]["_reflns.d_resolution_high"].append(t_resolution[1])

        # process number of reflections
        if not self.d_["reflns"]["_reflns.number_obs"]:
            if self.d_["reflns_shell"]["_reflns_shell.percent_possible_obs"]:
                n_obs = self.addAll(self.d_["reflns_shell"]["_reflns_shell.percent_possible_obs"])
                if n_obs:
                    self.d_["reflns"]["_reflns.number_obs"].append(str(n_obs))
        if not self.d_["reflns"]["_reflns.pdbx_number_measured_all"]:
            if self.d_["reflns_shell"]["_reflns_shell.number_measured_all"]:
                n_all = self.addAll(self.d_["reflns_shell"]["_reflns_shell.number_measured_all"])
                if n_all:
                    self.d_["reflns"]["_reflns.pdbx_number_measured_all"].append(str(n_all))  

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

        logger.info("start to parse number of crystals")
        self.parseCrystals()

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
    
    def parseOverall(self):
        """parse overall stats from log for self.d_[]["reflns"]
        """        
        d_re = {}
        d_re["_reflns.pdbx_CC_half"] = re.compile(r'^\s*Overall CC \=\s*(\d+\.\d+)')
        d_re["_reflns.pdbx_R_split"] = re.compile(r'^\s*Overall Rsplit \=\s*(\d+\.\d+)\s*\%')
        d_re["_reflns.pdbx_redundancy"] = re.compile(r'^\s*Overall redundancy \=\s*(\d+\.\d+)')
        d_re["_reflns.percent_possible_obs"] = re.compile(r'^\s*Overall completeness \=\s*(\d+\.\d+)\s*\%')
        d_re["_reflns.number_obs"] = re.compile(r'^\s*(\d+)\s+reflections in total')
        d_re["_reflns.pdbx_number_measured_all"] = re.compile(r'^\s*(\d+)\s+measurements in total')

        d_scale = {}
        d_scale["_reflns.pdbx_CC_half"] = None
        d_scale["_reflns.pdbx_R_split"] = 0.01
        d_scale["_reflns.pdbx_redundancy"] = None
        d_scale["_reflns.percent_possible_obs"] = None
        d_scale["_reflns.number_obs"] = None
        d_scale["_reflns.pdbx_number_measured_all"] = None        

        for item, re_ in d_re.items():
            for line in reversed(self.l_file):
                if re_.search(line):
                    value = re_.search(line).groups()[0]
                    if d_scale[item]:
                        value = str(round((float(value)*d_scale[item]), 4))
                    self.d_["reflns"][item].append(value)
                    logger.info("found overall %s of %s", item, value)
                    break
            else:
                logger.info("cannot find overall %s", item)

    def parseMeasurement(self):
        """
        Parse completeness and redundancy into calss dictionay

        """
        self.table_header = r"^\s*Center 1\/nm\s+\# refs\s+Possible\s+Compl\s+Meas\s+Red\s+SNR\s+Mean I\s+d\(A\)\s+Min 1\/nm\s+Max 1\/nm"
        self.n_value = 11
        self.col_low_res_reciprocal = 10
        self.col_high_res_reciprocal = 11

        self.d_column = {}
        self.d_column["_reflns_shell.number_unique_obs"] = 2
        self.d_column["_reflns_shell.percent_possible_obs"] = 4
        self.d_column["_reflns_shell.number_measured_all"] = 5
        self.d_column["_reflns_shell.pdbx_redundancy"] = 6

        self.d_scale = {}
        self.d_scale["_reflns_shell.number_unique_obs"] = None
        self.d_scale["_reflns_shell.percent_possible_obs"] = None
        self.d_scale["_reflns_shell.number_measured_all"] = None
        self.d_scale["_reflns_shell.pdbx_redundancy"] = None

        d_cat = self.parseTable()
        return d_cat

    def parseCchalf(self):
        """
        Parse CC1/2 into class dictionary

        """
        self.table_header = r"^\s*1/d centre\s+CC\s+nref\s+d / A\s+Min 1/nm\s+Max 1/nm"
        self.n_value = 6
        self.col_low_res_reciprocal = 5
        self.col_high_res_reciprocal = 6

        self.d_column = {}
        self.d_column["_reflns_shell.number_unique_obs"] = 3
        self.d_column["_reflns_shell.pdbx_CC_half"] = 2

        self.d_scale = {}
        self.d_scale["_reflns_shell.number_unique_obs"] = None
        self.d_scale["_reflns_shell.pdbx_CC_half"] = None

        d_cat = self.parseTable()
        return d_cat

    def parseRsplit(self):
        """
        Parse R split into calss dictionay

        """
        self.table_header = r"^\s*1/d centre\s+Rsplit\/\%\s+nref\s+d / A\s+Min 1/nm\s+Max 1/nm"
        self.n_value = 6
        self.col_low_res_reciprocal = 5
        self.col_high_res_reciprocal = 6

        self.d_column = {}
        self.d_column["_reflns_shell.number_unique_obs"] = 3
        self.d_column["_reflns_shell.pdbx_R_split"] = 2

        self.d_scale = {}
        self.d_scale["_reflns_shell.number_unique_obs"] = None
        self.d_scale["_reflns_shell.pdbx_R_split"] = 0.01

        d_cat = self.parseTable()
        return d_cat
    
    def parseTable(self):
        """ parse CrystaFel stats table

        Returns:
            dict: table stats in a dictionary
        """        
        i_start = getStartingIndex(self.l_file, self.table_header)
        if i_start < 0:
            logger.warning("cannot find table header %s, stop", self.table_header)
            return False
        logger.info("find table from line %s", i_start+1)
        
        re_char = re.compile(r'[a-zA-Z]')
        i_table_start = i_start + 1
        for i in range(i_table_start, len(self.l_file)):
            line = self.l_file[i]
            if re_char.search(line):
                i_table_end = i - 1 
                break  # stop if the row is not number-only
        else:
            i_table_end = len(self.l_file) - 1
        logger.info("find table value starts in line %s and ends in line %s", i_table_start+1, i_table_end+1)

        d_cat = {}
        l_item = ["_reflns_shell.d_res_low", "_reflns_shell.d_res_high"]
        l_item.extend(list(self.d_column.keys()))
        for item in l_item:
            d_cat[item] = []

        for i in range(i_table_start, i_table_end+1):
            line = self.l_file[i]
            l_row = line.strip().split()
            if len(l_row) == self.n_value:
                try:
                    low_res = round(10/float(l_row[self.col_low_res_reciprocal-1]), 2)
                    high_res = round(10/float(l_row[self.col_high_res_reciprocal-1]), 2)
                    d_cat["_reflns_shell.d_res_low"].append(str(low_res))
                    d_cat["_reflns_shell.d_res_high"].append(str(high_res))

                    for item, col in self.d_column.items():
                        raw = l_row[col-1]
                        if self.d_scale[item]:
                            value = str(round(float(raw)*self.d_scale[item],4))
                        else:
                            value = raw
                        d_cat[item].append(value)
                except Exception as e:
                    logger.warning("Log file line #%s, cannot parse stats wth error %s",i+1,e)
                    return {}
        return d_cat
    
    def combineCat(self, d_cat1, d_cat2):
        if not d_cat1:
            return d_cat2
        if not d_cat2:
            return d_cat1
        if "_reflns_shell.d_res_high" not in d_cat1 or "_reflns_shell.d_res_low" not in d_cat1:
            return d_cat2
        if "_reflns_shell.d_res_high" not in d_cat2 or "_reflns_shell.d_res_low" not in d_cat2:
            return d_cat1
        if d_cat1["_reflns_shell.d_res_high"] != d_cat2["_reflns_shell.d_res_high"]:
            return d_cat1  # if two dict have different shell high, drop d_cat2
        if d_cat1["_reflns_shell.d_res_low"] != d_cat2["_reflns_shell.d_res_low"]:
            return d_cat1  # if two dict have different shell low, drop d_cat2

        d_merge = {}
        for key1 in d_cat1:
            d_merge[key1] = d_cat1[key1]
        for key2 in d_cat2:
            if key2 not in d_merge:
                d_merge[key2] = d_cat2[key2]
        return d_merge

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

    def parseResolution(self):
        """find overall resolution from the log
        """       
        re_ = re.compile(r"resolution range\s+(\d+\.*\d*)\s+to\s+(\d+\.*\d*)\s+Angstroms")
        for line in reversed(self.l_file):
            if re_.search(line):
                [low, high] = re_.search(line).groups()
                return(low, high)
        return ()

    def addAll(self, l_):
        try:
            sum = 0
            for each in l_:
                sum += int(each)
            return sum
        except ValueError:
            logger.warning("addAll list components has non-numberic values")
            return None

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
                for item, value in d_cat.items():
                    if len(value) != 0:  # only if row is not an emtpy list
                        d_clean[cat][item] = value
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

    def parseCrystals(self):
        """
        Parse number of crystals hit

        Returns
        -------
        bool
            True if parse OK
            False if parse failed

        """
        re_ = re.compile("(\d+) crystals")
        n = 0
        for line in reversed(self.l_file):
            if re_.search(line):
                n = re_.search(line).groups()[0]
                break
        if n:
            self.d_["pdbx_serial_crystallography_data_reduction"] = {}
            self.d_["pdbx_serial_crystallography_data_reduction"]["_pdbx_serial_crystallography_data_reduction.diffrn_id"] = ['1']
            self.d_["pdbx_serial_crystallography_data_reduction"]["_pdbx_serial_crystallography_data_reduction.crystal_hits"] = [str(n)]
