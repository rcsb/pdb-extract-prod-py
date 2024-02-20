#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-20
# Updates:
#
# =============================================================================
"""
Unit test for aimless_html.py
"""
import unittest
from extract.extract_log.XRAY.scaling.aimless import aimless_html


class TestExtract(unittest.TestCase):
    def testExtract(self):
        d_ref = {'reflns': {'_reflns.entry_id': ['UNNAMED'], '_reflns.pdbx_diffrn_id': ['1'], '_reflns.pdbx_ordinal': ['1'], '_reflns.d_resolution_low': ['43.02'], '_reflns.d_resolution_high': ['3.06'], '_reflns.number_obs': ['9500'], '_reflns.percent_possible_obs': ['99.9'], '_reflns.pdbx_Rmerge_I_obs': ['0.437'], '_reflns.pdbx_netI_over_sigmaI': ['6.3'], '_reflns.pdbx_redundancy': ['13.2'], '_reflns.pdbx_Rrim_I_all': ['0.455'], '_reflns.pdbx_Rpim_I_all': ['0.124'], '_reflns.pdbx_CC_half': ['0.993'], '_reflns.pdbx_number_measured_all': ['125124'], '_reflns.pdbx_chi_squared': ['1.01']}, 'reflns_shell': {'_reflns_shell.pdbx_diffrn_id': ['1'], '_reflns_shell.pdbx_ordinal': ['1'], '_reflns_shell.d_res_high': ['3.06'], '_reflns_shell.d_res_low': ['3.27'], '_reflns_shell.number_measured_all': ['21542'], '_reflns_shell.number_unique_obs': ['1672'], '_reflns_shell.Rmerge_I_obs': ['1.747'], '_reflns_shell.pdbx_chi_squared': ['1.00'], '_reflns_shell.pdbx_redundancy': ['12.9'], '_reflns_shell.percent_possible_obs': ['99.6'], '_reflns_shell.pdbx_netI_over_sigmaI_obs': ['1.7'], '_reflns_shell.pdbx_Rrim_I_all': ['1.820'], '_reflns_shell.pdbx_Rpim_I_all': ['0.503'], '_reflns_shell.pdbx_CC_half': ['0.622']}}
        
        filepath = "/Users/chenghua/Projects/pdb-extract-prod-py/tests/test_data/PDB_XDS_AimlessHTML_Phenix_2021_9_20_22_31146/file_scl_1"
        log = aimless_html.LogAimlessHtml()
        log.parse(filepath)
        self.assertEqual(log.d_, d_ref)


if __name__ == "__main__":
    unittest.main()
