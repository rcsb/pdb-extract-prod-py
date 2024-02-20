#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2023-12-01
# Updates:
#
# =============================================================================
"""
Extract scaling statistics from cctbx.xfel log file
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
    logging.info("cctbx.xfel version: %s" % version)

    if version:
        pass
    else:
        logger.info("import general parser")
        from extract.extract_log.XRAY.scaling.cctbxxfel import cctbxxfel as parser_general
        log = parser_general.LogCctbx_xfel()        
    try:
        if log.parse(filepath):
            return log.d_
        else:
            return {}
    except Exception as e:
        logger.exception(e)
