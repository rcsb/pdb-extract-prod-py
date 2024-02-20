#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2023-02-06
# Updates:
#
# =============================================================================
"""
Unit test for mergeLogTemplateToModel.py
"""
import os
import sys
import unittest
import filecmp

TOP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, TOP_DIR)

from extract.merge.mergeLogTemplateToModel import Merger


class TestMerge(unittest.TestCase):
    def setUp(self):
        self.test_data = os.path.join(
            TOP_DIR, "tests/test_data")

    def tearDown(self):
        pass

    def testMergeMaxitOutput(self):
        folder = os.path.join(
            self.test_data, "PDB_XDS_Aimless_Phaser_Phenix_2021_10_8_18_16442")
        filename_in = "maxit.cif"
        filename_out = "merged.cif"
        filename_ref = "merged.cif_ref"
        filepath_in = os.path.join(folder, filename_in)
        filepath_out = os.path.join(folder, filename_out)
        filepath_ref = os.path.join(folder, filename_ref)

        d_log = {'scaling':
                 {'reflns':
                  {'_reflns.entry_id': ['UNNAMED'],
                   '_reflns.pdbx_diffrn_id': ['1'],
                   '_reflns.pdbx_ordinal': ['1'],
                   '_reflns.d_resolution_low': ['50.00'],
                   '_reflns.d_resolution_high': ['1.67'],
                   '_reflns.test': ["9999"]},
                  }
                 }

        d_template = {'pdbx_database_status':
                      {'_pdbx_database_status.entry_id': ['ToBeAssigned'],
                       '_pdbx_database_status.dep_release_code_coordinates': ['HOLD FOR PUBLICATION'],
                       '_pdbx_database_status.dep_release_code_sequence': ['HOLD FOR RELEASE']
                       },
                      '_pdbx_audit_support':
                          {'_pdbx_audit_support.funding_organization': ['National Institutes of Health/National Institute of General Medical Sciences'],
                           '_pdbx_audit_support.country': ['United States'],
                           '_pdbx_audit_support.grant_number': ['XX000000']
                           }
                      }
        d_software_author = {"_software.name": ["DENZO", "SCALEPACK", "phenix"],
                             "_software.classification": ["data reduction", "data scaling", "refinement"],
                             "_software.test": ["test1", "test2", "test3"],
                             "_software.citation_id": ["1", "2", "3"]
                             }

        merger = Merger()
        merger.readModel(filepath_in)
        merger.truncateMaxitCat()
        # merger.addCat(d_software)

        merger.mergeLog(d_log)
        merger.mergeTemplate(d_template)
        merger.processSoftwareXRAY(d_software_author)

        merger.addRefine()
        merger.write(filepath_out)

        self.assertTrue(os.path.isfile(filepath_out))
        self.assertTrue(filecmp.cmp(filepath_out, filepath_ref))

        try:
            os.remove(filepath_out)
        except FileNotFoundError:
            pass

    def testMergePhenixCifOutput(self):
        folder = os.path.join(
            self.test_data, "CIF_Phenix_D_1000262088")
        filename_in = "D_1000262088_model-upload_P1.cif.V1"
        filename_out = "merged.cif"
        filename_ref = "merged.cif_ref"
        filepath_in = os.path.join(folder, filename_in)
        filepath_out = os.path.join(folder, filename_out)
        filepath_ref = os.path.join(folder, filename_ref)

        d_log = {'scaling':
                 {'reflns':
                  {'_reflns.entry_id': ['UNNAMED'],
                   '_reflns.pdbx_diffrn_id': ['1'],
                   '_reflns.pdbx_ordinal': ['1'],
                   '_reflns.d_resolution_low': ['50.00'],
                   '_reflns.d_resolution_high': ['1.67'],
                   '_reflns.test': ["9999"]},
                  }
                 }

        d_template = {'pdbx_database_status':
                      {'_pdbx_database_status.entry_id': ['ToBeAssigned'],
                       '_pdbx_database_status.dep_release_code_coordinates': ['HOLD FOR PUBLICATION'],
                       '_pdbx_database_status.dep_release_code_sequence': ['HOLD FOR RELEASE']
                       },
                      '_pdbx_audit_support':
                          {'_pdbx_audit_support.funding_organization': ['National Institutes of Health/National Institute of General Medical Sciences'],
                           '_pdbx_audit_support.country': ['United States'],
                           '_pdbx_audit_support.grant_number': ['XX000000']
                           }
                      }
        d_software_author = {"_software.name": ["DENZO", "SCALEPACK", "phenix"],
                             "_software.classification": ["data reduction", "data scaling", "refinement"],
                             "_software.test": ["test1", "test2", "test3"],
                             "_software.citation_id": ["1", "2", "3"]
                             }

        merger = Merger()
        merger.readModel(filepath_in)
        merger.truncateMaxitCat()

        merger.mergeLog(d_log)
        merger.mergeTemplate(d_template)
        merger.processSoftwareXRAY(d_software_author)

        merger.addRefine()
        merger.write(filepath_out)

        self.assertTrue(os.path.isfile(filepath_out))
        self.assertTrue(filecmp.cmp(filepath_out, filepath_ref))

        try:
            os.remove(filepath_out)
        except FileNotFoundError:
            pass

    def testMergeMaxitOutputMod(self):
        folder = os.path.join(
            self.test_data, "PDB_XDS_Aimless_Phaser_Phenix_2021_10_8_18_16442")
        filename_in = "maxit_mod_software.cif"
        filename_out = "merged_mod_software.cif"
        filename_ref = "merged_mod_software.cif_ref"
        filepath_in = os.path.join(folder, filename_in)
        filepath_out = os.path.join(folder, filename_out)
        filepath_ref = os.path.join(folder, filename_ref)

        d_log = {'scaling':
                 {'reflns':
                  {'_reflns.entry_id': ['UNNAMED'],
                   '_reflns.pdbx_diffrn_id': ['1'],
                   '_reflns.pdbx_ordinal': ['1'],
                   '_reflns.d_resolution_low': ['50.00'],
                   '_reflns.d_resolution_high': ['1.67'],
                   '_reflns.test': ["9999"]},
                  }
                 }

        d_template = {'pdbx_database_status':
                      {'_pdbx_database_status.entry_id': ['ToBeAssigned'],
                       '_pdbx_database_status.dep_release_code_coordinates': ['HOLD FOR PUBLICATION'],
                       '_pdbx_database_status.dep_release_code_sequence': ['HOLD FOR RELEASE']
                       },
                      'pdbx_audit_support':
                          {'_pdbx_audit_support.funding_organization': ['National Institutes of Health/National Institute of General Medical Sciences'],
                           '_pdbx_audit_support.country': ['United States'],
                           '_pdbx_audit_support.grant_number': ['XX000000']
                           },
                      'software':
                      {"_software.name": ['test1', 'test2'],
                       "_software.classification": ["data reduction", "refinement"],
                       "_software.version": ["v1", "v2"]
                       }
                      }
        d_software_author = {"_software.name": ["DENZO", "SCALEPACK", "phenix"],
                             "_software.classification": ["data reduction", "data scaling", "refinement"],
                             "_software.test": ["test1", "test2", "test3"],
                             "_software.citation_id": ["1", "2", "3"]
                             }

        merger = Merger()
        merger.readModel(filepath_in)
        merger.truncateMaxitCat()

        merger.mergeLog(d_log)
        merger.mergeTemplate(d_template)
        merger.processSoftwareXRAY(d_software_author)

        merger.addRefine()
        merger.write(filepath_out)

        self.assertTrue(os.path.isfile(filepath_out))
        self.assertTrue(filecmp.cmp(filepath_out, filepath_ref))

        try:
            os.remove(filepath_out)
        except FileNotFoundError:
            pass

    def testMergeEMCifOutput(self):
        folder = os.path.join(
            self.test_data, "EM_Phenix_2023_2_13_13_11_1069")
        filename_in = "maxit_out_mod.cif"
        filename_out = "merged.cif"
        filename_ref = "merged.cif_ref"
        filepath_in = os.path.join(folder, filename_in)
        filepath_out = os.path.join(folder, filename_out)
        filepath_ref = os.path.join(folder, filename_ref)

        d_log = {'scaling':
                 {'reflns':
                  {'_reflns.entry_id': ['UNNAMED'],
                   '_reflns.pdbx_diffrn_id': ['1'],
                   '_reflns.pdbx_ordinal': ['1'],
                   '_reflns.d_resolution_low': ['50.00'],
                   '_reflns.d_resolution_high': ['1.67'],
                   '_reflns.test': ["9999"]},
                  }
                 }

        d_template = {'pdbx_database_status':
                      {'_pdbx_database_status.entry_id': ['ToBeAssigned'],
                       '_pdbx_database_status.dep_release_code_coordinates': ['HOLD FOR PUBLICATION'],
                       '_pdbx_database_status.dep_release_code_sequence': ['HOLD FOR RELEASE']
                       },
                      '_pdbx_audit_support':
                          {'_pdbx_audit_support.funding_organization': ['National Institutes of Health/National Institute of General Medical Sciences'],
                           '_pdbx_audit_support.country': ['United States'],
                           '_pdbx_audit_support.grant_number': ['XX000000']
                           }
                      }
        d_software_author = {"_em_software.name": ["EMAN", "EMfit"],
                             "_em_software.category": ["MODEL REFINEMENT", "MODEL FITTING"],
                             "_em_software.version": ["1", "2"],
                             "_em_software.test": ["test1", "test2"]
                             }

        merger = Merger()
        merger.readModel(filepath_in)
        merger.truncateMaxitCat()
        # merger.addCat(d_software)

        merger.mergeLog(d_log)
        merger.mergeTemplate(d_template)
        merger.processSoftwareEM(d_software_author)

        merger.write(filepath_out)

        self.assertTrue(os.path.isfile(filepath_out))
        self.assertTrue(filecmp.cmp(filepath_out, filepath_ref))

        try:
            os.remove(filepath_out)
        except FileNotFoundError:
            pass


if __name__ == "__main__":
    unittest.main()
