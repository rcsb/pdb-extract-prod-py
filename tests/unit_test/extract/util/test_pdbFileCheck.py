#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-20
# Updates:
#
# =============================================================================
"""
Unit test for cifCheck.py
"""
import os
import sys
import unittest

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, TOP_DIR)

from extract.util.pdbFileCheck import Check


class TestCheck(unittest.TestCase):
    def setUp(self):
        self.folder = os.path.join(TOP_DIR, "tests/test_data/PDB4test")
        
    def tearDown(self):
        pass
        
    def testGood(self):
        filename = "full_public.pdb"
        filepath = os.path.join(self.folder, filename)
        print(filepath)
        checker = Check(filepath)
        self.assertTrue(checker.checkFormat())

    def testMinimal(self):
        filename = "minimal.pdb"
        filepath = os.path.join(self.folder, filename)
        print(filepath)
        checker = Check(filepath)
        self.assertTrue(checker.checkFormat())

    def testCNSoutput(self):
        filename = "deposited_CNS_wo_REMARK3.pdb"
        filepath = os.path.join(self.folder, filename)
        print(filepath)
        checker = Check(filepath)
        self.assertTrue(checker.checkFormat())

    def testMissingCRYST1(self):
        filename = "missing_CRYST1.pdb"
        filepath = os.path.join(self.folder, filename)
        print(filepath)
        checker = Check(filepath)
        self.assertFalse(checker.checkCryst1())

    def testMissingATOM(self):
        filename = "missing_ATOM.pdb"
        filepath = os.path.join(self.folder, filename)
        print(filepath)
        checker = Check(filepath)
        self.assertFalse(checker.checkFormat())

    def testAtomWrongColumn(self):
        filename = "wrong_ATOM_chainIDinCol23.pdb"
        filepath = os.path.join(self.folder, filename)
        print(filepath)
        checker = Check(filepath)
        self.assertFalse(checker.checkFormat())


if __name__ == "__main__":
    unittest.main()
