#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-25
# Updates:
#   2022-06-10 CS refactor
# =============================================================================
"""
Extract scaling statistics from HKL-3000 log file
Use the same parser for Scalepack
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
    logging.info("HKL-3000 version: %s" % version)

    if version:
        pass
    else:
        logger.info("import general parser")
        from extract.extract_log.XRAY.scaling.scalepack import scalepack as parser_general
        log = parser_general.LogScalepack()

    try:
        if log.parse(filepath):
            return log.d_
        else:
            return {}
    except Exception as e:
        logger.exception(e)

def main():
    filepath = "/Users/chenghua/Projects/pdb-extract-prod-py/tests/test_data/PDB_HKL2000_Phaser_Refmac_2021_9_28_13_26368/file_scl_1"
    d_ = run(filepath)
    for item in d_["reflns"]:
        print(item, d_["reflns"][item])
    print()
    for item in d_["reflns_shell"]:
        print(item, d_["reflns_shell"][item])


if __name__ == "__main__":
    main()
