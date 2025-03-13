#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2025-03-12
# Updates:
#
# =============================================================================
"""
Unit test for splitMetadata.py
"""
import os
import sys
import unittest
import filecmp

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, TOP_DIR)

from extract.process_model.splitMetadata import Spliter


class TestSplit(unittest.TestCase):
    def setUp(self):
        self.test_data = os.path.join(TOP_DIR, "tests/test_data")

    def tearDown(self):
        pass
    
    def test1(self):
        filepath_model = os.path.join(self.test_data, "PDB_Template_Scalepack_1", "pdb_extract_out_full.cif")
        filepath_cat = os.path.join(self.test_data, "Templates", "xray_metadata_cat.list")
        spliter = Spliter()
        self.assertTrue(spliter.splitMetadata(filepath_model, filepath_cat))

        folder_temp = os.path.join(self.test_data, "temp")
        if not os.path.isdir(folder_temp):
            os.makedirs(folder_temp)
        fp_metadata = os.path.join(folder_temp, "metadata.cif")
        spliter.writeMetadata(fp_metadata)


if __name__ == "__main__":
    unittest.main()
