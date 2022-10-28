#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-27
# =============================================================================
"""
Extract scaling statistics from Pointless log file
Use Aimless parser
Pointless usually generates the input for Aimless during scaling so authors
might indicate either one for scaling software.
"""
import re
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
    try:
        with open(filepath) as file:
            line_1st = file.readline()
            re_html = re.compile(r"^<!doctype html")
            if re_html.search(line_1st.lower()):
                version = "html"
            else:
                re_ccp4 = re.compile(r"^ ### CCP4.+AIMLESS.+##\s*$")
                for line in file:
                    if re_ccp4.search(line):
                        version = "ccp4"
                        break
    except IOError as msg:
        logging.error(msg)

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
    # print(version)
    logging.info("Aimless version: %s" % version)

    if version == "ccp4":
        logger.info("import ccp4 versioned parser")
        from extract.extract_log.XRAY.scaling.aimless import aimless as parser_ccp4
        log = parser_ccp4.LogAimless()
    elif version == "html":
        logger.info("import html versioned parser")
        from extract.extract_log.XRAY.scaling.aimless import aimless_html as parser_html
        log = parser_html.LogAimlessHtml()
    else:
        logger.info("import general parser")
        from extract.extract_log.XRAY.scaling.aimless import aimless as parser_general
        log = parser_general.LogAimless()

    try:
        if log.parse(filepath):
            return log.d_
        else:
            return {}
    except Exception as e:
        logger.exception(e)

def main():
    filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_XDS_Aimless_Phaser_Phenix_2021_10_8_18_16442/file_scl_1"
    d_ = run(filepath)
    print(d_)
    
    print()
    
    filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_XDS_AimlessHTML_Phenix_2021_9_20_22_31146/file_scl_1"
    d_ = run(filepath)
    print(d_)    

if __name__ == "__main__":
    main()