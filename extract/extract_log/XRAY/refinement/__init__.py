# =============================================================================
# Author:  Chenghua Shao
# Date:    2025-03-22
# Updates:
# 
# =============================================================================
"""
Initiate data dictionary for refinement process for all programs
"""


class LogRefinement():
    """class of refinement log, read template to create empty class dict
    """

    def __init__(self):
        self.d_ = {
            'refine': {
                '_refine.pdbx_refine_id':	    [],
                '_refine.entry_id':	    [],
                '_refine.pdbx_diffrn_id':	    [],
                '_refine.pdbx_TLS_residual_ADP_flag':	    [],
                '_refine.ls_number_reflns_obs':	    [],
                '_refine.ls_number_reflns_all':	    [],
                '_refine.pdbx_ls_sigma_I':	    [],
                '_refine.pdbx_ls_sigma_F':	    [],
                '_refine.pdbx_data_cutoff_high_absF':	    [],
                '_refine.pdbx_data_cutoff_low_absF':	    [],
                '_refine.pdbx_data_cutoff_high_rms_absF':	    [],
                '_refine.ls_d_res_low':	    [],
                '_refine.ls_d_res_high':	    [],
                '_refine.ls_percent_reflns_obs':	    [],
                '_refine.ls_R_factor_obs':	    [],
                '_refine.ls_R_factor_all':	    [],
                '_refine.ls_R_factor_R_work':	    [],
                '_refine.ls_R_factor_R_free':	    [],
                '_refine.ls_R_factor_R_free_error':	    [],
                '_refine.ls_R_factor_R_free_error_details':	    [],
                '_refine.ls_percent_reflns_R_free':	    [],
                '_refine.ls_number_reflns_R_free':	    [],
                '_refine.ls_number_parameters':	    [],
                '_refine.ls_number_restraints':	    [],
                '_refine.occupancy_min':	    [],
                '_refine.occupancy_max':	    [],
                '_refine.correlation_coeff_Fo_to_Fc':	    [],
                '_refine.correlation_coeff_Fo_to_Fc_free':	    [],
                '_refine.B_iso_mean':	    [],
                '_refine.aniso_B[1][1]':	    [],
                '_refine.aniso_B[2][2]':	    [],
                '_refine.aniso_B[3][3]':	    [],
                '_refine.aniso_B[1][2]':	    [],
                '_refine.aniso_B[1][3]':	    [],
                '_refine.aniso_B[2][3]':	    [],
                '_refine.solvent_model_details':	    [],
                '_refine.solvent_model_param_ksol':	    [],
                '_refine.solvent_model_param_bsol':	    [],
                '_refine.pdbx_solvent_vdw_probe_radii':	    [],
                '_refine.pdbx_solvent_ion_probe_radii':	    [],
                '_refine.pdbx_solvent_shrinkage_radii':	    [],
                '_refine.pdbx_ls_cross_valid_method':	    [],
                '_refine.details':	    [],
                '_refine.pdbx_starting_model':	    [],
                '_refine.pdbx_method_to_determine_struct':	    [],
                '_refine.pdbx_isotropic_thermal_model':	    [],
                '_refine.pdbx_stereochemistry_target_values':	    [],
                '_refine.pdbx_stereochem_target_val_spec_case':	    [],
                '_refine.pdbx_R_Free_selection_details':	    [],
                '_refine.pdbx_overall_ESU_R':	    [],
                '_refine.pdbx_overall_ESU_R_Free':	    [],
                '_refine.overall_SU_ML':	    [],
                '_refine.pdbx_overall_phase_error':	    [],
                '_refine.overall_SU_B':	    [],
                '_refine.overall_SU_R_Cruickshank_DPI':	    [],
                '_refine.pdbx_overall_SU_R_free_Cruickshank_DPI':	    [],
                '_refine.pdbx_overall_SU_R_Blow_DPI':	    [],
                '_refine.pdbx_overall_SU_R_free_Blow_DPI':	    [],
            }, 
            'refine_ls_shell': {
                '_refine_ls_shell.pdbx_refine_id':	    [],
                '_refine_ls_shell.pdbx_total_number_of_bins_used':	    [],
                '_refine_ls_shell.d_res_high':	    [],
                '_refine_ls_shell.d_res_low':	    [],
                '_refine_ls_shell.number_reflns_R_work':	    [],
                '_refine_ls_shell.R_factor_R_work':	    [],
                '_refine_ls_shell.percent_reflns_obs':	    [],
                '_refine_ls_shell.R_factor_R_free':	    [],
                '_refine_ls_shell.R_factor_R_free_error':	    [],
                '_refine_ls_shell.percent_reflns_R_free':	    [],
                '_refine_ls_shell.number_reflns_R_free':	    [],
                '_refine_ls_shell.number_reflns_all':	    [],
                '_refine_ls_shell.R_factor_all':	    [],
            },
            'refine_ls_restr': {
                '_refine_ls_restr.type':	    [],
                '_refine_ls_restr.dev_ideal':	    [],
                '_refine_ls_restr.dev_ideal_target':	    [],
                '_refine_ls_restr.weight':	    [],
                '_refine_ls_restr.number':	    [],
                '_refine_ls_restr.pdbx_refine_id':	    [],
                '_refine_ls_restr.pdbx_restraint_function':	    [],
            },
        }
        #     'refine_hist': {
        #         '_refine_hist.pdbx_refine_id':	    [],
        #         '_refine_hist.cycle_id':	    [],
        #         '_refine_hist.pdbx_number_atoms_protein':	    [],
        #         '_refine_hist.pdbx_number_atoms_nucleic_acid':	    [],
        #         '_refine_hist.pdbx_number_atoms_ligand':	    [],
        #         '_refine_hist.number_atoms_solvent':	    [],
        #         '_refine_hist.number_atoms_total':	    [],
        #         '_refine_hist.d_res_high':	    [],
        #         '_refine_hist.d_res_low':	    [],
        #     },
        # }


# def main():
#     log = LogRefinement()
#     print(log.d_)


# if __name__ == "__main__":
#     main()