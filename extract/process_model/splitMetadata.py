#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2025-03-12
# Updates:
# =============================================================================
"""
Split metadata contents from the processed file
The metadata is then written to a template
Only work on the 1st data block
"""
import os
import json

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mmcif.io.IoAdapterCore import IoAdapterCore

import logging
logger_name = '.'.join(["PDB_EX", __name__])
logger = logging.getLogger(logger_name)


class Spliter():
    """ Class to merge log data and template data into converted model file
    """

    def __init__(self):
        self.l_dc = None  # container list for model file
        self.dc0 = None  # container for the 1st data section of model file
        self.l_cat_kept = []

    def readModel(self, filepath_model):
        """
        Read model file data into class variables

        Parameters
        ----------
        filepath_model : str
            filepath of converted model file after running maxit.

        Returns
        -------
            boolean: success or failure

        """
        try:
            self.io = IoAdapterCore()
            logger.debug("to split metadata on converted file at %s" % filepath_model)
            try:
                self.l_dc = self.io.readFile(filepath_model)
                self.dc0 = self.l_dc[0]
                logger.info("Read converted model file into Spliter")
                return True
            except Exception as e:
                logger.exception(e)
                return False
        except IOError as e:
            logger.exception(e)
            return False
        
    def readMetadataCatList(self, filepath_cat):
        """
        Read the category list 

        Parameters
        ----------
        filepath_model : str
            filepath of list of categroies to keep.

        Returns
        -------
        l_cat : list
            list of metadata categories to be kept.

        """
        try:
            l_cat = []
            with open(filepath_cat) as file:
                for line in file:
                    if line.strip():
                        if line.strip().startswith("#"):
                            pass
                        else:
                            l_cat.append(line.strip())
            return l_cat
        except IOError as e:
            logger.exception(e)
            return []

    def splitMetadata(self, filepath_model, filepath_cat):
        """split metadata data contents from filepath_model based on the category list in filepath_cat

        Args:
            filepath_model (str): filepath of the model
            filepath_cat (str): filepath of the category list

        Returns:
            boolean: success or failure

        """        
        if not self.readModel(filepath_model):
            return False
        l_cat_to_keep = self.readMetadataCatList(filepath_cat)
        if not l_cat_to_keep:
            return False
        
        l_cat = []  # must create a separate list to go though during deletion
        for each in self.dc0.getObjNameList():
            l_cat.append(each)

        try:
            for cat in l_cat:  # cannot use "for cat_name in self.dc0.getObjNameList() because of deletion will mess up iteration"
                if cat in l_cat_to_keep:
                    self.l_cat_kept.append(cat)
                else:
                    self.dc0.remove(cat)
            if self.l_cat_kept:
                logger.info("split metadata categories of %s", self.l_cat_kept)
                return True
            else:
                logger.warning("no common metadata categories have been found in the result file, continue without writting metadata.cif")
                return False
        except Exception as e:
            logger.error(e)
            return False

    def writeMetadata(self, filepath_metadata):
        """
        Write the to-be-kept metadata cateories into a template file

        Parameters
        ----------
        filepath_out : str
            output filepath for the template

        Returns
        -------
        None.

        """
        try:
            self.io.writeFile(filepath_metadata, [self.dc0])
        except IOError as e:
            logger.exception(e)
