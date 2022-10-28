#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2021-12-06
# Updates:
#   2022-06-07 CS refactor
# =============================================================================
"""
Merge log data and template data into model
Priority: model > template > log
"""
from extract.pdbx_v2.PdbxReader import PdbxReader
from extract.pdbx_v2.DataCategory import DataCategory
from extract.pdbx_v2.PdbxWriter import PdbxWriter
from extract.util.convertCatDataFormat import convertDictToCatObj, convertCatObjToDict

import logging
logger_name = '.'.join(["PDB_EX", __name__])
logger = logging.getLogger(logger_name)

class Merger():
    """ Class to merge log data and template data into converted model file
    """

    def __init__(self):
        self.l_dc = None  # container list for model file
        self.dc0 = None  # container for the 1st data section of model file

    def readModel(self, filepath_model):
        """
        Read model file data into class variables

        Parameters
        ----------
        filepath_model : str
            filepath of converted model file after running maxit.

        Returns
        -------
        None.

        """
        try:
            with open(filepath_model) as file:
                reader = PdbxReader(file)
                logger.debug("Merge starts by opening converted file at %s" %
                             filepath_model)
                try:
                    self.l_dc = []
                    reader.read(self.l_dc)
                    self.dc0 = self.l_dc[0]
                    logger.info("Read converted model file into merger")
                except Exception as e:
                    logger.exception(e)
        except IOError as e:
            logger.exception(e)

    def addCat(self, d_cat):
        """
        Add data category to model container, based on cat dictionary
        If the category object exists in model, replace it with the d_cat

        Parameters
        ----------
        d_cat : dict
            cat dictionary with keys of mmcif items for the category, and
            values as list for each key.

        Returns
        -------
        bool
            True for successful addition.

        """
        cat_obj = convertDictToCatObj(d_cat)
        if cat_obj:
            self.dc0.append(cat_obj)  # add cat obj to data container
            cat_name = cat_obj.getName()
            logger.debug("added cat %s to model" % cat_name)
            return True
        else:
            logger.debug("cannot add cat %s to model" % cat_name)
            return False

    def mergeCat(self, d_cat_from, tf_replace=False):
      """
      Merge cat dictionary data into the current data category in model

      Parameters
      ----------
      d_cat_from : dict
         cat dictionary with keys of mmcif items for the category, and
         values as list for each key.

      Returns
      -------
      bool
         True for successful merge.

      """
      cat_name = list(d_cat_from.keys())[0].split('.')[0].strip('_')
      logger.info("merge log/template data into category %s" % cat_name)
      l_items = list(d_cat_from.keys())
      n_rows = len(list(d_cat_from.values())[0])

      if cat_name not in self.dc0.getObjNameList():
         return self.addCat(d_cat_from)
		  
      cat_obj_in_model = self.dc0.getObj(cat_name)
      l_items_in_model = cat_obj_in_model.getItemNameList()
      n_rows_in_model = cat_obj_in_model.getRowCount()

      if n_rows != n_rows_in_model:
         logger.info("different number of data rows between converted\
                  model files and parsed log/template on %s,\
                  no merge" % cat_name)
         return False

      l_items_to_add = []
      for item in l_items:
         if item not in l_items_in_model:
            l_items_to_add.append(item)
      if not l_items_to_add:
         logger.info("all data items in parsed log/template are present in\
                  converted model file on %s " % cat_name)
         if not tf_replace:
            return False 

      logger.info("merging data items %r to model" % l_items_to_add)
      d_cat_in_model = convertCatObjToDict(cat_obj_in_model)
      if d_cat_in_model:
         if tf_replace:
            for item in l_items_in_model:
               if item in d_cat_from:
                  d_cat_in_model[item] = d_cat_from[item]
         for item in l_items_to_add:
            d_cat_in_model[item] = d_cat_from[item]
      else:
         logger.debug("cannot process cat %s in model file, merge stopped" % cat_name)
         return False
      cat_obj_updated = convertDictToCatObj(d_cat_in_model)
      if not cat_obj_updated:
         logger.debug("cannot converted merged cat %s" % cat_name)
      self.dc0.replace(cat_obj_updated)
      logger.debug("merged cat %s to model OK")
      return True

    def mergeLog(self, d_log):
        """
        Merge parsed log meta data of all process into model container.
        Choose model data over log data if in conflict

        Parameters
        ----------
        d_log : dict
            log data in 3-level dictionary.
            d_log[process]: 1st-level key is the process.
            d_log[process][category]: 2nd-level key is the category name without underscore
            d_log[process][category] is cat dictionary with keys of mmcif items
            for the category, and values as list for each key.


        Returns
        -------
        bool
            True for successful process of log merge process for at least 1 cat

        """
        if not d_log:
            logger.info("No log data parsed, no merge")
            return None

        tf_log_data_exist = False
        n_merged_cat = 0
        for process in d_log:
            d_process = d_log[process]
            if d_process:
                tf_log_data_exist = True
            else:
                logger.info("No log data parsed for process %s" % process)
                continue
            
            for cat_name in d_process:
                logger.info("processing log data for %s" % cat_name)
                d_cat = d_process[cat_name]
                if cat_name in self.dc0.getObjNameList():
                    if self.mergeCat(d_cat):
                        logger.info("merged log data for %s OK" % cat_name)
                        n_merged_cat += 1
                    else:
                        logger.info("failed merging log data for %s" % cat_name)
                else:
                    if self.addCat(d_cat):
                        logger.info("added log data for %s OK" % cat_name)
                        n_merged_cat += 1
                    else:
                        logger.info("failed adding log data for %s" % cat_name)
        if tf_log_data_exist:
            if not n_merged_cat:
                logger.info("no data category was merged/added from log to model")
                return False
            else:
                logger.info("merged/added %s categories from log to model" % n_merged_cat)
                return True
        else:
            return None

    def mergeTemplate(self, d_template):
        """
        Merge parsed template meta data into model container.
        Choose model data over template data if in conflict.

        Parameters
        ----------
        d_template : dict
            template data in 2-level dictionary.
            d_template[category]: key is the category name without underscore
            d_template[category] is cat dictionary with keys of mmcif items
            for the category, and values as list for each key.

        Returns
        -------
        None.

        """

        if not d_template:
            logger.info("No template data parsed, no merge")            
            return None
        n_merged_cat = 0
        for cat_name in d_template:
            d_cat = d_template[cat_name]
            if cat_name in self.dc0.getObjNameList():
                if self.mergeCat(d_cat):
                    logger.info("merged template data for %s OK" % cat_name)
                    n_merged_cat += 1
                else:
                    logger.info("failed merging template data for %s" % cat_name)
            else:
                if self.addCat(d_cat):
                    logger.info("added template data for %s OK" % cat_name)
                    n_merged_cat += 1
                else:
                    logger.info("failed adding template data for %s" % cat_name)
        if not n_merged_cat:
            logger.info("no data category was merged/added from template to model")
            return False
        else:
            logger.info("merged/added %s categories from template to model" % n_merged_cat)
            return True
        
    def addRefine(self):
        if "refine" in self.dc0.getObjNameList():
            logger.info("refine cat already in the model")
            return False
        d_refine = {}
        d_refine["_refine.pdbx_refine_id"] = ["X-RAY DIFFRACTION"]
        d_refine["_refine.pdbx_diffrn_id"] = ['1']
        if self.addCat(d_refine):
            logger.info("added empty refine cat")
            return True
        else:
            logger.info("failed adding empty refine cat")
            return False

    def truncateMaxitCat(self):
        l_cat_to_keep = ["atom_site",
                         "atom_site_anisotrop",
                         "atom_sites",
                         "cell",
                         "symmetry",
                         "refine",
                         "refine_ls_restr",
                         "refine_ls_shell",
                         "pdbx_refine_tls",
                         "pdbx_refine_tls_group",
                         "refine_analyze",
                         "refine_hist",
                         "refine_ls_restr_ncs"
                         ]
        # l_cat_to_remove = ["pdbx_database_status",
        #                    "entity_poly_seq",
        #                    "entity",
        #                    "pdbx_poly_seq_scheme",
        #                    "pdbx_nonpoly_scheme",
        #                    "chem_comp",
        #                    "struct_asym",
        #                    "pdbx_validate_close_contact",
        #                    "pdbx_validate_torsion",
        #                    "pdbx_unobs_or_zero_occ_atoms",
        #                    "atom_type",
        #                    "pdbx_entity_nonpoly"
        #                    ]
        l_cat = []  # must create a separate list to go though during deletion
        for each in self.dc0.getObjNameList():
            l_cat.append(each)

        for cat_name in l_cat:  # cannot use "for cat_name in self.dc0.getObjNameList() because of deletion will mess up iteration"
            if cat_name not in l_cat_to_keep:
                self.dc0.remove(cat_name)
        # print(self.dc0.getObjNameList())

    def write(self, filepath_out):
        """
        Write the current data container list into a file

        Parameters
        ----------
        filepath_out : str
            output filepath.

        Returns
        -------
        None.

        """
        try:
            file = open(filepath_out, 'w')
        except IOError as e:
            logger.exception(e)
        else:
            try:
                writer = PdbxWriter(file)
                writer.write(self.l_dc)
            except Exception as e:
                logger.exception(e)
        finally:
            file.close()
            logger.info("wrote merged model data to file %s" % filepath_out)


def main():
    #filepath_model = '/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_Template_Scalepack_1/maxit.cif'
    #filepath_out = '/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_Template_Scalepack_1/merged.cif'
    filepath_model = '/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_XDS_Aimless_Phaser_Phenix_2021_10_8_18_16442/maxit.cif'
    filepath_out = '/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_XDS_Aimless_Phaser_Phenix_2021_10_8_18_16442/merged.cif'

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
    d_software = {"_software.name": ["DENZO", "SCALEPACK"],
                  "_software.classification":["data reduction", "data scaling"]
                  }
    merger = Merger()
    merger.readModel(filepath_model)
    merger.truncateMaxitCat()
    merger.addCat(d_software)

    merger.mergeLog(d_log)
    merger.mergeTemplate(d_template)

    merger.addRefine()
    merger.write(filepath_out)


if __name__ == "__main__":
    main()
