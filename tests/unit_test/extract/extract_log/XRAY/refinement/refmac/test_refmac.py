#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2025-03-25
# Updates:
#
# =============================================================================
"""
Unit test for refmac.py
"""
import os
import sys
import unittest

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))))
sys.path.insert(0, TOP_DIR)

from extract.extract_log.XRAY.refinement.refmac import refmac

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.folder_test_data = os.path.join(TOP_DIR, "tests/test_data/")

    def tearDown(self):
        pass

    def testExtractScalepack(self):
        d_ref = {
            'refine': {
                '_refine.pdbx_refine_id': ['X-RAY DIFFRACTION'], 
                '_refine.entry_id': ['UNNAMED'], 
                '_refine.pdbx_diffrn_id': ['1'], 
                '_refine.ls_number_reflns_obs': ['59321'], 
                '_refine.ls_d_res_low': ['19.893'], 
                '_refine.ls_d_res_high': ['2.060'], 
                '_refine.ls_percent_reflns_obs': ['68.4044'], 
                '_refine.ls_R_factor_R_work': ['0.1787'], 
                '_refine.ls_R_factor_R_free': ['0.2334'], 
                '_refine.ls_percent_reflns_R_free': ['5.0423'], 
                '_refine.correlation_coeff_Fo_to_Fc': ['0.9534'], 
                '_refine.correlation_coeff_Fo_to_Fc_free': ['0.9207'], 
                '_refine.pdbx_overall_ESU_R': ['0.3500'], 
                '_refine.pdbx_overall_ESU_R_Free': ['0.2372'], 
                '_refine.overall_SU_ML': ['0.1378'], 
                '_refine.overall_SU_B': ['10.1077']
            }, 
            'refine_ls_restr': {
                '_refine_ls_restr.type': ['r_bond_refined_d', 'r_bond_other_d', 'r_angle_refined_deg', 'r_angle_other_deg', 'r_dihedral_angle_1_deg', 'r_dihedral_angle_2_deg', 'r_dihedral_angle_3_deg', 'r_chiral_restr', 'r_gen_planes_refined', 'r_gen_planes_other', 'r_mcbond_it', 'r_mcbond_other', 'r_mcangle_it', 'r_mcangle_other', 'r_scbond_it', 'r_scbond_other', 'r_scangle_it', 'r_scangle_other', 'r_long_range_B_refined', 'r_long_range_B_other'], 
                '_refine_ls_restr.dev_ideal': ['0.009', '0.003', '1.884', '0.746', '7.408', '12.714', '15.010', '0.094', '0.008', '0.003', '2.202', '2.192', '3.368', '3.368', '2.632', '2.631', '4.144', '4.144', '5.727', '5.719'], 
                '_refine_ls_restr.dev_ideal_target': ['0.012', '0.016', '1.849', '1.767', '5.000', '5.000', '10.000', '0.200', '0.020', '0.020', '2.497', '2.494', '4.479', '4.479', '2.692', '2.692', '4.859', '4.859', '25.063', '25.066'], 
                '_refine_ls_restr.number': ['10694', '9907', '14473', '22777', '1248', '130', '1743', '1567', '12779', '2605', '5050', '5037', '6252', '6253', '5644', '5645', '8221', '8222', '11924', '11881'], 
                '_refine_ls_restr.pdbx_refine_id': ['X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION', 'X-RAY DIFFRACTION']
            }
        }
        folder = os.path.join(self.folder_test_data, "Refine_log")
        filepath = os.path.join(folder, "refmac_5.8.0430_XRAY_2025_3_6_8_5_2837710")
        # filepath = os.path.join(folder, "refmac_5.8.0425_XRAY_2025_3_3_10_5_2768480")
        # filepath = os.path.join(folder, "refmac_5.8.0267_XRAY_2025_2_26_22_38_2666649")
        # filepath = os.path.join(folder, "refmac_5.8.0258_XRAY_2025_2_21_2_34_2533180")
        log = refmac.LogRefmac()
        log.parse(filepath)
        self.assertEqual(log.d_, d_ref)
        for cat in log.d_:
            for item in log.d_[cat]:
                print(item, log.d_[cat][item])


if __name__ == "__main__":
    unittest.main()
