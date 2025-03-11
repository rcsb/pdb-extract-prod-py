#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-20
# Updates:
#
# =============================================================================
"""
Unit test for pdb_extract full command runs on authors' data
"""
import os
import sys
import unittest

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, TOP_DIR)

from bin.pdb_extract import runPdbExtract
from extract.process_model.validateCifModel import validateCif


class TestPdbExtract(unittest.TestCase):
    def setUp(self):
        self.test_data  = os.path.join(TOP_DIR, "tests/test_data")
        
    def tearDown(self):
        pass
    
    def test1(self):
        test_run_folder = os.path.join(self.test_data, "PDB_Template_Scalepack_1")
        os.chdir(test_run_folder)
        args = "-iPDB %s -r CNS -s Scalepack %s -iENT %s -o testout.cif" % \
            ("deposited_XRAY.pdb", "scalepack_log", "template_new_XRAY.cif")
        runPdbExtract(args)
        self.assertTrue(os.path.isfile("testout.cif"))
        self.assertTrue(os.path.isfile("dictionary_check.json"))
        self.assertTrue(validateCif("testout.cif"))
        try:
            os.remove("testout.cif")
        except FileNotFoundError:
            pass
        try:
            os.remove("dictionary_check.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("pdb_extract.log")
        except FileNotFoundError:
            pass
        try:
            os.remove("maxit_out.cif")
        except FileNotFoundError:
            pass

    def test2(self):
        test_run_folder = os.path.join(self.test_data, "PDB_XDS_Aimless_Phaser_Phenix_2021_10_8_18_16442")
        os.chdir(test_run_folder)
        args = "-iPDB %s -r Phenix -i XDS %s -s Aimless %s -o testout.cif" % \
            ("deposited_XRAY.pdb", "file_index_1", "file_scl_1")
        runPdbExtract(args)
        self.assertTrue(os.path.isfile("testout.cif"))
        self.assertTrue(os.path.isfile("dictionary_check.json"))
        self.assertTrue(validateCif("testout.cif"))        
        try:
            os.remove("testout.cif")
        except FileNotFoundError:
            pass
        try:
            os.remove("dictionary_check.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("pdb_extract.log")
        except FileNotFoundError:
            pass
        try:
            os.remove("maxit_out.cif")
        except FileNotFoundError:
            pass

    def test3(self):
        test_run_folder = os.path.join(self.test_data, "PDB_HKL2000_Phaser_Refmac_2021_9_28_13_26368")
        os.chdir(test_run_folder)
        args = "-iPDB %s -r Refmac -i HKL-2000 %s -s HKL-2000 %s -m Phaser -o testout.cif" % \
            ("deposited_XRAY.pdb", "file_index_1", "file_scl_1")
        runPdbExtract(args)
        self.assertTrue(os.path.isfile("testout.cif"))
        self.assertTrue(os.path.isfile("dictionary_check.json"))
        self.assertTrue(validateCif("testout.cif"))        
        try:
            os.remove("testout.cif")
        except FileNotFoundError:
            pass
        try:
            os.remove("dictionary_check.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("pdb_extract.log")
        except FileNotFoundError:
            pass
        try:
            os.remove("maxit_out.cif")
        except FileNotFoundError:
            pass

    def test4(self):
        test_run_folder = os.path.join(self.test_data, "PDB_Xscale_Phaser_Buster_2021_10_15_16_9523")
        os.chdir(test_run_folder)
        args = "-iPDB %s -r Buster -s Xscale %s -m Phaser -o testout.cif" % \
            ("deposited_XRAY.pdb", "file_scl_1")
        runPdbExtract(args)
        self.assertTrue(os.path.isfile("testout.cif"))
        self.assertTrue(os.path.isfile("dictionary_check.json"))
        self.assertTrue(validateCif("testout.cif"))        
        try:
            os.remove("testout.cif")
        except FileNotFoundError:
            pass
        try:
            os.remove("dictionary_check.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("pdb_extract.log")
        except FileNotFoundError:
            pass
        try:
            os.remove("maxit_out.cif")
        except FileNotFoundError:
            pass

    def test5(self):
        test_run_folder = os.path.join(self.test_data, "CIF_phenix_D_1000267334")
        os.chdir(test_run_folder)
        args = "-iCIF %s -r phenix -o testout.cif" % \
            ("D_1000267334_model-upload_P1.cif.V1")
        runPdbExtract(args)
        self.assertTrue(os.path.isfile("testout.cif"))
        self.assertTrue(os.path.isfile("dictionary_check.json"))
        self.assertTrue(validateCif("testout.cif"))
        try:
            os.remove("testout.cif")
        except FileNotFoundError:
            pass
        try:
            os.remove("dictionary_check.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("pdb_extract.log")
        except FileNotFoundError:
            pass
        try:
            os.remove("maxit_out.cif")
        except FileNotFoundError:
            pass

    def testEM1(self):
        test_run_folder = os.path.join(self.test_data, "EM_Phenix_2023_2_13_13_11_1069")
        os.chdir(test_run_folder)
        args = "-EM -iPDB %s -iENT %s -o testout.cif" % ("deposited_EM.pdb", "template_new_EM_with_software.cif")
        runPdbExtract(args)
        self.assertTrue(os.path.isfile("testout.cif"))
        self.assertTrue(os.path.isfile("dictionary_check.json"))
        self.assertTrue(validateCif("testout.cif"))
        try:
            os.remove("testout.cif")
        except FileNotFoundError:
            pass
        try:
            os.remove("dictionary_check.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("pdb_extract.log")
        except FileNotFoundError:
            pass
        try:
            os.remove("maxit_out.cif")
        except FileNotFoundError:
            pass

    def testNMR1(self):
        test_run_folder = os.path.join(self.test_data, "NMR_2023_2_3_0_47_17090")
        os.chdir(test_run_folder)
        args = "-NMR -iPDB %s -iENT %s -o testout.cif" % ("deposited_NMR.pdb", "data_template_nmr.cif")
        runPdbExtract(args)
        self.assertTrue(os.path.isfile("testout.cif"))
        self.assertTrue(os.path.isfile("dictionary_check.json"))
        self.assertTrue(validateCif("testout.cif"))
        try:
            os.remove("testout.cif")
        except FileNotFoundError:
            pass
        try:
            os.remove("dictionary_check.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("pdb_extract.log")
        except FileNotFoundError:
            pass
        try:
            os.remove("maxit_out.cif")
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestPdbExtract("test1"))
    test_suite.addTest(TestPdbExtract("test2"))
    test_suite.addTest(TestPdbExtract("test3"))
    test_suite.addTest(TestPdbExtract("test4"))
    test_suite.addTest(TestPdbExtract("test5"))
    test_suite.addTest(TestPdbExtract("testEM1"))
    test_suite.addTest(TestPdbExtract("testNMR1"))
    unittest.TextTestRunner(verbosity=2).run(test_suite)
