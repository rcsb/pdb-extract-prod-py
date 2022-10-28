#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-30
# Updates:
#   2022-06-10 CS refactor
# =============================================================================
"""
Extract scaling statistics from DIALS log file
Use Xia2 parser
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
    logging.info("Xia2 version: %s" % version)

    if version:
        pass
    else:
        logger.info("import general parser")
        from extract.extract_log.XRAY.scaling.xia2 import xia2 as parser_general
        log = parser_general.LogXia2()        
    try:
        if log.parse(filepath):
            return log.d_
        else:
            return {}
    except Exception as e:
        logger.exception(e)

def main():
    filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_Xia2long_2021_9_18_5_1293/file_scl_1"
    d_ = run(filepath)
    print(d_)    

    filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_Xia2short_2021_10_9_7_7004/file_scl_1"
    d_ = run(filepath)
    print(d_)    

if __name__ == "__main__":
    main()