#!/usr/bin/env python3
# =============================================================================
# Author:  Chenghua Shao
# Date:    2021-11-21
# Updates:
#   2022-06-10 CS refactor
# =============================================================================
"""
Initiate data dictionary for scaling process for all programs
"""


class LogScaling():
    """class of scaling log, read template to create empty class dict
    """

    def __init__(self):
        self.d_ = {'reflns': {'_reflns.entry_id': [], 
                               '_reflns.pdbx_diffrn_id': [], 
                               '_reflns.pdbx_ordinal': [], 
                               '_reflns.observed_criterion_sigma_I': [], 
                               '_reflns.observed_criterion_sigma_F': [], 
                               '_reflns.d_resolution_low': [], 
                               '_reflns.d_resolution_high': [], 
                               '_reflns.number_obs': [], 
                               '_reflns.number_all': [], 
                               '_reflns.percent_possible_obs': [], 
                               '_reflns.pdbx_Rmerge_I_obs': [], 
                               '_reflns.pdbx_Rsym_value': [], 
                               '_reflns.pdbx_netI_over_sigmaI': [], 
                               '_reflns.B_iso_Wilson_estimate': [], 
                               '_reflns.pdbx_redundancy': [], 
                               '_reflns.pdbx_Rrim_I_all': [], 
                               '_reflns.pdbx_Rpim_I_all': [], 
                               '_reflns.pdbx_CC_half': [], 
                               '_reflns.pdbx_netI_over_av_sigmaI': [], 
                               '_reflns.pdbx_number_measured_all': [], 
                               '_reflns.pdbx_scaling_rejects': [], 
                               '_reflns.pdbx_chi_squared': [], 
                               '_reflns.Rmerge_F_all': [], 
                               '_reflns.Rmerge_F_obs': [], 
                               '_reflns.observed_criterion_F_max': [], 
                               '_reflns.observed_criterion_F_min': [], 
                               '_reflns.observed_criterion_I_max': [], 
                               '_reflns.observed_criterion_I_min': [], 
                               '_reflns.pdbx_d_res_high_opt': [], 
                               '_reflns.pdbx_d_res_low_opt': [], 
                               '_reflns.details': [],
                               '_reflns.pdbx_R_split': [],
                               }, 
                   'reflns_shell': {'_reflns_shell.pdbx_diffrn_id': [], 
                                     '_reflns_shell.pdbx_ordinal': [], 
                                     '_reflns_shell.d_res_high': [], 
                                     '_reflns_shell.d_res_low': [], 
                                     '_reflns_shell.number_measured_obs': [], 
                                     '_reflns_shell.number_measured_all': [], 
                                     '_reflns_shell.number_unique_obs': [], 
                                     '_reflns_shell.pdbx_rejects': [], 
                                     '_reflns_shell.Rmerge_I_obs': [], 
                                     '_reflns_shell.meanI_over_sigI_obs': [], 
                                     '_reflns_shell.pdbx_Rsym_value': [], 
                                     '_reflns_shell.pdbx_chi_squared': [], 
                                     '_reflns_shell.pdbx_redundancy': [], 
                                     '_reflns_shell.percent_possible_obs': [], 
                                     '_reflns_shell.pdbx_netI_over_sigmaI_obs': [], 
                                     '_reflns_shell.number_possible': [], 
                                     '_reflns_shell.number_unique_all': [], 
                                     '_reflns_shell.Rmerge_F_all': [], 
                                     '_reflns_shell.Rmerge_F_obs': [], 
                                     '_reflns_shell.Rmerge_I_all': [], 
                                     '_reflns_shell.meanI_over_sigI_all': [], 
                                     '_reflns_shell.percent_possible_all': [], 
                                     '_reflns_shell.pdbx_Rrim_I_all': [], 
                                     '_reflns_shell.pdbx_Rpim_I_all': [], 
                                     '_reflns_shell.pdbx_CC_half': [], 
                                     '_reflns_shell.pdbx_number_anomalous': [],
                                     '_reflns_shell.pdbx_R_split': [],
                                     }
                   }


def main():
    log = LogScaling()
    print(log.d_)


if __name__ == "__main__":
    main()