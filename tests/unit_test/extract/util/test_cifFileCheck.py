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

from extract.util.cifFileCheck import Check


class TestCheck(unittest.TestCase):
    def setUp(self):
        self.folder = os.path.join(TOP_DIR, "tests/test_data/CIF4test")

    def tearDown(self):
        pass

    def testGood(self):
        filename = "D_1000267334_model-upload_P1.cif.V1"
        filepath = os.path.join(self.folder, filename)
        checker = Check(filepath)
        self.assertTrue(checker.checkFormat())
        self.assertTrue(checker.checkMandatoryCat())

    def testIncomplete(self):
        filename = "incomplete_categories.cif"
        filepath = os.path.join(self.folder, filename)
        checker = Check(filepath)
        self.assertTrue(checker.checkFormat())
        self.assertFalse(checker.checkMandatoryCat())

    def testMissingHeader(self):
        filename = "missing_header.cif"
        filepath = os.path.join(self.folder, filename)
        checker = Check(filepath)
        self.assertFalse(checker.checkHeader(filepath))

    def testUppercaseHeader(self):
        filename = "uppercase_header.cif"
        filepath = os.path.join(self.folder, filename)
        checker = Check(filepath)
        self.assertFalse(checker.checkHeader(filepath))

    def testWrongHeader(self):
        filename = "wrong_header.cif"
        filepath = os.path.join(self.folder, filename)
        checker = Check(filepath)
        self.assertFalse(checker.checkHeader(filepath))


if __name__ == "__main__":
    unittest.main()
