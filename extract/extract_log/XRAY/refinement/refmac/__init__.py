# =============================================================================
# Author:  Chenghua Shao
# Date:    2025-03-25
# Updates:
# 
# =============================================================================
"""
Extract refinement statistics from refmac log file
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
    version = None  #recent phenix outout do not differ based on version, no need to check version
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
    logging.info("Refmac version: %s" % version)

    if version:
        pass
    else:
        logger.info("import general parser")
        from extract.extract_log.XRAY.refinement.refmac import refmac as parser_general_refine
        log = parser_general_refine.LogRefmac()   
    try:
        if log.parse(filepath):
            return log.d_
        else:
            return {}
    except Exception as e:
        logger.exception(e)

def main():
    filepath = "/Users/chenghua/Projects/pdb_extract/Refine_log/refmac_5.8.0430_XRAY_2025_3_6_8_5_2837710"
    d_ = run(filepath)
    for item in d_["refine"]:
        print(item, d_["refine"][item])
    print()
    for item in d_["refine_ls_shell"]:
        print(item, d_["refine_ls_shell"][item])
    print()
    for item in d_["refine_ls_restr"]:
        print(item, d_["refine_ls_restr"][item])
    print()


if __name__ == "__main__":
    main()
