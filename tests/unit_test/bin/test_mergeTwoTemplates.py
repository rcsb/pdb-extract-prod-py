#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2023-02-06
# Updates:
#
# =============================================================================
"""
Unit test for mergeTwoTemplates.py
"""

import os
import sys
import unittest
import filecmp

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, TOP_DIR)

from bin.mergeTwoTemplates import mergeTwoTemplates

class TestMerge(unittest.TestCase):
    def setUp(self):
        self.test_data  = os.path.join(TOP_DIR, "tests/test_data")

    def tearDown(self):
        pass

    def testMerge(self):
        folder = os.path.join(self.test_data, "PDB_Template_Scalepack_1")
        filename_template_1 = "template_new_XRAY.cif"
        filename_template_2 = "entity_poly.cif"
        filename_out = "template_merged.cif"
        filename_ref = "data_template_entity_poly"
        filepath_template_1 = os.path.join(folder, filename_template_1)
        filepath_template_2 = os.path.join(folder, filename_template_2)
        filepath_out = os.path.join(folder, filename_out)
        filepath_ref = os.path.join(folder, filename_ref)
        l_cat_to_merge = ["entity_poly"]
        mergeTwoTemplates(filepath_template_1, filepath_template_2, filepath_out, l_cat_to_merge)

        self.assertTrue(os.path.isfile(filepath_out))
        self.assertTrue(filecmp.cmp(filepath_out, filepath_ref))

        try:
            os.remove(filepath_out)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    unittest.main()
