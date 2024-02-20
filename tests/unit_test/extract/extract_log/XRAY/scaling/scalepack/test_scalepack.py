#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-20
# Updates:
#
# =============================================================================
"""
Unit test for scalepack.py
"""
import os
import sys
import unittest

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))))
sys.path.insert(0, TOP_DIR)

from extract.extract_log.XRAY.scaling.scalepack import scalepack

class TestExtract(unittest.TestCase):
    def setUp(self):
        self.folder_test_data = os.path.join(TOP_DIR, "tests/test_data/")

    def tearDown(self):
        pass

    def testExtractScalepack(self):
        d_ref = {'reflns': {'_reflns.entry_id': ['UNNAMED'],
                            '_reflns.pdbx_diffrn_id': ['1'],
                            '_reflns.pdbx_ordinal': ['1'],
                            '_reflns.d_resolution_low': ['50.00'],
                            '_reflns.d_resolution_high': ['1.67'],
                            '_reflns.number_obs': ['17121'],
                            '_reflns.percent_possible_obs': ['98.9'],
                            '_reflns.pdbx_Rmerge_I_obs': ['0.051'],
                            '_reflns.pdbx_netI_over_sigmaI': ['19.9'],
                            '_reflns.pdbx_redundancy': ['4.5'],
                            '_reflns.pdbx_number_measured_all': ['76499'],
                            '_reflns.pdbx_chi_squared': ['1.290']
                            },
                 'reflns_shell': {'_reflns_shell.pdbx_diffrn_id': ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
                                  '_reflns_shell.pdbx_ordinal': ['13', '12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1'],
                                  '_reflns_shell.d_res_high': ['1.67', '1.72', '1.77', '1.82', '1.89', '1.96', '2.05', '2.16', '2.30', '2.47', '2.72', '3.12', '3.93'],
                                  '_reflns_shell.d_res_low': ['1.72', '1.77', '1.82', '1.89', '1.96', '2.05', '2.16', '2.30', '2.47', '2.72', '3.12', '3.93', '50.00'],
                                  '_reflns_shell.number_unique_obs': ['1286', '1309', '1271', '1309', '1276', '1304', '1298', '1315', '1319', '1325', '1346', '1349', '1414'],
                                  '_reflns_shell.Rmerge_I_obs': ['0.334', '0.283', '0.210', '0.170', '0.140', '0.111', '0.090', '0.076', '0.066', '0.053', '0.045', '0.038', '0.034'],
                                  '_reflns_shell.pdbx_chi_squared': ['1.658', '1.610', '1.541', '1.573', '1.498', '1.381', '1.196', '1.192', '1.090', '1.010', '1.062', '1.142', '1.034'],
                                  '_reflns_shell.pdbx_redundancy': ['4.0', '4.3', '4.2', '4.3', '4.4', '4.5', '4.5', '4.5', '4.6', '4.8', '4.8', '4.7', '4.5'],
                                  '_reflns_shell.percent_possible_all': ['98.9', '99.3', '98.8', '99.2', '98.8', '99.2', '98.7', '99.1', '99.6', '99.7', '99.5', '98.8', '96.4']
                                  }
                 }
        folder = os.path.join(self.folder_test_data, "PDB_Template_Scalepack_1")
        filepath = os.path.join(folder, "scalepack.log")
        log = scalepack.LogScalepack()
        log.parse(filepath)
        # print(log.d_)
        for cat in log.d_:
            for item in log.d_[cat]:
                # print(item, log.d_[cat][item])
                # print(item, d_ref[cat][item])
                self.assertEqual(log.d_[cat][item], d_ref[cat][item])

    def testExtractHKL2000(self):
        d_ref = {'reflns':
                     {'_reflns.entry_id': ['UNNAMED'],
                      '_reflns.pdbx_diffrn_id': ['1'],
                      '_reflns.pdbx_ordinal': ['1'],
                      '_reflns.d_resolution_low': ['50.00'],
                      '_reflns.d_resolution_high': ['1.15'],
                      '_reflns.number_obs': ['62701'],
                      '_reflns.percent_possible_obs': ['98.9'],
                      '_reflns.pdbx_Rmerge_I_obs': ['0.067'],
                      '_reflns.pdbx_netI_over_sigmaI': ['17.9'],
                      '_reflns.pdbx_redundancy': ['6.5'],
                      '_reflns.pdbx_Rrim_I_all': ['0.072'],
                      '_reflns.pdbx_Rpim_I_all': ['0.025'],
                      '_reflns.pdbx_CC_half': ['0.999'],
                      '_reflns.pdbx_number_measured_all': ['404893'],
                      '_reflns.pdbx_chi_squared': ['0.999'],
                      '_reflns.pdbx_CC_star': ['1.000']
                  },
                 'reflns_shell':
                     {'_reflns_shell.pdbx_diffrn_id': ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
                      '_reflns_shell.pdbx_ordinal': ['10', '9', '8', '7', '6', '5', '4', '3', '2', '1'],
                      '_reflns_shell.d_res_high': ['1.15', '1.19', '1.24', '1.30', '1.36', '1.45', '1.56', '1.72', '1.97', '2.48'],
                      '_reflns_shell.d_res_low': ['1.19', '1.24', '1.30', '1.36', '1.45', '1.56', '1.72', '1.97', '2.48', '50.00'],
                      '_reflns_shell.number_unique_obs': ['6102', '6281', '6333', '6303', '6336', '6322', '6336', '6350', '6338', '6000'],
                      '_reflns_shell.Rmerge_I_obs': ['0.547', '0.507', '0.399', '0.268', '0.184', '0.133', '0.102', '0.076', '0.066', '0.057'],
                      '_reflns_shell.pdbx_chi_squared': ['0.991', '0.995', '0.991', '1.007', '1.005', '0.997', '1.001', '0.995', '1.007', '0.996'],
                      '_reflns_shell.pdbx_redundancy': ['2.8', '4.5', '5.6', '5.6', '5.8', '6.3', '7.1', '8.9', '9.6', '8.5'],
                      '_reflns_shell.percent_possible_all': ['96.2', '99.9', '100.0', '100.0', '100.0', '100.0', '100.0', '99.9', '99.7', '93.2'],
                      '_reflns_shell.pdbx_Rrim_I_all': ['0.661', '0.573', '0.440', '0.295', '0.202', '0.145', '0.109', '0.080', '0.069', '0.061'],
                      '_reflns_shell.pdbx_Rpim_I_all': ['0.364', '0.261', '0.183', '0.122', '0.083', '0.057', '0.040', '0.027', '0.022', '0.021'],
                      '_reflns_shell.pdbx_CC_half': ['0.718', '0.839', '0.934', '0.967', '0.983', '0.992', '0.995', '0.997', '0.997', '0.998'],
                      '_reflns_shell.pdbx_CC_star': ['0.914', '0.955', '0.983', '0.992', '0.996', '0.998', '0.999', '0.999', '0.999', '1.000']
                      }
                     }

        folder = os.path.join(self.folder_test_data, "PDB_HKL2000_Phaser_Refmac_2021_9_28_13_26368")
        filepath = os.path.join(folder, "file_scl_1")
        log = scalepack.LogScalepack()
        log.parse(filepath)
        # print(log.d_)
        for cat in log.d_:
            for item in log.d_[cat]:
                # print(item, log.d_[cat][item])
                # print(item, d_ref[cat][item])
                self.assertEqual(log.d_[cat][item], d_ref[cat][item])

    def testExtractHKL3000(self):
        d_ref = {'reflns': {'_reflns.entry_id': ['UNNAMED'],
                            '_reflns.pdbx_diffrn_id': ['1'],
                            '_reflns.pdbx_ordinal': ['1'],
                            '_reflns.d_resolution_low': ['50.00'],
                            '_reflns.d_resolution_high': ['1.92'],
                            '_reflns.number_obs': ['34468'],
                            '_reflns.percent_possible_obs': ['100.0'],
                            '_reflns.pdbx_Rmerge_I_obs': ['0.063'],
                            '_reflns.pdbx_netI_over_sigmaI': ['9.7'],
                            '_reflns.pdbx_redundancy': ['18.1'],
                            '_reflns.pdbx_Rrim_I_all': ['0.065'],
                            '_reflns.pdbx_Rpim_I_all': ['0.015'],
                            '_reflns.pdbx_CC_half': ['1.002'],
                            '_reflns.pdbx_number_measured_all': ['623704'],
                            '_reflns.pdbx_chi_squared': ['0.928'],
                            '_reflns.pdbx_CC_star': ['1.000']},
                 'reflns_shell':
                                 {'_reflns_shell.pdbx_diffrn_id': ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
                                  '_reflns_shell.pdbx_ordinal': ['20', '19', '18', '17', '16', '15', '14', '13', '12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1'],
                                  '_reflns_shell.d_res_high': ['1.92', '1.95', '1.99', '2.03', '2.07', '2.11', '2.16', '2.22', '2.28', '2.34', '2.42', '2.51', '2.61', '2.72', '2.87', '3.05', '3.28', '3.61', '4.14', '5.21'],
                                  '_reflns_shell.d_res_low': ['1.95', '1.99', '2.03', '2.07', '2.11', '2.16', '2.22', '2.28', '2.34', '2.42', '2.51', '2.61', '2.72', '2.87', '3.05', '3.28', '3.61', '4.14', '5.21', '50.00'],
                                  '_reflns_shell.number_unique_obs': ['1702', '1681', '1672', '1712', '1669', '1686', '1697', '1691', '1710', '1706', '1696', '1708', '1701', '1718', '1742', '1718', '1746', '1787', '1779', '1947'],
                                  '_reflns_shell.Rmerge_I_obs': ['0.985', '0.720', '0.615', '0.485', '0.379', '0.337', '0.263', '0.212', '0.176', '0.151', '0.133', '0.106', '0.088', '0.072', '0.063', '0.055', '0.049', '0.045', '0.042', '0.040'],
                                  '_reflns_shell.pdbx_chi_squared': ['0.419', '0.433', '0.424', '0.448', '0.461', '0.465', '0.478', '0.502', '0.505', '0.529', '0.546', '0.607', '0.707', '0.833', '1.063', '1.408', '1.803', '2.053', '2.142', '2.102'],
                                  '_reflns_shell.pdbx_redundancy': ['17.6', '17.4', '16.8', '15.4', '17.1', '18.7', '18.7', '18.7', '18.5', '18.4', '18.3', '18.2', '18.1', '17.6', '16.6', '20.6', '20.5', '19.6', '17.9', '17.2'],
                                  '_reflns_shell.percent_possible_all': ['100.0', '100.0', '100.0', '100.0', '100.0', '100.0', '100.0', '100.0', '100.0', '100.0', '100.0', '100.0', '99.9', '100.0', '100.0', '100.0', '99.9', '99.8', '99.6', '99.8'],
                                  '_reflns_shell.pdbx_Rrim_I_all': ['1.015', '0.742', '0.635', '0.502', '0.391', '0.346', '0.270', '0.218', '0.181', '0.155', '0.137', '0.109', '0.090', '0.074', '0.065', '0.056', '0.051', '0.047', '0.043', '0.042'],
                                  '_reflns_shell.pdbx_Rpim_I_all': ['0.240', '0.176', '0.153', '0.126', '0.093', '0.079', '0.062', '0.050', '0.042', '0.036', '0.032', '0.025', '0.021', '0.018', '0.016', '0.012', '0.011', '0.011', '0.010', '0.010'],
                                  '_reflns_shell.pdbx_CC_half': ['0.894', '0.939', '0.950', '0.962', '0.980', '0.986', '0.992', '0.994', '0.996', '0.997', '0.997', '0.998', '0.998', '0.999', '0.999', '0.999', '0.999', '0.999', '0.999', '0.999'],
                                  '_reflns_shell.pdbx_CC_star': ['0.972', '0.984', '0.987', '0.990', '0.995', '0.996', '0.998', '0.998', '0.999', '0.999', '0.999', '1.000', '1.000', '1.000', '1.000', '1.000', '1.000', '1.000', '1.000', '1.000']
                                  }
                 }

        folder = os.path.join(self.folder_test_data, "PDB_HKL3000_Phaser_Refmac_2023_01_12")
        filepath = os.path.join(folder, "file_scl_1")
        log = scalepack.LogScalepack()
        log.parse(filepath)
        # print(log.d_)
        for cat in log.d_:
            for item in log.d_[cat]:
                # print(item, log.d_[cat][item])
                # print(item, d_ref[cat][item])
                self.assertEqual(log.d_[cat][item], d_ref[cat][item])

if __name__ == "__main__":
    unittest.main()
