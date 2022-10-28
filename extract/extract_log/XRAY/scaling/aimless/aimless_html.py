# =============================================================================
# Author:  Chenghua Shao
# Date:    2022-07-28
# =============================================================================
"""
Extract scaling statistics from Aimless log fille.
Deal with Aimless HTML output
"""

import re
import logging
# from extract.extract_log.XRAY.scaling.aimless.aimless import LogAimless
from aimless import LogAimless

logger = logging.getLogger(__name__)


class LogAimlessHtml(LogAimless):
    def __init__(self):
        super().__init__()

    def parseSummary(self):
        """
        Parse summary.

        Returns
        -------
        None.

        """
        pattern = r'^Summary\s+data\s+for\s+Project:\s+'
        i_start = self.getStartingIndex(pattern)
        i_end = i_start + 21 # truncate the summary section
        l_summary_section = self.l_file[i_start:i_end]
        # print(l_summary_section)
        d_re = {}
        d_re["Low resolution limit"] = ("_reflns.d_resolution_low", '_reflns_shell.d_res_low')
        d_re["High resolution limit"] = ("_reflns.d_resolution_high", '_reflns_shell.d_res_high')
        d_re["Total number unique"] = ("_reflns.number_obs", '_reflns_shell.number_unique_obs')
        d_re["Completeness"] = ("_reflns.percent_possible_obs", '_reflns_shell.percent_possible_obs')
        d_re["Rmerge \(all I\+ and I\-\)"] = ("_reflns.pdbx_Rmerge_I_obs", '_reflns_shell.Rmerge_I_obs')
        d_re["Mean\(\(I\)\/sd\(I\)\)"] = ("_reflns.pdbx_netI_over_sigmaI", '_reflns_shell.pdbx_netI_over_sigmaI_obs')
        d_re["Multiplicity"] = ("_reflns.pdbx_redundancy", '_reflns_shell.pdbx_redundancy')
        d_re["Rmeas \(all I\+ \&amp\; I\-\)"] = ("_reflns.pdbx_Rrim_I_all", '_reflns_shell.pdbx_Rrim_I_all')
        d_re["Rpim \(all I\+ \&amp\; I\-\)"] = ("_reflns.pdbx_Rpim_I_all", '_reflns_shell.pdbx_Rpim_I_all')
        d_re["Mn\(I\) half-set correlation CC\(1\/2\)"] = ("_reflns.pdbx_CC_half", '_reflns_shell.pdbx_CC_half')
        d_re["Total number of observations"] = ("_reflns.pdbx_number_measured_all", '_reflns_shell.number_measured_all')
        d_re["Mean\(Chi\^2\)"] = ("_reflns.pdbx_chi_squared", '_reflns_shell.pdbx_chi_squared')

        for each in d_re:
            re_ = re.compile(r"^\s*<tr><th>%s\s+</th><td>(\d+\.?\d+)</td><td>(\d+.?\d+)</td><td>(\d+.?\d+)</td></tr>\s*$" % each)
            # re_ = re.compile(r"%s" % each)
            for line in l_summary_section:
                if re_.search(line):
                    try:
                        self.d_["reflns"][d_re[each][0]].append(re_.search(line).groups()[0])
                        self.d_["reflns_shell"][d_re[each][1]].append(re_.search(line).groups()[2])
                        break
                    except IndexError as msg:
                        logger.warning(msg)


def main():
    filepath = "/Users/chenghua/Projects/pdb_extract/tests/test_data/PDB_XDS_AimlessHTML_Phenix_2021_9_20_22_31146/file_scl_1"
    log = LogAimlessHtml()
    log.parse(filepath)
    print(log.d_)
 

if __name__ == "__main__":
    main()