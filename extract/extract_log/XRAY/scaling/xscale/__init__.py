#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2021-11-21
# Updates:
#   2022-06-10 CS refactor
# =============================================================================
"""
Extract scaling statistics from Xscale log file
"""
import logging

logger = logging.getLogger(__name__)

def checkVersion(filepath):
    """
    Check version of the software based on log file

    Parameters
    ----------
    filepath : str
        log file path.

    Returns
    -------
    version : str
        version.

    """
    version = None
    return version

def run(filepath):
    """
    Run log extraction

    Parameters
    ----------
    filepath : str
        log file path.

    Returns
    -------
    TYPE : dict
        dictionary of parsed daata.

    """
    version = checkVersion(filepath)
    logging.info("Xscale version: %s" % version)

    if version:
        pass
    else:
        logger.info("import general parser")
        from extract.extract_log.XRAY.scaling.xscale import xscale as parser_general
        log = parser_general.LogXscale()        
    try:
        if log.parse(filepath):
            return log.d_
        else:
            return {}
    except Exception as e:
        logger.exception(e)

def main():
    filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_XDS_Xscale_2021_10_11_2_16188/file_scl_1"
    d_ = run(filepath)
    print(d_)    

if __name__ == "__main__":
    main()