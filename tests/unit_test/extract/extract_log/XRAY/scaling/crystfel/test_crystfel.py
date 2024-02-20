#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2023-12-25
# Updates:
#
# =============================================================================
"""
Unit test for crystfel.py
"""
import os
import sys
import unittest

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))))
sys.path.insert(0, TOP_DIR)

from extract.extract_log.XRAY.scaling.crystfel import crystfel

import logging
log_format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s:%(lineno)d - %(message)s')

c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_handler.setFormatter(log_format)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(c_handler)

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.folder_test_data = os.path.join(TOP_DIR, "tests/test_data/")

    def tearDown(self):
        pass

    def testExtractGood(self):
        folder = os.path.join(self.folder_test_data, "PDB_CrystFEL")
        filepath = os.path.join(folder, "combined.log")
        log = crystfel.LogCrystfel()
        ret = log.parse(filepath)
        self.assertTrue(ret)

        d_ref = {'reflns': 
                 {'_reflns.entry_id': ['UNNAMED'], 
                  '_reflns.pdbx_diffrn_id': ['1'], 
                  '_reflns.pdbx_ordinal': ['1'], 
                  '_reflns.d_resolution_low': ['45.45'], 
                  '_reflns.d_resolution_high': ['2.5'], 
                  '_reflns.number_obs': ['32778'], 
                  '_reflns.percent_possible_obs': ['100.003051'], 
                  '_reflns.pdbx_redundancy': ['455.397492'], 
                  '_reflns.pdbx_CC_half': ['0.9831507'], 
                  '_reflns.pdbx_number_measured_all': ['14927019'], 
                  '_reflns.pdbx_R_split': ['0.1207']
                  }, 
                  'reflns_shell': 
                  {'_reflns_shell.pdbx_diffrn_id': ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], 
                   '_reflns_shell.pdbx_ordinal': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], 
                   '_reflns_shell.d_res_high': ['2.5', '2.59', '2.69', '2.82', '2.96', '3.15', '3.39', '3.73', '4.27', '5.38'], 
                   '_reflns_shell.d_res_low': ['2.59', '2.69', '2.82', '2.96', '3.15', '3.39', '3.73', '4.27', '5.38', '45.45'], 
                   '_reflns_shell.number_measured_all': ['1057679', '1074607', '1125217', '1164926', '1219624', '1258342', '1325450', '1643460', '1969641', '3088073'], 
                   '_reflns_shell.number_unique_obs': ['3240', '3204', '3231', '3238', '3256', '3256', '3277', '3280', '3323', '3473'], 
                   '_reflns_shell.pdbx_redundancy': ['326.4', '335.4', '348.3', '359.8', '374.6', '386.5', '404.5', '501.1', '592.7', '889.2'], 
                   '_reflns_shell.percent_possible_obs': ['100.00', '100.00', '100.00', '100.00', '100.00', '100.00', '100.00', '100.00', '100.00', '100.03'], 
                   '_reflns_shell.pdbx_CC_half': ['0.6714697', '0.7766946', '0.8398525', '0.9050327', '0.9443234', '0.9600602', '0.9727725', '0.9771509', '0.9733717', '0.9828289'], 
                   '_reflns_shell.pdbx_R_split': ['0.5564', '0.4348', '0.3277', '0.2474', '0.1953', '0.1436', '0.1141', '0.0949', '0.0951', '0.0928']
                   }, 
                   'pdbx_serial_crystallography_data_reduction': 
                   {'_pdbx_serial_crystallography_data_reduction.diffrn_id': ['1'], 
                   '_pdbx_serial_crystallography_data_reduction.crystal_hits': ['19928']
                   }, 
                   'diffrn': 
                   {'_diffrn.id': ['1'], 
                    '_diffrn.pdbx_serial_crystal_experiment': ['Y']
                    }
                    }

        for cat, d_cat in log.d_.items():
            for item, value in d_cat.items():
                # print(item, log.d_[cat][item])
                # print(item, d_ref[cat][item])
                self.assertEqual(value, d_ref[cat][item])

    # def testExtractBad(self):
    #     folder = os.path.join(self.folder_test_data, "PDB_cctbx_XFEL")
    #     filepath = os.path.join(folder, "bad.log")
    #     log = cctbx_xfel.LogCctbx_xfel()
    #     ret = log.parse(filepath)
    #     self.assertFalse(ret)

if __name__ == "__main__":
    unittest.main()
