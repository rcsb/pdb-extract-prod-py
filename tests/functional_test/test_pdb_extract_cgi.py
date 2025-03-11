#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-20
# Updates:
#
# =============================================================================
"""
Unit test for pdb_extract_cgi.py
"""
import os
import sys
import unittest

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, TOP_DIR)

from bin.pdb_extract_cgi import create_parser, parseArgs, processPdbModel, processCifModel, generateSummaryForCGI
from extract.process_model.validateCifModel import validateCif


class TestPdbExtract(unittest.TestCase):
    def setUp(self):
        self.test_data  = os.path.join(TOP_DIR, "tests/test_data")
        
    def tearDown(self):
        pass
    
    def test1(self):
        test_run_folder = os.path.join(self.test_data, "PDB_Template_Scalepack_1")
        os.chdir(test_run_folder)
        args_text = "-iPDB deposited_XRAY.pdb"
        parser = create_parser()
        args = parser.parse_args(args_text.split())
        (file_format, filepath_in, filepath_out) = parseArgs(args)
        if file_format == "PDB":
            filepath_maxit_out = "maxit_out.cif"
            if processPdbModel(filepath_in, filepath_maxit_out, filepath_out):
                generateSummaryForCGI(filepath_maxit_out)
        elif file_format == "CIF":
            if processCifModel(filepath_in, filepath_out):
                generateSummaryForCGI(filepath_out)
        self.assertTrue(os.path.isfile("pdb_extract_cgi_out.cif"))
        self.assertTrue(os.path.isfile("converted_summary.json"))
        try:
            os.remove("pdb_extract_cgi_out.cif")
        except FileNotFoundError:
            pass
        try:
            os.remove("converted_summary.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("pdb_extract_cgi.log")
        except FileNotFoundError:
            pass
        try:
            os.remove("maxit_out.cif")
        except FileNotFoundError:
            pass

    def test2(self):
        test_run_folder = os.path.join(self.test_data, "PDB_XDS_Aimless_Phaser_Phenix_2021_10_8_18_16442")
        os.chdir(test_run_folder)
        filepath_in = "deposited_XRAY.pdb"
        filepath_out = "pdb_extract_cgi_out.cif"
        filepath_maxit_out = "maxit_out.cif"
        if processPdbModel(filepath_in, filepath_maxit_out, filepath_out):
            generateSummaryForCGI(filepath_maxit_out)
        self.assertTrue(os.path.isfile("pdb_extract_cgi_out.cif"))
        self.assertTrue(os.path.isfile("converted_summary.json"))
        try:
            os.remove("pdb_extract_cgi_out.cif")
        except FileNotFoundError:
            pass
        try:
            os.remove("converted_summary.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("pdb_extract_cgi.log")
        except FileNotFoundError:
            pass
        try:
            os.remove("maxit_out.cif")
        except FileNotFoundError:
            pass

    def test3(self):
        test_run_folder = os.path.join(self.test_data, "PDB_HKL2000_Phaser_Refmac_2021_9_28_13_26368")
        os.chdir(test_run_folder)
        filepath_in = "deposited_XRAY.pdb"
        filepath_out = "pdb_extract_cgi_out.cif"
        filepath_maxit_out = "maxit_out.cif"
        if processPdbModel(filepath_in, filepath_maxit_out, filepath_out):
            generateSummaryForCGI(filepath_maxit_out)
        self.assertTrue(os.path.isfile("pdb_extract_cgi_out.cif"))
        self.assertTrue(os.path.isfile("converted_summary.json"))
        try:
            os.remove("pdb_extract_cgi_out.cif")
        except FileNotFoundError:
            pass
        try:
            os.remove("converted_summary.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("pdb_extract_cgi.log")
        except FileNotFoundError:
            pass
        try:
            os.remove("maxit_out.cif")
        except FileNotFoundError:
            pass

    def test4(self):
        test_run_folder = os.path.join(self.test_data, "PDB_Xscale_Phaser_Buster_2021_10_15_16_9523")
        os.chdir(test_run_folder)
        filepath_in = "deposited_XRAY.pdb"
        filepath_out = "pdb_extract_cgi_out.cif"
        filepath_maxit_out = "maxit_out.cif"
        if processPdbModel(filepath_in, filepath_maxit_out, filepath_out):
            generateSummaryForCGI(filepath_maxit_out)
        self.assertTrue(os.path.isfile("pdb_extract_cgi_out.cif"))
        self.assertTrue(os.path.isfile("converted_summary.json"))
        try:
            os.remove("pdb_extract_cgi_out.cif")
        except FileNotFoundError:
            pass
        try:
            os.remove("converted_summary.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("pdb_extract_cgi.log")
        except FileNotFoundError:
            pass
        try:
            os.remove("maxit_out.cif")
        except FileNotFoundError:
            pass

    def test5(self):
        test_run_folder = os.path.join(self.test_data, "CIF_phenix_D_1000267334")
        os.chdir(test_run_folder)
        filepath_in = "D_1000267334_model-upload_P1.cif.V1"
        filepath_out = "pdb_extract_cgi_out.cif"
        if processCifModel(filepath_in, filepath_out):
            generateSummaryForCGI(filepath_out)
        self.assertTrue(os.path.isfile("pdb_extract_cgi_out.cif"))
        self.assertTrue(os.path.isfile("converted_summary.json"))
        try:
            os.remove("pdb_extract_cgi_out.cif")
        except FileNotFoundError:
            pass
        try:
            os.remove("converted_summary.json")
        except FileNotFoundError:
            pass
        try:
            os.remove("pdb_extract_cgi.log")
        except FileNotFoundError:
            pass
        try:
            os.remove("maxit_out.cif")
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    unittest.main()  # all unit tests

    # # test 1
    # folder_test_data = os.path.join(TOP_DIR, "tests/test_data/PDB_Template_Scalepack_1")
    # filepath_pdb_input = os.path.join(folder_test_data, "deposited_XRAY.pdb")
    # parser = create_parser()
    # args_text = "-iPDB %s" % filepath_pdb_input
    # args = parser.parse_args(args_text.split())
    # (format, filepath_in) = parseArgs(args)
    # filepath_out = "pdb_extract_cgi_out.cif"
    # if processModel(format, filepath_in, filepath_out):
    #     generateSummaryForCGI(filepath_out)

    ## test 2
    # folder = "/Users/chenghua/Projects/pdb_extract/tests/test_data"
    # test_run_folder = os.path.join(folder, "PDB_XDS_Aimless_Phaser_Phenix_2021_10_8_18_16442")
    # os.chdir(test_run_folder)
    # args = "-iPDB %s -r Phenix -i XDS %s -s Aimless %s -o testout.cif" % \
    #     ("deposited_XRAY.pdb", "file_index_1", "file_scl_1")
    # args = "-iPDB %s -r Phenix -i XDS -s Aimless %s -o testout.cif" % \
    #     ("deposited_XRAY.pdb", "file_scl_1")
    # runPdbExtract(args)

