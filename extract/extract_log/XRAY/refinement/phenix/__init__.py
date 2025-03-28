# =============================================================================
# Author:  Chenghua Shao
# Date:    2025-03-22
# Updates:
# 
# =============================================================================
"""
Extract refinement statistics from phenix log file
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
    logging.info("Phenix version: %s" % version)

    if version:
        pass
    else:
        logger.info("import general parser")
        from extract.extract_log.XRAY.refinement.phenix import phenix as parser_general_refine
        log = parser_general_refine.LogPhenix()        
    try:
        if log.parse(filepath):
            return log.d_
        else:
            return {}
    except Exception as e:
        logger.exception(e)

def main():
    filepath = "/Users/chenghua/Projects/pdb_extract/Refine_log/phenix_1.21.2_XRAY_2025_2_27_3_9_2670933"
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
