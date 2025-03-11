#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-20
# Updates:
#
# =============================================================================
"""
Unit test for cifDictCheck.py
"""
import os
import sys
import unittest

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, TOP_DIR)

from extract.util.cifDictCheck import DictCheck


class TestCheck(unittest.TestCase):
    def setUp(self):
        filepath_dict = os.path.join(TOP_DIR,
                                     "data/dictionary/mmcif_pdbx_v5_next.dic")
        self.dict = DictCheck(filepath_dict)
        self.folder = os.path.join(TOP_DIR, "tests/test_data/CIF4test")

    def tearDown(self):
        pass

    def testGood(self):
        filename = "maxit_out.cif"
        filepath = os.path.join(self.folder, filename)
        self.dict.readModelCif(filepath)
        self.dict.check()
        print("test good example")
        print("")
        self.assertEqual(self.dict.l_cat_not_in_dict, [])
        self.assertEqual(self.dict.l_item_not_in_dict, [])
        self.assertEqual(self.dict.d_value_failRE, {})
        self.assertEqual(self.dict.d_value_failEnum, {})
        self.assertEqual(self.dict.d_value_failBoundary, {})

    def testWrongCat(self):
        filename = "wrong_cat_name.cif"
        filepath = os.path.join(self.folder, filename)
        self.dict.readModelCif(filepath)
        self.dict.check()
        print("test category name not in dictionary")
        print(self.dict.l_cat_not_in_dict)
        print("")
        self.assertFalse(self.dict.l_cat_not_in_dict==[])

    def testWrongItem(self):
        filename = "wrong_item_name.cif"
        filepath = os.path.join(self.folder, filename)
        self.dict.readModelCif(filepath)
        self.dict.check()
        print("test item name not in dictionary")
        print(self.dict.l_item_not_in_dict)
        print("")
        self.assertFalse(self.dict.l_item_not_in_dict==[])

    def testWrongValueType(self):
        filename = "wrong_value_type.cif"
        filepath = os.path.join(self.folder, filename)
        self.dict.readModelCif(filepath)
        self.dict.check()
        print("test value in wrong type")
        print(self.dict.d_value_failRE)
        print("")
        self.assertFalse(self.dict.d_value_failRE=={})

    def testValueNotInEnum(self):
        filename = "value_not_in_enum.cif"
        filepath = os.path.join(self.folder, filename)
        self.dict.readModelCif(filepath)
        self.dict.check()
        print("test value not in enum")
        print(self.dict.d_value_failEnum)
        print("")
        self.assertFalse(self.dict.d_value_failEnum=={})

    def testValueOutBound(self):
        filename = "value_outof_bound.cif"
        filepath = os.path.join(self.folder, filename)
        self.dict.readModelCif(filepath)
        self.dict.check()
        print("test value out of bound")
        print(self.dict.d_value_failBoundary)
        print("")
        self.assertFalse(self.dict.d_value_failBoundary=={})

    def testGetMandatoryAttrByCat(self):
        l_mandatory = self.dict.getMandatoryAttrByCat("em_imaging")
        self.assertEqual(l_mandatory, ['accelerating_voltage', 'electron_source', 'entry_id', 'id', 
                                       'illumination_mode', 'microscope_model', 'mode', 'specimen_id'])


    def testCheckMandatoryItemMissingValue(self):
        filename = "maxit_out.cif"
        filepath = os.path.join(self.folder, filename)
        self.dict.readModelCif(filepath)
        self.dict.check(l_mandatory_cat=["refine"])
        print("test good example")
        print("")
        self.assertTrue('_refine.pdbx_ls_cross_valid_method' in self.dict.l_mandatory_item_missing_value)

if __name__ == "__main__":
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestCheck("testGood"))
    test_suite.addTest(TestCheck("testWrongCat"))
    test_suite.addTest(TestCheck("testWrongItem"))
    test_suite.addTest(TestCheck("testWrongValueType"))
    test_suite.addTest(TestCheck("testValueNotInEnum"))
    test_suite.addTest(TestCheck("testValueOutBound"))
    test_suite.addTest(TestCheck("testGetMandatoryAttrByCat"))
    test_suite.addTest(TestCheck("testCheckMandatoryItemMissingValue"))
    unittest.TextTestRunner(verbosity=2).run(test_suite)
