# ==========================================
# AUTO-GENERATED PBPK MODEL
# Route: oral | Metabolism: mm
# Species: human, rat
# ==========================================
if (!require('deSolve')) {
  install.packages('deSolve', repos='http://cran.us.r-project.org')
  library(deSolve)
}

# --- GLOBAL / BIOCHEMICAL PARAMETERS ---
global_params <- list(
  fu = 10.0,
  Vmax = 80.0,
  Km = 2.86,
  GE = 2.5,
  Kabs = 0.5,
  K_feces = 0.01
)

# ==========================================
# HUMAN PBPK MODEL
# ==========================================
params_human <- unlist(list(
  BW = 70.0,
  Qc = 372.0,
  fu = global_params$fu,
  Vmax = global_params$Vmax,
  Km = global_params$Km,
  GE = global_params$GE,
  Kabs = global_params$Kabs,
  K_feces = global_params$K_feces,
  Q_brain_human = 0.114,
  Q_brain_rat = 0.114,
  Q_diaphragm_human = 0.006,
  Q_diaphragm_rat = 0.006,
  Q_fat_human = 0.052,
  Q_fat_rat = 0.052,
  Q_liver_human = 0.23,
  Q_liver_rat = 0.25,
  Q_rapidly_perfused_human = 0.4,
  Q_rapidly_perfused_rat = 0.426,
  Q_skin_human = 0.058,
  Q_skin_rat = 0.058,
  Q_slowly_perfused_human = 0.14,
  Q_slowly_perfused_rat = 0.14,
  Q_liver = 0.227,
  Q_rest = max(0, 1.0 - 2.273),
  V_brain_human = 0.07,
  V_brain_rat = 0.06,
  V_diaphragm_human = 0.0003,
  V_diaphragm_rat = 0.0003,
  V_fat_human = 0.052,
  V_fat_rat = 0.09,
  V_liver_human = 0.21,
  V_liver_rat = 0.07,
  V_rapidly_perfused_human = 0.04,
  V_rapidly_perfused_rat = 0.04,
  V_slowly_perfused_human = 0.63,
  V_slowly_perfused_rat = 0.78,
  V_liver = 0.026,
  V_rest = max(0.05, 1.0 - (2.0686 + 0.04)),
  P_brain_human = 1.0,
  P_brain_rat = 1.0,
  P_diaphragm_human = 1.0,
  P_diaphragm_rat = 1.0,
  P_fat_human = 1.0,
  P_fat_rat = 1.0,
  P_liver_human = 1.0,
  P_liver_rat = 1.0,
  P_rapidly_perfused_human = 1.0,
  P_rapidly_perfused_rat = 1.0,
  P_skin_human = 1.0,
  P_skin_rat = 1.0,
  P_slowly_perfused_human = 1.0,
  P_slowly_perfused_rat = 1.0,
  P_liver = 1.0,
  P_rest = 1.0
))

pbpk_ode_human <- function(t, state, parms) {
  with(as.list(c(state, parms)), {
    Q_brain_human_abs <- Q_brain_human * Qc
    V_brain_human_abs <- V_brain_human * BW
    Cv_brain_human <- C_brain_human / P_brain_human
    Q_brain_rat_abs <- Q_brain_rat * Qc
    V_brain_rat_abs <- V_brain_rat * BW
    Cv_brain_rat <- C_brain_rat / P_brain_rat
    Q_diaphragm_human_abs <- Q_diaphragm_human * Qc
    V_diaphragm_human_abs <- V_diaphragm_human * BW
    Cv_diaphragm_human <- C_diaphragm_human / P_diaphragm_human
    Q_diaphragm_rat_abs <- Q_diaphragm_rat * Qc
    V_diaphragm_rat_abs <- V_diaphragm_rat * BW
    Cv_diaphragm_rat <- C_diaphragm_rat / P_diaphragm_rat
    Q_fat_human_abs <- Q_fat_human * Qc
    V_fat_human_abs <- V_fat_human * BW
    Cv_fat_human <- C_fat_human / P_fat_human
    Q_fat_rat_abs <- Q_fat_rat * Qc
    V_fat_rat_abs <- V_fat_rat * BW
    Cv_fat_rat <- C_fat_rat / P_fat_rat
    Q_liver_human_abs <- Q_liver_human * Qc
    V_liver_human_abs <- V_liver_human * BW
    Cv_liver_human <- C_liver_human / P_liver_human
    Q_liver_rat_abs <- Q_liver_rat * Qc
    V_liver_rat_abs <- V_liver_rat * BW
    Cv_liver_rat <- C_liver_rat / P_liver_rat
    Q_rapidly_perfused_human_abs <- Q_rapidly_perfused_human * Qc
    V_rapidly_perfused_human_abs <- V_rapidly_perfused_human * BW
    Cv_rapidly_perfused_human <- C_rapidly_perfused_human / P_rapidly_perfused_human
    Q_rapidly_perfused_rat_abs <- Q_rapidly_perfused_rat * Qc
    V_rapidly_perfused_rat_abs <- V_rapidly_perfused_rat * BW
    Cv_rapidly_perfused_rat <- C_rapidly_perfused_rat / P_rapidly_perfused_rat
    Q_skin_human_abs <- Q_skin_human * Qc
    V_skin_human_abs <- V_skin_human * BW
    Cv_skin_human <- C_skin_human / P_skin_human
    Q_skin_rat_abs <- Q_skin_rat * Qc
    V_skin_rat_abs <- V_skin_rat * BW
    Cv_skin_rat <- C_skin_rat / P_skin_rat
    Q_slowly_perfused_human_abs <- Q_slowly_perfused_human * Qc
    V_slowly_perfused_human_abs <- V_slowly_perfused_human * BW
    Cv_slowly_perfused_human <- C_slowly_perfused_human / P_slowly_perfused_human
    Q_slowly_perfused_rat_abs <- Q_slowly_perfused_rat * Qc
    V_slowly_perfused_rat_abs <- V_slowly_perfused_rat * BW
    Cv_slowly_perfused_rat <- C_slowly_perfused_rat / P_slowly_perfused_rat
    Q_liver_abs <- Q_liver * Qc
    V_liver_abs <- V_liver * BW
    Cv_liver <- C_liver / P_liver
    Q_rest_abs <- Q_rest * Qc
    V_rest_abs <- V_rest * BW
    Cv_rest <- C_rest / P_rest
    Cv_mix <- (Q_brain_human_abs * Cv_brain_human + Q_brain_rat_abs * Cv_brain_rat + Q_diaphragm_human_abs * Cv_diaphragm_human + Q_diaphragm_rat_abs * Cv_diaphragm_rat + Q_fat_human_abs * Cv_fat_human + Q_fat_rat_abs * Cv_fat_rat + Q_liver_human_abs * Cv_liver_human + Q_liver_rat_abs * Cv_liver_rat + Q_rapidly_perfused_human_abs * Cv_rapidly_perfused_human + Q_rapidly_perfused_rat_abs * Cv_rapidly_perfused_rat + Q_skin_human_abs * Cv_skin_human + Q_skin_rat_abs * Cv_skin_rat + Q_slowly_perfused_human_abs * Cv_slowly_perfused_human + Q_slowly_perfused_rat_abs * Cv_slowly_perfused_rat + Q_liver_abs * Cv_liver + Q_rest_abs * Cv_rest) / Qc
    C_art <- Cv_mix

    # --- Metabolism in Liver ---
    Vmet <- (Vmax * C_liver * fu) / (Km + C_liver * fu)

    # --- GI Tract Absorption (oral) ---
    dAmount_stomach <- -GE * Amount_stomach
    dAmount_gut <- GE * Amount_stomach - Kabs * Amount_gut - K_feces * Amount_gut

    # --- Organ Concentration ODEs ---
    dC_brain_human <- (Q_brain_human_abs * (C_art - Cv_brain_human)) / V_brain_human_abs
    dC_brain_rat <- (Q_brain_rat_abs * (C_art - Cv_brain_rat)) / V_brain_rat_abs
    dC_diaphragm_human <- (Q_diaphragm_human_abs * (C_art - Cv_diaphragm_human)) / V_diaphragm_human_abs
    dC_diaphragm_rat <- (Q_diaphragm_rat_abs * (C_art - Cv_diaphragm_rat)) / V_diaphragm_rat_abs
    dC_fat_human <- (Q_fat_human_abs * (C_art - Cv_fat_human)) / V_fat_human_abs
    dC_fat_rat <- (Q_fat_rat_abs * (C_art - Cv_fat_rat)) / V_fat_rat_abs
    dC_liver_human <- (Q_liver_human_abs * (C_art - Cv_liver_human)) / V_liver_human_abs
    dC_liver_rat <- (Q_liver_rat_abs * (C_art - Cv_liver_rat)) / V_liver_rat_abs
    dC_rapidly_perfused_human <- (Q_rapidly_perfused_human_abs * (C_art - Cv_rapidly_perfused_human)) / V_rapidly_perfused_human_abs
    dC_rapidly_perfused_rat <- (Q_rapidly_perfused_rat_abs * (C_art - Cv_rapidly_perfused_rat)) / V_rapidly_perfused_rat_abs
    dC_skin_human <- (Q_skin_human_abs * (C_art - Cv_skin_human)) / V_skin_human_abs
    dC_skin_rat <- (Q_skin_rat_abs * (C_art - Cv_skin_rat)) / V_skin_rat_abs
    dC_slowly_perfused_human <- (Q_slowly_perfused_human_abs * (C_art - Cv_slowly_perfused_human)) / V_slowly_perfused_human_abs
    dC_slowly_perfused_rat <- (Q_slowly_perfused_rat_abs * (C_art - Cv_slowly_perfused_rat)) / V_slowly_perfused_rat_abs
    dC_liver <- (Q_liver_abs * (C_art - Cv_liver) + Kabs * Amount_gut + - Vmet) / V_liver_abs
    dC_rest <- (Q_rest_abs * (C_art - Cv_rest)) / V_rest_abs

    return(list(c(dAmount_stomach, dAmount_gut, dC_brain_human, dC_brain_rat, dC_diaphragm_human, dC_diaphragm_rat, dC_fat_human, dC_fat_rat, dC_liver_human, dC_liver_rat, dC_rapidly_perfused_human, dC_rapidly_perfused_rat, dC_skin_human, dC_skin_rat, dC_slowly_perfused_human, dC_slowly_perfused_rat, dC_liver, dC_rest)))
  })
}

# --- Human Simulation ---
init_human <- c(
  Amount_stomach = 50.0, Amount_gut = 0, C_brain_human = 0, C_brain_rat = 0, C_diaphragm_human = 0, C_diaphragm_rat = 0, C_fat_human = 0, C_fat_rat = 0, C_liver_human = 0, C_liver_rat = 0, C_rapidly_perfused_human = 0, C_rapidly_perfused_rat = 0, C_skin_human = 0, C_skin_rat = 0, C_slowly_perfused_human = 0, C_slowly_perfused_rat = 0, C_liver = 0, C_rest = 0
)
times <- seq(0, 24, by = 0.1)
out_human <- as.data.frame(ode(y = init_human, times = times, func = pbpk_ode_human, parms = params_human))
write.csv(out_human, file = 'human_simulation_results.csv', row.names = FALSE)
print('Human PBPK Simulation complete! Saved to human_simulation_results.csv')

# ==========================================
# RAT PBPK MODEL
# ==========================================
params_rat <- unlist(list(
  BW = 0.25,
  Qc = 14.0,
  fu = global_params$fu,
  Vmax = global_params$Vmax,
  Km = global_params$Km,
  GE = global_params$GE,
  Kabs = global_params$Kabs,
  K_feces = global_params$K_feces,
  Q_brain_human = 0.114,
  Q_brain_rat = 0.114,
  Q_diaphragm_human = 0.006,
  Q_diaphragm_rat = 0.006,
  Q_fat_human = 0.052,
  Q_fat_rat = 0.052,
  Q_liver_human = 0.23,
  Q_liver_rat = 0.25,
  Q_rapidly_perfused_human = 0.4,
  Q_rapidly_perfused_rat = 0.426,
  Q_skin_human = 0.058,
  Q_skin_rat = 0.058,
  Q_slowly_perfused_human = 0.14,
  Q_slowly_perfused_rat = 0.14,
  Q_liver = 0.183,
  Q_rest = max(0, 1.0 - 2.229),
  V_brain_human = 0.07,
  V_brain_rat = 0.06,
  V_diaphragm_human = 0.0003,
  V_diaphragm_rat = 0.0003,
  V_fat_human = 0.052,
  V_fat_rat = 0.09,
  V_liver_human = 0.21,
  V_liver_rat = 0.07,
  V_rapidly_perfused_human = 0.04,
  V_rapidly_perfused_rat = 0.04,
  V_slowly_perfused_human = 0.63,
  V_slowly_perfused_rat = 0.78,
  V_liver = 0.034,
  V_rest = max(0.05, 1.0 - (2.0766 + 0.04)),
  P_brain_human = 1.0,
  P_brain_rat = 1.0,
  P_diaphragm_human = 1.0,
  P_diaphragm_rat = 1.0,
  P_fat_human = 1.0,
  P_fat_rat = 1.0,
  P_liver_human = 1.0,
  P_liver_rat = 1.0,
  P_rapidly_perfused_human = 1.0,
  P_rapidly_perfused_rat = 1.0,
  P_skin_human = 1.0,
  P_skin_rat = 1.0,
  P_slowly_perfused_human = 1.0,
  P_slowly_perfused_rat = 1.0,
  P_liver = 1.0,
  P_rest = 1.0
))

pbpk_ode_rat <- function(t, state, parms) {
  with(as.list(c(state, parms)), {
    Q_brain_human_abs <- Q_brain_human * Qc
    V_brain_human_abs <- V_brain_human * BW
    Cv_brain_human <- C_brain_human / P_brain_human
    Q_brain_rat_abs <- Q_brain_rat * Qc
    V_brain_rat_abs <- V_brain_rat * BW
    Cv_brain_rat <- C_brain_rat / P_brain_rat
    Q_diaphragm_human_abs <- Q_diaphragm_human * Qc
    V_diaphragm_human_abs <- V_diaphragm_human * BW
    Cv_diaphragm_human <- C_diaphragm_human / P_diaphragm_human
    Q_diaphragm_rat_abs <- Q_diaphragm_rat * Qc
    V_diaphragm_rat_abs <- V_diaphragm_rat * BW
    Cv_diaphragm_rat <- C_diaphragm_rat / P_diaphragm_rat
    Q_fat_human_abs <- Q_fat_human * Qc
    V_fat_human_abs <- V_fat_human * BW
    Cv_fat_human <- C_fat_human / P_fat_human
    Q_fat_rat_abs <- Q_fat_rat * Qc
    V_fat_rat_abs <- V_fat_rat * BW
    Cv_fat_rat <- C_fat_rat / P_fat_rat
    Q_liver_human_abs <- Q_liver_human * Qc
    V_liver_human_abs <- V_liver_human * BW
    Cv_liver_human <- C_liver_human / P_liver_human
    Q_liver_rat_abs <- Q_liver_rat * Qc
    V_liver_rat_abs <- V_liver_rat * BW
    Cv_liver_rat <- C_liver_rat / P_liver_rat
    Q_rapidly_perfused_human_abs <- Q_rapidly_perfused_human * Qc
    V_rapidly_perfused_human_abs <- V_rapidly_perfused_human * BW
    Cv_rapidly_perfused_human <- C_rapidly_perfused_human / P_rapidly_perfused_human
    Q_rapidly_perfused_rat_abs <- Q_rapidly_perfused_rat * Qc
    V_rapidly_perfused_rat_abs <- V_rapidly_perfused_rat * BW
    Cv_rapidly_perfused_rat <- C_rapidly_perfused_rat / P_rapidly_perfused_rat
    Q_skin_human_abs <- Q_skin_human * Qc
    V_skin_human_abs <- V_skin_human * BW
    Cv_skin_human <- C_skin_human / P_skin_human
    Q_skin_rat_abs <- Q_skin_rat * Qc
    V_skin_rat_abs <- V_skin_rat * BW
    Cv_skin_rat <- C_skin_rat / P_skin_rat
    Q_slowly_perfused_human_abs <- Q_slowly_perfused_human * Qc
    V_slowly_perfused_human_abs <- V_slowly_perfused_human * BW
    Cv_slowly_perfused_human <- C_slowly_perfused_human / P_slowly_perfused_human
    Q_slowly_perfused_rat_abs <- Q_slowly_perfused_rat * Qc
    V_slowly_perfused_rat_abs <- V_slowly_perfused_rat * BW
    Cv_slowly_perfused_rat <- C_slowly_perfused_rat / P_slowly_perfused_rat
    Q_liver_abs <- Q_liver * Qc
    V_liver_abs <- V_liver * BW
    Cv_liver <- C_liver / P_liver
    Q_rest_abs <- Q_rest * Qc
    V_rest_abs <- V_rest * BW
    Cv_rest <- C_rest / P_rest
    Cv_mix <- (Q_brain_human_abs * Cv_brain_human + Q_brain_rat_abs * Cv_brain_rat + Q_diaphragm_human_abs * Cv_diaphragm_human + Q_diaphragm_rat_abs * Cv_diaphragm_rat + Q_fat_human_abs * Cv_fat_human + Q_fat_rat_abs * Cv_fat_rat + Q_liver_human_abs * Cv_liver_human + Q_liver_rat_abs * Cv_liver_rat + Q_rapidly_perfused_human_abs * Cv_rapidly_perfused_human + Q_rapidly_perfused_rat_abs * Cv_rapidly_perfused_rat + Q_skin_human_abs * Cv_skin_human + Q_skin_rat_abs * Cv_skin_rat + Q_slowly_perfused_human_abs * Cv_slowly_perfused_human + Q_slowly_perfused_rat_abs * Cv_slowly_perfused_rat + Q_liver_abs * Cv_liver + Q_rest_abs * Cv_rest) / Qc
    C_art <- Cv_mix

    # --- Metabolism in Liver ---
    Vmet <- (Vmax * C_liver * fu) / (Km + C_liver * fu)

    # --- GI Tract Absorption (oral) ---
    dAmount_stomach <- -GE * Amount_stomach
    dAmount_gut <- GE * Amount_stomach - Kabs * Amount_gut - K_feces * Amount_gut

    # --- Organ Concentration ODEs ---
    dC_brain_human <- (Q_brain_human_abs * (C_art - Cv_brain_human)) / V_brain_human_abs
    dC_brain_rat <- (Q_brain_rat_abs * (C_art - Cv_brain_rat)) / V_brain_rat_abs
    dC_diaphragm_human <- (Q_diaphragm_human_abs * (C_art - Cv_diaphragm_human)) / V_diaphragm_human_abs
    dC_diaphragm_rat <- (Q_diaphragm_rat_abs * (C_art - Cv_diaphragm_rat)) / V_diaphragm_rat_abs
    dC_fat_human <- (Q_fat_human_abs * (C_art - Cv_fat_human)) / V_fat_human_abs
    dC_fat_rat <- (Q_fat_rat_abs * (C_art - Cv_fat_rat)) / V_fat_rat_abs
    dC_liver_human <- (Q_liver_human_abs * (C_art - Cv_liver_human)) / V_liver_human_abs
    dC_liver_rat <- (Q_liver_rat_abs * (C_art - Cv_liver_rat)) / V_liver_rat_abs
    dC_rapidly_perfused_human <- (Q_rapidly_perfused_human_abs * (C_art - Cv_rapidly_perfused_human)) / V_rapidly_perfused_human_abs
    dC_rapidly_perfused_rat <- (Q_rapidly_perfused_rat_abs * (C_art - Cv_rapidly_perfused_rat)) / V_rapidly_perfused_rat_abs
    dC_skin_human <- (Q_skin_human_abs * (C_art - Cv_skin_human)) / V_skin_human_abs
    dC_skin_rat <- (Q_skin_rat_abs * (C_art - Cv_skin_rat)) / V_skin_rat_abs
    dC_slowly_perfused_human <- (Q_slowly_perfused_human_abs * (C_art - Cv_slowly_perfused_human)) / V_slowly_perfused_human_abs
    dC_slowly_perfused_rat <- (Q_slowly_perfused_rat_abs * (C_art - Cv_slowly_perfused_rat)) / V_slowly_perfused_rat_abs
    dC_liver <- (Q_liver_abs * (C_art - Cv_liver) + Kabs * Amount_gut + - Vmet) / V_liver_abs
    dC_rest <- (Q_rest_abs * (C_art - Cv_rest)) / V_rest_abs

    return(list(c(dAmount_stomach, dAmount_gut, dC_brain_human, dC_brain_rat, dC_diaphragm_human, dC_diaphragm_rat, dC_fat_human, dC_fat_rat, dC_liver_human, dC_liver_rat, dC_rapidly_perfused_human, dC_rapidly_perfused_rat, dC_skin_human, dC_skin_rat, dC_slowly_perfused_human, dC_slowly_perfused_rat, dC_liver, dC_rest)))
  })
}

# --- Rat Simulation ---
init_rat <- c(
  Amount_stomach = unname(10.0 * params_rat['BW']), Amount_gut = 0, C_brain_human = 0, C_brain_rat = 0, C_diaphragm_human = 0, C_diaphragm_rat = 0, C_fat_human = 0, C_fat_rat = 0, C_liver_human = 0, C_liver_rat = 0, C_rapidly_perfused_human = 0, C_rapidly_perfused_rat = 0, C_skin_human = 0, C_skin_rat = 0, C_slowly_perfused_human = 0, C_slowly_perfused_rat = 0, C_liver = 0, C_rest = 0
)
times <- seq(0, 24, by = 0.1)
out_rat <- as.data.frame(ode(y = init_rat, times = times, func = pbpk_ode_rat, parms = params_rat))
write.csv(out_rat, file = 'rat_simulation_results.csv', row.names = FALSE)
print('Rat PBPK Simulation complete! Saved to rat_simulation_results.csv')

write.csv(out_rat, file = 'dynamic_simulation_results.csv', row.names = FALSE)