#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2023-02-01
# Updates:
#
# =============================================================================
"""
Unit test for mergeCats.py
"""
import os
import sys
import unittest

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, TOP_DIR)

from extract.util.mergeCats import mergeCatItemsUnionValuesByKeys, mergeCatItemsUpdateValuesByKeys, mergeCatItemsUpdateValuesByRowIndex


class TestMergeCats(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testmergeCatsUnionValuesByKeys1(self):
        d_to = {
            'key_item': ['key_value1', 'key_value2'],
            'item1': ['value11t', 'value12t'],
            'item2': ['value21t', 'value22t']
        }

        d_from = {
            'key_item': ['key_value1', 'key_value3'],
            'item1': ['value11f', 'value12f'],
            'item3': ['value31f', 'value32f']
        }

        d_combine = mergeCatItemsUnionValuesByKeys(d_to, d_from, ["key_item"])

        d_combine_ref = {
            'key_item': ['key_value1', 'key_value2', 'key_value3'],
            'item1': ['value11t', 'value12t', 'value12f'],
            'item2': ['value21t', 'value22t', '?'],
            'item3': ['value31f', '?',        'value32f']
        }

        self.assertEqual(d_combine, d_combine_ref)

    def testmergeCatsUnionValuesByKeys2(self):
        d_to = {
            'key_item': ['key_value1', 'key_value2'],
            'item1': ['value11t', 'value12t'],
            'item2': ['value21t', 'value22t']
        }

        d_from = {
            'key_item': ['key_value1', 'key_value3'],
            'item1': ['value11f', 'value12f'],
            'item3': ['value31f', 'value32f']
        }

        d_combine = mergeCatItemsUnionValuesByKeys(
            d_to, d_from, ["key_item"], tf_replace=True)

        d_combine_ref = {
            'key_item': ['key_value1', 'key_value2', 'key_value3'],
            'item1': ['value11f', 'value12t', 'value12f'],
            'item2': ['value21t', 'value22t', '?'],
            'item3': ['value31f', '?',        'value32f']
        }
        self.assertEqual(d_combine, d_combine_ref)

    def testmergeCatsUnionValuesByKeys3(self):
        d_to = {
            'key_item': ['key_value1', 'key_value2'],
            'item1': ['?', 'value12t'],
            'item2': ['value21t', 'value22t']
        }

        d_from = {
            'key_item': ['key_value1', 'key_value3'],
            'item1': ['value11f', 'value12f'],
            'item3': ['value31f', 'value32f']
        }

        d_combine = mergeCatItemsUnionValuesByKeys(d_to, d_from, ["key_item"])

        d_combine_ref = {
            'key_item': ['key_value1', 'key_value2', 'key_value3'],
            'item1': ['value11f', 'value12t', 'value12f'],
            'item2': ['value21t', 'value22t', '?'],
            'item3': ['value31f', '?',        'value32f']
        }
        self.assertEqual(d_combine, d_combine_ref)

    def testmergeCatsUnionValuesByKeysEM1(self):
        d_software_model_converted = {
            '_em_software.name': ['PHENIX'], 
            '_em_software.category': ['MODEL REFINEMENT'], 
            '_em_software.version': ['1.20.1_4487:']
            }
        
        d_em_software_model = {
            '_em_software.id': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13'], 
            '_em_software.category': ['PARTICLE SELECTION', 'IMAGE ACQUISITION', 'MASKING', 
            'CTF CORRECTION', 'LAYERLINE INDEXING', 'DIFFRACTION INDEXING', 'MODEL FITTING', 
            'MODEL REFINEMENT', 'OTHER', 'INITIAL EULER ASSIGNMENT', 'FINAL EULER ASSIGNMENT', 
            'CLASSIFICATION', 'RECONSTRUCTION'], 
            '_em_software.name': ['3dmod', ' ', ' ', ' ', ' ', ' ', ' ', 'PHENIX', ' ', ' ', ' ', ' ', ' '], 
            '_em_software.version': ['9.98 test', ' ', ' ', ' ', ' ', ' ', ' ', '9.99 test', ' ', ' ', ' ', ' ', ' ']
            }

        d_to = d_software_model_converted
        d_from = d_em_software_model

        d_combine = mergeCatItemsUnionValuesByKeys(d_to, d_from, ['_em_software.name', '_em_software.category'])

        d_combine_ref = {
            '_em_software.category': ['MODEL REFINEMENT', 'PARTICLE SELECTION'], 
            '_em_software.id': ['8', '1'], 
            '_em_software.version': ['1.20.1_4487:', '9.98 test'], 
            '_em_software.name': ['PHENIX', '3dmod']
            }

        self.assertEqual(d_combine, d_combine_ref)

    def testmergeCatsUpdateValuesByKeys1(self):
        d_to = {
            'key_item': ['key_value1', 'key_value2'],
            'item1': ['value11t', 'value12t'],
            'item2': ['value21t', 'value22t']
        }

        d_from = {
            'key_item': ['key_value1', 'key_value3'],
            'item1': ['value11f', 'value12f'],
            'item3': ['value31f', 'value32f']
        }

        d_combine = mergeCatItemsUpdateValuesByKeys(d_to, d_from, ["key_item"])

        d_combine_ref = {
            'key_item': ['key_value1', 'key_value2'],
            'item1': ['value11t', 'value12t'],
            'item2': ['value21t', 'value22t'],
            'item3': ['value31f', '?']
        }

        self.assertEqual(d_combine, d_combine_ref)

    def testmergeCatsUpdateValuesByKeys2(self):
        d_to = {
            'key_item': ['key_value1', 'key_value2'],
            'item1': ['value11t', 'value12t'],
            'item2': ['value21t', 'value22t']
        }

        d_from = {
            'key_item': ['key_value1', 'key_value3'],
            'item1': ['value11f', 'value12f'],
            'item3': ['value31f', 'value32f']
        }

        d_combine = mergeCatItemsUpdateValuesByKeys(
            d_to, d_from, ["key_item"], tf_replace=True)

        d_combine_ref = {
            'key_item': ['key_value1', 'key_value2'],
            'item1': ['value11f', 'value12t'],
            'item2': ['value21t', 'value22t'],
            'item3': ['value31f', '?']
        }
        self.assertEqual(d_combine, d_combine_ref)

    def testmergeCatsUpdateValuesByKeys3(self):
        d_to = {
            'key_item': ['key_value1', 'key_value2'],
            'item1': ['?', 'value12t'],
            'item2': ['value21t', 'value22t']
        }

        d_from = {
            'key_item': ['key_value1', 'key_value3'],
            'item1': ['value11f', 'value12f'],
            'item3': ['value31f', 'value32f']
        }

        d_combine = mergeCatItemsUpdateValuesByKeys(d_to, d_from, ["key_item"])

        d_combine_ref = {
            'key_item': ['key_value1', 'key_value2'],
            'item1': ['value11f', 'value12t'],
            'item2': ['value21t', 'value22t'],
            'item3': ['value31f', '?']
        }
        self.assertEqual(d_combine, d_combine_ref)

    def testmergeCatsUpdateValuesByRowIndex1(self):
        d_to = {
            'item1': ['value11t', 'value12t'],
            'item2': ['value21t', 'value22t']
        }

        d_from = {
            'item1': ['value11f', 'value12f'],
            'item3': ['value31f', 'value32f']
        }

        d_combine = mergeCatItemsUpdateValuesByRowIndex(d_to, d_from)

        d_combine_ref = {
            'item1': ['value11t', 'value12t'],
            'item2': ['value21t', 'value22t'],
            'item3': ['value31f', 'value32f']
        }

        self.assertEqual(d_combine, d_combine_ref)

    def testmergeCatsUpdateValuesByRowIndex2(self):
        d_to = {
            'item1': ['value11t', 'value12t'],
            'item2': ['value21t', 'value22t']
        }

        d_from = {
            'item1': ['value11f', 'value12f'],
            'item3': ['value31f', 'value32f']
        }

        d_combine = mergeCatItemsUpdateValuesByRowIndex(
            d_to, d_from, tf_replace=True)

        d_combine_ref = {
            'item1': ['value11f', 'value12f'],
            'item2': ['value21t', 'value22t'],
            'item3': ['value31f', 'value32f']
        }

        self.assertEqual(d_combine, d_combine_ref)

    def testmergeCatsUpdateValuesByRowIndex3(self):
        d_to = {
            'item1': ['?', 'value12t'],
            'item2': ['value21t', 'value22t']
        }

        d_from = {
            'item1': ['value11f', 'value12f'],
            'item3': ['value31f', 'value32f']
        }

        d_combine = mergeCatItemsUpdateValuesByRowIndex(d_to, d_from)

        d_combine_ref = {
            'item1': ['value11f', 'value12t'],
            'item2': ['value21t', 'value22t'],
            'item3': ['value31f', 'value32f']
        }

        self.assertEqual(d_combine, d_combine_ref)


if __name__ == "__main__":
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestMergeCats("testmergeCatsUnionValuesByKeys1"))
    test_suite.addTest(TestMergeCats("testmergeCatsUnionValuesByKeys2"))
    test_suite.addTest(TestMergeCats("testmergeCatsUnionValuesByKeys3"))
    test_suite.addTest(TestMergeCats("testmergeCatsUpdateValuesByKeys1"))
    test_suite.addTest(TestMergeCats("testmergeCatsUpdateValuesByKeys2"))
    test_suite.addTest(TestMergeCats("testmergeCatsUpdateValuesByKeys3"))
    test_suite.addTest(TestMergeCats("testmergeCatsUpdateValuesByRowIndex1"))
    test_suite.addTest(TestMergeCats("testmergeCatsUpdateValuesByRowIndex2"))
    test_suite.addTest(TestMergeCats("testmergeCatsUpdateValuesByRowIndex3"))
    test_suite.addTest(TestMergeCats("testmergeCatsUnionValuesByKeysEM1"))
    unittest.TextTestRunner(verbosity=2).run(test_suite)
