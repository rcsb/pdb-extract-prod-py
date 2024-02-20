#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2023-12-25
# Updates:
#
# =============================================================================
"""
Unit test for cctbx_xfel.py
"""
import os
import sys
import unittest

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))))
sys.path.insert(0, TOP_DIR)

from extract.extract_log.XRAY.scaling.cctbxxfel import cctbxxfel

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
        folder = os.path.join(self.folder_test_data, "PDB_cctbx_XFEL")
        filepath = os.path.join(folder, "good_1.log")
        log = cctbxxfel.LogCctbx_xfel()
        ret = log.parse(filepath)
        self.assertTrue(ret)

        d_ref = {'reflns': 
                 {'_reflns.entry_id': ['UNNAMED'], 
                  '_reflns.pdbx_diffrn_id': ['1'], 
                  '_reflns.pdbx_ordinal': ['1'], 
                  '_reflns.d_resolution_low': ['28.44'], 
                  '_reflns.d_resolution_high': ['1.8000'], 
                  '_reflns.number_obs': ['100015'], 
                  '_reflns.number_all': ['100280'], 
                  '_reflns.percent_possible_obs': ['0.997'], 
                  '_reflns.pdbx_netI_over_sigmaI': ['5.725'], 
                  '_reflns.pdbx_redundancy': ['158.12'], 
                  '_reflns.pdbx_CC_half': ['0.991'], 
                  '_reflns.pdbx_number_measured_all': ['15885649'], 
                  '_reflns.pdbx_R_split': ['0.147']
                  }, 
                  'reflns_shell': 
                  {'_reflns_shell.pdbx_diffrn_id': ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'], 
                   '_reflns_shell.pdbx_ordinal': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20'], 
                   '_reflns_shell.d_res_high': ['1.8000', '1.8310', '1.8643', '1.9002', '1.9390', '1.9812', '2.0272', '2.0779', '2.1341', '2.1969', '2.2679', '2.3489', '2.4430', '2.5542', '2.6888', '2.8573', '3.0780', '3.3877', '3.8780', '4.8859'], 
                   '_reflns_shell.d_res_low': ['1.8310', '1.8643', '1.9002', '1.9390', '1.9812', '2.0272', '2.0779', '2.1341', '2.1969', '2.2679', '2.3489', '2.4430', '2.5542', '2.6888', '2.8573', '3.0780', '3.3877', '3.8780', '4.8859', '28.44'], 
                   '_reflns_shell.number_measured_all': ['61179', '86454', '117831', '140622', '190699', '258300', '290255', '362663', '452202', '538900', '618771', '769965', '819283', '865087', '1149300', '1245324', '1400688', '1675960', '1925995', '2916171'], 
                   '_reflns_shell.number_unique_obs': ['4600', '4870', '4940', '4907', '4988', '4954', '4939', '4968', '4988', '4979', '4989', '4985', '5002', '5028', '5047', '5037', '5076', '5110', '5181', '5427'], 
                   '_reflns_shell.pdbx_redundancy': ['12.47', '17.47', '23.79', '28.62', '38.22', '52.14', '58.77', '73.00', '90.66', '108.23', '124.03', '154.46', '163.79', '172.05', '227.72', '247.24', '275.94', '327.98', '371.74', '533.22'], 
                   '_reflns_shell.percent_possible_obs': ['0.957', '0.984', '0.997', '0.999', '1.0', '1.0', '1.0', '1.0', '1.0', '1.0', '1.0', '1.0', '1.0', '1.0', '1.0', '1.0', '1.0', '1.0', '1.0', '0.992'], 
                   '_reflns_shell.pdbx_netI_over_sigmaI_obs': ['0.612', '0.695', '0.796', '0.899', '1.033', '1.233', '1.394', '1.591', '1.823', '2.184', '2.493', '2.894', '3.231', '3.807', '4.642', '6.163', '9.371', '14.846', '22.389', '28.982'], 
                   '_reflns_shell.number_unique_all': ['4776', '4938', '4953', '4914', '4988', '4954', '4939', '4968', '4988', '4979', '4989', '4985', '5002', '5028', '5047', '5037', '5076', '5110', '5181', '5428'], 
                   '_reflns_shell.pdbx_CC_half': ['0.048', '0.065', '0.083', '0.17', '0.264', '0.375', '0.495', '0.419', '0.372', '0.784', '0.828', '0.884', '0.913', '0.937', '0.964', '0.98', '0.99', '0.996', '0.997', '0.999'], 
                   '_reflns_shell.pdbx_R_split': ['1.095', '1.024', '0.956', '0.861', '0.764', '0.66', '0.589', '0.551', '0.5', '0.379', '0.341', '0.288', '0.252', '0.218', '0.174', '0.129', '0.083', '0.05', '0.035', '0.026']
                  }, 
                   'diffrn_source': 
                   {'_diffrn_source.diffrn_id': ['1'], 
                    '_diffrn_source.pdbx_wavelength_list': ['1.260535']
                   }, 
                    'pdbx_serial_crystallography_data_reduction': 
                    {'_pdbx_serial_crystallography_data_reduction.diffrn_id': ['1'], 
                     '_pdbx_serial_crystallography_data_reduction.lattices_merged': ['77167']
                    }, 
                    'diffrn': 
                    {'_diffrn.id': ['1'], 
                      '_diffrn.pdbx_serial_crystal_experiment': ['Y']
                    }
        }

        # print(log.d_)
        for cat, d_cat in log.d_.items():
            for item, value in d_cat.items():
                # print(item, log.d_[cat][item])
                # print(item, d_ref[cat][item])
                self.assertEqual(value, d_ref[cat][item])

    def testExtractBad(self):
        folder = os.path.join(self.folder_test_data, "PDB_cctbx_XFEL")
        filepath = os.path.join(folder, "bad.log")
        log = cctbxxfel.LogCctbx_xfel()
        ret = log.parse(filepath)
        self.assertFalse(ret)

if __name__ == "__main__":
    unittest.main()

