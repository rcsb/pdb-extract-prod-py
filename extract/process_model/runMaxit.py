# File:    convertModel.py
# Author:  Chenghua Shao
# Date:    2021-12-07
# Version: 1.0
# Updates:
#   2022-06-06 CS refactor, use direct args input, add tracking dictionary
"""
run pre-installed maxit command tool
"""
__docformat__ = "restructuredtext en"
__author__ = "Chenghua Shao"
__email__ = "chenghua.shao@rcsb.org"
__license__ = "Apache 2.0"

import os
import subprocess


class Maxit:
    """ Class to run maxit
    """
    def __init__(self):
        """
        Set up maxit path, command, and run env

        Returns
        -------
        None.

        """
        maxit_dir = os.getenv("RCSBROOT")
        self.maxit_command = os.path.join(maxit_dir, "bin", "maxit")

    def pdb2cif(self, filepath_input, filepath_output, filepath_log):
        """
        Run PDB to CIF conversion

        Parameters
        ----------
        filepath_input : str
            PDB model input filepath.
        filepath_output : str
            mmCIF model output filepath.
        filepath_log : str
            maxit log filepath.

        Returns
        -------
        integer
            return status code, only zero indicates successful maxit run.

        """
        maxit_run = subprocess.run([os.path.join(self.maxit_command),
                                    "-input", filepath_input,
                                    "-output", filepath_output,
                                    "-o", "1",
                                    "-log", filepath_log])
        return maxit_run.returncode

    def cif2cif(self, filepath_input, filepath_output, filepath_log):
        """
        Run CIF to CIF conversion

        Parameters
        ----------
        filepath_input : str
            CIF model input filepath.
        filepath_output : str
            mmCIF model output filepath.
        filepath_log : str
            maxit log filepath.

        Returns
        -------
        integer
            return status code, only zero indicates successful maxit run.

        """
        maxit_run = subprocess.run([os.path.join(self.maxit_command),
                                    "-input", filepath_input,
                                    "-output", filepath_output,
                                    "-o", "8",
                                    "-log", filepath_log])
        return maxit_run.returncode
