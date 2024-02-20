#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-20
# Updates:
#
# =============================================================================
"""
Unit test for aimless.py
"""

import os
import sys
import unittest

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))))
sys.path.insert(0, TOP_DIR)

from extract.extract_log.XRAY.scaling.aimless import aimless

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.folder_test_data = os.path.join(TOP_DIR, "tests/test_data/")

    def tearDown(self):
        pass

    def testExtractCCP4(self):
        d_ref = {'reflns': 
        {'_reflns.entry_id': ['UNNAMED'], 
        '_reflns.pdbx_diffrn_id': ['1'], 
        '_reflns.pdbx_ordinal': ['1'], 
        '_reflns.d_resolution_low': ['40.65'], 
        '_reflns.d_resolution_high': ['1.80'], 
        '_reflns.number_obs': ['22741'], 
        '_reflns.percent_possible_obs': ['97.0'], 
        '_reflns.pdbx_Rmerge_I_obs': ['0.074'], 
        '_reflns.pdbx_netI_over_sigmaI': ['6.8'], 
        '_reflns.pdbx_redundancy': ['3.4'], 
        '_reflns.pdbx_Rrim_I_all': ['0.088'], 
        '_reflns.pdbx_Rpim_I_all': ['0.047'], 
        '_reflns.pdbx_CC_half': ['0.997'], 
        '_reflns.pdbx_number_measured_all': ['78435'], 
        '_reflns.pdbx_chi_squared': ['0.45']
        }, 
        'reflns_shell': 
        {'_reflns_shell.pdbx_diffrn_id': ['1'], 
        '_reflns_shell.pdbx_ordinal': ['1'], 
        '_reflns_shell.d_res_high': ['1.80'], 
        '_reflns_shell.d_res_low': ['1.84'], 
        '_reflns_shell.number_measured_all': ['4166'], 
        '_reflns_shell.number_unique_obs': ['1294'], 
        '_reflns_shell.Rmerge_I_obs': ['0.444'], 
        '_reflns_shell.pdbx_chi_squared': ['0.39'], 
        '_reflns_shell.pdbx_redundancy': ['3.2'], 
        '_reflns_shell.percent_possible_obs': ['95.6'], 
        '_reflns_shell.pdbx_netI_over_sigmaI_obs': ['1.8'], 
        '_reflns_shell.pdbx_Rrim_I_all': ['0.533'], 
        '_reflns_shell.pdbx_Rpim_I_all': ['0.292'], 
        '_reflns_shell.pdbx_CC_half': ['0.862']
        }
        }

        folder = os.path.join(self.folder_test_data, "PDB_XDS_Aimless_Phaser_Phenix_2021_10_8_18_16442")
        filepath = os.path.join(folder, "file_scl_1")
        log = aimless.LogAimless()
        log.parse(filepath)
        # print(log.d_)
        for cat in log.d_:
            for item in log.d_[cat]:
                print(item, log.d_[cat][item])
                # print(item, d_ref[cat][item])
                self.assertEqual(log.d_[cat][item], d_ref[cat][item])

    def testExtractHTML(self):
        d_ref = {'reflns': 
        {'_reflns.entry_id': ['UNNAMED'], 
        '_reflns.pdbx_diffrn_id': ['1'], 
        '_reflns.pdbx_ordinal': ['1'], 
        '_reflns.d_resolution_low': ['43.02'], 
        '_reflns.d_resolution_high': ['3.06'], 
        '_reflns.number_obs': ['9500'], 
        '_reflns.percent_possible_obs': ['99.9'], 
        '_reflns.pdbx_Rmerge_I_obs': ['0.437'], 
        '_reflns.pdbx_netI_over_sigmaI': ['6.3'], 
        '_reflns.pdbx_redundancy': ['13.2'], 
        '_reflns.pdbx_Rrim_I_all': ['0.455'], 
        '_reflns.pdbx_Rpim_I_all': ['0.124'], 
        '_reflns.pdbx_CC_half': ['0.993'], 
        '_reflns.pdbx_number_measured_all': ['125124'], 
        '_reflns.pdbx_chi_squared': ['1.01']
        }, 
        'reflns_shell': 
        {'_reflns_shell.pdbx_diffrn_id': ['1'], 
        '_reflns_shell.pdbx_ordinal': ['1'], 
        '_reflns_shell.d_res_high': ['3.06'], 
        '_reflns_shell.d_res_low': ['3.27'], 
        '_reflns_shell.number_measured_all': ['21542'], 
        '_reflns_shell.number_unique_obs': ['1672'], 
        '_reflns_shell.Rmerge_I_obs': ['1.747'], 
        '_reflns_shell.pdbx_chi_squared': ['1.00'], 
        '_reflns_shell.pdbx_redundancy': ['12.9'], 
        '_reflns_shell.percent_possible_obs': ['99.6'], 
        '_reflns_shell.pdbx_netI_over_sigmaI_obs': ['1.7'], 
        '_reflns_shell.pdbx_Rrim_I_all': ['1.820'], 
        '_reflns_shell.pdbx_Rpim_I_all': ['0.503'], 
        '_reflns_shell.pdbx_CC_half': ['0.622']
        }
        }

        folder = os.path.join(self.folder_test_data, "PDB_XDS_AimlessHTML_Phenix_2021_9_20_22_31146")
        filepath = os.path.join(folder, "file_scl_1")
        log = aimless.LogAimless()
        log.parse(filepath)
        # print(log.d_)
        for cat in log.d_:
            for item in log.d_[cat]:
                print(item, log.d_[cat][item])
                # print(item, d_ref[cat][item])
                self.assertEqual(log.d_[cat][item], d_ref[cat][item])

    def testExtractAutoPROC(self):
        d_ref = {'reflns': 
        {'_reflns.entry_id': ['UNNAMED'], 
        '_reflns.pdbx_diffrn_id': ['1'], 
        '_reflns.pdbx_ordinal': ['1'], 
        '_reflns.d_resolution_low': ['150.093'], 
        '_reflns.d_resolution_high': ['2.997'], 
        '_reflns.number_obs': ['14084'], 
        '_reflns.percent_possible_obs': ['100.0'], 
        '_reflns.pdbx_Rmerge_I_obs': ['0.165'], 
        '_reflns.pdbx_redundancy': ['6.3'], 
        '_reflns.pdbx_Rrim_I_all': ['0.180'], 
        '_reflns.pdbx_Rpim_I_all': ['0.071'], 
        '_reflns.pdbx_number_measured_all': ['88039'],
        '_reflns.pdbx_netI_over_sigmaI': ['9.9']
        }, 
        'reflns_shell': 
        {'_reflns_shell.pdbx_diffrn_id': ['1'], 
        '_reflns_shell.pdbx_ordinal': ['1'], 
        '_reflns_shell.d_res_high': ['2.997'], 
        '_reflns_shell.d_res_low': ['3.007'], 
        '_reflns_shell.number_measured_all': ['958'], 
        '_reflns_shell.number_unique_obs': ['147'], 
        '_reflns_shell.Rmerge_I_obs': ['0.543'], 
        '_reflns_shell.pdbx_redundancy': ['6.5'], 
        '_reflns_shell.percent_possible_obs': ['100.0'], 
        '_reflns_shell.pdbx_Rrim_I_all': ['0.590'], 
        '_reflns_shell.pdbx_Rpim_I_all': ['0.229'],
        '_reflns_shell.pdbx_netI_over_sigmaI_obs': ['3.4']
        }
        }

        folder = os.path.join(self.folder_test_data, "Aimless_autoPROC_log")
        filepath = os.path.join(folder, "aP_scale.log")
        log = aimless.LogAimless()
        log.parse(filepath)
        print(log.d_)
        for cat in log.d_:
            for item in log.d_[cat]:
                print(item, log.d_[cat][item])
                # print(item, d_ref[cat][item])
                self.assertEqual(log.d_[cat][item], d_ref[cat][item])


if __name__ == "__main__":
    unittest.main()
