#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2025-03-25
# Updates:
#
# =============================================================================
"""
Unit test for phenix.py
"""
import os
import sys
import unittest

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))))
sys.path.insert(0, TOP_DIR)

from extract.extract_log.XRAY.refinement.phenix import phenix

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.folder_test_data = os.path.join(TOP_DIR, "tests/test_data/")

    def tearDown(self):
        pass

    def testExtractScalepack(self):
        d_ref = {'refine': 
                 {'_refine.pdbx_refine_id': ['X-RAY DIFFRACTION'], 
                  '_refine.entry_id': ['UNNAMED'], '_refine.pdbx_diffrn_id': ['1'], 
                  '_refine.ls_number_reflns_obs': ['31940'], 
                  '_refine.ls_d_res_low': ['25.16'], 
                  '_refine.ls_d_res_high': ['2.50'], 
                  '_refine.ls_percent_reflns_obs': ['99.74'], 
                  '_refine.ls_R_factor_obs': ['0.1836'], 
                  '_refine.ls_R_factor_R_work': ['0.1819'], 
                  '_refine.ls_R_factor_R_free': ['0.2178'], 
                  '_refine.ls_percent_reflns_R_free': ['5.07']
                  }, 
                  'refine_ls_shell': 
                  {'_refine_ls_shell.pdbx_refine_id': ['X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION'], 
                   '_refine_ls_shell.d_res_high': ['2.50', '2.57', '2.65', '2.75', '2.86', '2.99', '3.15', '3.34', '3.60', '3.96', '4.53', '5.70'], 
                   '_refine_ls_shell.d_res_low': ['2.57', '2.65', '2.75', '2.86', '2.99', '3.15', '3.34', '3.60', '3.96', '4.53', '5.70', '25.16'], 
                   '_refine_ls_shell.number_reflns_R_work': ['2406', '2442', '2472', '2475', '2499', '2443', '2506', '2494', '2566', '2583', '2630', '2804'], 
                   '_refine_ls_shell.R_factor_R_work': ['0.2292', '0.2148', '0.2201', '0.2220', '0.2143', '0.2013', '0.2015', '0.1881', '0.1637', '0.1499', '0.1656', '0.1842'], 
                   '_refine_ls_shell.percent_reflns_obs': ['99.0', '100.0', '100.0', '100.0', '100.0', '100.0', '100.0', '100.0', '100.0', '100.0', '100.0', '98.0'], 
                   '_refine_ls_shell.R_factor_R_free': ['0.2937', '0.2968', '0.2654', '0.2885', '0.2335', '0.2444', '0.2357', '0.2218', '0.1678', '0.1647', '0.1911', '0.2455'], 
                   '_refine_ls_shell.number_reflns_R_free': ['147', '142', '132', '133', '133', '136', '134', '161', '120', '116', '132', '134']
                   }, 
                   'refine_ls_restr': 
                   {'_refine_ls_restr.type': ['f_bond_d', 'f_angle_d'], 
                    '_refine_ls_restr.dev_ideal': ['0.006', '0.867'], 
                    '_refine_ls_restr.number': ['4451', '6176'], 
                    '_refine_ls_restr.pdbx_refine_id': ['X-RAY DIFFRACTION', 'X-RAY DIFFRACTION']
                    }
                }
        folder = os.path.join(self.folder_test_data, "Refine_log")
        filepath = os.path.join(folder, "phenix_1.21.2_XRAY_2025_2_27_3_9_2670933")
        log = phenix.LogPhenix()
        log.parse(filepath)
        self.assertEqual(log.d_, d_ref)
        for cat in log.d_:
            for item in log.d_[cat]:
                print(item, log.d_[cat][item])


if __name__ == "__main__":
    unittest.main()
