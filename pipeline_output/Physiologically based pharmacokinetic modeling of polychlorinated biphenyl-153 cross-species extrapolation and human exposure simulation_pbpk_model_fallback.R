# ==========================================
# AUTO-GENERATED PBPK MODEL
# Route: oral | Metabolism: linear
# Species: human, mouse, rat
# ==========================================
if (!require('deSolve')) {
  install.packages('deSolve', repos='http://cran.us.r-project.org')
  library(deSolve)
}

# --- GLOBAL / BIOCHEMICAL PARAMETERS ---
global_params <- list(
  fu = 0.05,
  CLint = 1.0,
  GE = 2.5,
  Kabs = 0.08,
  K_feces = 0.01
)

# ==========================================
# HUMAN PBPK MODEL
# ==========================================
params_human <- unlist(list(
  BW = 70.0,
  Qc = 372.0,
  fu = global_params$fu,
  CLint = global_params$CLint,
  GE = global_params$GE,
  Kabs = global_params$Kabs,
  K_feces = global_params$K_feces,
  Q_kidney = 0.175,
  Q_gut = 0.15,
  Q_brain = 0.114,
  Q_liver = 0.227,
  Q_fat = 0.052,
  Q_lung = 1.0,
  Q_skin = 0.05,
  Q_rest = max(0, 1.0 - 0.768),
  V_kidney = 0.004,
  V_gut = 0.017,
  V_brain = 0.02,
  V_liver = 0.026,
  V_fat = 0.214,
  V_lung = 0.008,
  V_skin = 0.037,
  V_plasma = 0.044,
  V_rest = max(0.05, 1.0 - (0.326 + 0.04)),
  P_kidney = 1.0,
  P_gut = 1.0,
  P_brain = 1.0,
  P_liver = 1.45e-05,
  P_fat = 1.0,
  P_lung = 1.0,
  P_skin = 1.0,
  P_rest = 1.0
))

pbpk_ode_human <- function(t, state, parms) {
  with(as.list(c(state, parms)), {
    Q_kidney_abs <- Q_kidney * Qc
    V_kidney_abs <- V_kidney * BW
    Cv_kidney <- C_kidney / P_kidney
    Q_gut_abs <- Q_gut * Qc
    V_gut_abs <- V_gut * BW
    Cv_gut <- C_gut / P_gut
    Q_brain_abs <- Q_brain * Qc
    V_brain_abs <- V_brain * BW
    Cv_brain <- C_brain / P_brain
    Q_liver_abs <- Q_liver * Qc
    V_liver_abs <- V_liver * BW
    Cv_liver <- C_liver / P_liver
    Q_fat_abs <- Q_fat * Qc
    V_fat_abs <- V_fat * BW
    Cv_fat <- C_fat / P_fat
    Q_lung_abs <- Q_lung * Qc
    V_lung_abs <- V_lung * BW
    Cv_lung <- C_lung / P_lung
    Q_skin_abs <- Q_skin * Qc
    V_skin_abs <- V_skin * BW
    Cv_skin <- C_skin / P_skin
    Q_rest_abs <- Q_rest * Qc
    V_rest_abs <- V_rest * BW
    Cv_rest <- C_rest / P_rest
    Cv_mix <- (Q_kidney_abs * Cv_kidney + Q_gut_abs * Cv_gut + Q_brain_abs * Cv_brain + Q_liver_abs * Cv_liver + Q_fat_abs * Cv_fat + Q_skin_abs * Cv_skin + Q_rest_abs * Cv_rest) / Qc
    C_art <- C_lung / P_lung

    # --- Metabolism in Liver ---
    Vmet <- CLint * C_liver * fu / P_liver

    # --- GI Tract Absorption (oral) ---
    dAmount_stomach <- -GE * Amount_stomach
    dAmount_gut <- GE * Amount_stomach - Kabs * Amount_gut - K_feces * Amount_gut

    # --- Organ Concentration ODEs ---
    dC_kidney <- (Q_kidney_abs * (C_art - Cv_kidney)) / V_kidney_abs
    dC_gut <- (Q_gut_abs * (C_art - Cv_gut)) / V_gut_abs
    dC_brain <- (Q_brain_abs * (C_art - Cv_brain)) / V_brain_abs
    dC_liver <- (Q_liver_abs * (C_art - Cv_liver) + Kabs * Amount_gut + - Vmet) / V_liver_abs
    dC_fat <- (Q_fat_abs * (C_art - Cv_fat)) / V_fat_abs
    dC_lung <- (Qc * (Cv_mix - Cv_lung)) / V_lung_abs
    dC_skin <- (Q_skin_abs * (C_art - Cv_skin)) / V_skin_abs
    dC_rest <- (Q_rest_abs * (C_art - Cv_rest)) / V_rest_abs

    return(list(c(dAmount_stomach, dAmount_gut, dC_kidney, dC_gut, dC_brain, dC_liver, dC_fat, dC_lung, dC_skin, dC_rest)))
  })
}

# --- Human Simulation ---
init_human <- c(
  Amount_stomach = 50.0, Amount_gut = 0, C_kidney = 0, C_gut = 0, C_brain = 0, C_liver = 0, C_fat = 0, C_lung = 0, C_skin = 0, C_rest = 0
)
times <- seq(0, 24, by = 0.1)
out_human <- as.data.frame(ode(y = init_human, times = times, func = pbpk_ode_human, parms = params_human))
write.csv(out_human, file = 'human_simulation_results.csv', row.names = FALSE)
print('Human PBPK Simulation complete! Saved to human_simulation_results.csv')

# ==========================================
# MOUSE PBPK MODEL
# ==========================================
params_mouse <- unlist(list(
  BW = 0.025,
  Qc = 1.68,
  fu = global_params$fu,
  CLint = global_params$CLint,
  GE = global_params$GE,
  Kabs = global_params$Kabs,
  K_feces = global_params$K_feces,
  Q_kidney = 0.175,
  Q_gut = 0.15,
  Q_brain = 0.114,
  Q_liver = 0.227,
  Q_fat = 0.052,
  Q_lung = 1.0,
  Q_skin = 0.05,
  Q_rest = max(0, 1.0 - 0.768),
  V_kidney = 0.004,
  V_gut = 0.017,
  V_brain = 0.02,
  V_liver = 0.026,
  V_fat = 0.214,
  V_lung = 0.008,
  V_skin = 0.037,
  V_plasma = 0.044,
  V_rest = max(0.05, 1.0 - (0.326 + 0.04)),
  P_kidney = 1.0,
  P_gut = 1.0,
  P_brain = 1.0,
  P_liver = 1.45e-05,
  P_fat = 1.0,
  P_lung = 1.0,
  P_skin = 1.0,
  P_rest = 1.0
))

pbpk_ode_mouse <- function(t, state, parms) {
  with(as.list(c(state, parms)), {
    Q_kidney_abs <- Q_kidney * Qc
    V_kidney_abs <- V_kidney * BW
    Cv_kidney <- C_kidney / P_kidney
    Q_gut_abs <- Q_gut * Qc
    V_gut_abs <- V_gut * BW
    Cv_gut <- C_gut / P_gut
    Q_brain_abs <- Q_brain * Qc
    V_brain_abs <- V_brain * BW
    Cv_brain <- C_brain / P_brain
    Q_liver_abs <- Q_liver * Qc
    V_liver_abs <- V_liver * BW
    Cv_liver <- C_liver / P_liver
    Q_fat_abs <- Q_fat * Qc
    V_fat_abs <- V_fat * BW
    Cv_fat <- C_fat / P_fat
    Q_lung_abs <- Q_lung * Qc
    V_lung_abs <- V_lung * BW
    Cv_lung <- C_lung / P_lung
    Q_skin_abs <- Q_skin * Qc
    V_skin_abs <- V_skin * BW
    Cv_skin <- C_skin / P_skin
    Q_rest_abs <- Q_rest * Qc
    V_rest_abs <- V_rest * BW
    Cv_rest <- C_rest / P_rest
    Cv_mix <- (Q_kidney_abs * Cv_kidney + Q_gut_abs * Cv_gut + Q_brain_abs * Cv_brain + Q_liver_abs * Cv_liver + Q_fat_abs * Cv_fat + Q_skin_abs * Cv_skin + Q_rest_abs * Cv_rest) / Qc
    C_art <- C_lung / P_lung

    # --- Metabolism in Liver ---
    Vmet <- CLint * C_liver * fu / P_liver

    # --- GI Tract Absorption (oral) ---
    dAmount_stomach <- -GE * Amount_stomach
    dAmount_gut <- GE * Amount_stomach - Kabs * Amount_gut - K_feces * Amount_gut

    # --- Organ Concentration ODEs ---
    dC_kidney <- (Q_kidney_abs * (C_art - Cv_kidney)) / V_kidney_abs
    dC_gut <- (Q_gut_abs * (C_art - Cv_gut)) / V_gut_abs
    dC_brain <- (Q_brain_abs * (C_art - Cv_brain)) / V_brain_abs
    dC_liver <- (Q_liver_abs * (C_art - Cv_liver) + Kabs * Amount_gut + - Vmet) / V_liver_abs
    dC_fat <- (Q_fat_abs * (C_art - Cv_fat)) / V_fat_abs
    dC_lung <- (Qc * (Cv_mix - Cv_lung)) / V_lung_abs
    dC_skin <- (Q_skin_abs * (C_art - Cv_skin)) / V_skin_abs
    dC_rest <- (Q_rest_abs * (C_art - Cv_rest)) / V_rest_abs

    return(list(c(dAmount_stomach, dAmount_gut, dC_kidney, dC_gut, dC_brain, dC_liver, dC_fat, dC_lung, dC_skin, dC_rest)))
  })
}

# --- Mouse Simulation ---
init_mouse <- c(
  Amount_stomach = unname(10.0 * params_mouse['BW']), Amount_gut = 0, C_kidney = 0, C_gut = 0, C_brain = 0, C_liver = 0, C_fat = 0, C_lung = 0, C_skin = 0, C_rest = 0
)
times <- seq(0, 24, by = 0.1)
out_mouse <- as.data.frame(ode(y = init_mouse, times = times, func = pbpk_ode_mouse, parms = params_mouse))
write.csv(out_mouse, file = 'mouse_simulation_results.csv', row.names = FALSE)
print('Mouse PBPK Simulation complete! Saved to mouse_simulation_results.csv')

# ==========================================
# RAT PBPK MODEL
# ==========================================
params_rat <- unlist(list(
  BW = 0.25,
  Qc = 14.0,
  fu = global_params$fu,
  CLint = global_params$CLint,
  GE = global_params$GE,
  Kabs = global_params$Kabs,
  K_feces = global_params$K_feces,
  Q_kidney = 0.141,
  Q_gut = 0.141,
  Q_brain = 0.02,
  Q_liver = 0.183,
  Q_fat = 0.07,
  Q_lung = 1.0,
  Q_skin = 0.058,
  Q_rest = max(0, 1.0 - 0.613),
  V_kidney = 0.007,
  V_gut = 0.027,
  V_brain = 0.006,
  V_liver = 0.034,
  V_fat = 0.07,
  V_lung = 0.005,
  V_skin = 0.19,
  V_plasma = 0.041,
  V_rest = max(0.05, 1.0 - (0.339 + 0.04)),
  P_kidney = 1.0,
  P_gut = 1.0,
  P_brain = 1.0,
  P_liver = 1.45e-05,
  P_fat = 1.0,
  P_lung = 1.0,
  P_skin = 1.0,
  P_rest = 1.0
))

pbpk_ode_rat <- function(t, state, parms) {
  with(as.list(c(state, parms)), {
    Q_kidney_abs <- Q_kidney * Qc
    V_kidney_abs <- V_kidney * BW
    Cv_kidney <- C_kidney / P_kidney
    Q_gut_abs <- Q_gut * Qc
    V_gut_abs <- V_gut * BW
    Cv_gut <- C_gut / P_gut
    Q_brain_abs <- Q_brain * Qc
    V_brain_abs <- V_brain * BW
    Cv_brain <- C_brain / P_brain
    Q_liver_abs <- Q_liver * Qc
    V_liver_abs <- V_liver * BW
    Cv_liver <- C_liver / P_liver
    Q_fat_abs <- Q_fat * Qc
    V_fat_abs <- V_fat * BW
    Cv_fat <- C_fat / P_fat
    Q_lung_abs <- Q_lung * Qc
    V_lung_abs <- V_lung * BW
    Cv_lung <- C_lung / P_lung
    Q_skin_abs <- Q_skin * Qc
    V_skin_abs <- V_skin * BW
    Cv_skin <- C_skin / P_skin
    Q_rest_abs <- Q_rest * Qc
    V_rest_abs <- V_rest * BW
    Cv_rest <- C_rest / P_rest
    Cv_mix <- (Q_kidney_abs * Cv_kidney + Q_gut_abs * Cv_gut + Q_brain_abs * Cv_brain + Q_liver_abs * Cv_liver + Q_fat_abs * Cv_fat + Q_skin_abs * Cv_skin + Q_rest_abs * Cv_rest) / Qc
    C_art <- C_lung / P_lung

    # --- Metabolism in Liver ---
    Vmet <- CLint * C_liver * fu / P_liver

    # --- GI Tract Absorption (oral) ---
    dAmount_stomach <- -GE * Amount_stomach
    dAmount_gut <- GE * Amount_stomach - Kabs * Amount_gut - K_feces * Amount_gut

    # --- Organ Concentration ODEs ---
    dC_kidney <- (Q_kidney_abs * (C_art - Cv_kidney)) / V_kidney_abs
    dC_gut <- (Q_gut_abs * (C_art - Cv_gut)) / V_gut_abs
    dC_brain <- (Q_brain_abs * (C_art - Cv_brain)) / V_brain_abs
    dC_liver <- (Q_liver_abs * (C_art - Cv_liver) + Kabs * Amount_gut + - Vmet) / V_liver_abs
    dC_fat <- (Q_fat_abs * (C_art - Cv_fat)) / V_fat_abs
    dC_lung <- (Qc * (Cv_mix - Cv_lung)) / V_lung_abs
    dC_skin <- (Q_skin_abs * (C_art - Cv_skin)) / V_skin_abs
    dC_rest <- (Q_rest_abs * (C_art - Cv_rest)) / V_rest_abs

    return(list(c(dAmount_stomach, dAmount_gut, dC_kidney, dC_gut, dC_brain, dC_liver, dC_fat, dC_lung, dC_skin, dC_rest)))
  })
}

# --- Rat Simulation ---
init_rat <- c(
  Amount_stomach = unname(10.0 * params_rat['BW']), Amount_gut = 0, C_kidney = 0, C_gut = 0, C_brain = 0, C_liver = 0, C_fat = 0, C_lung = 0, C_skin = 0, C_rest = 0
)
times <- seq(0, 24, by = 0.1)
out_rat <- as.data.frame(ode(y = init_rat, times = times, func = pbpk_ode_rat, parms = params_rat))
write.csv(out_rat, file = 'rat_simulation_results.csv', row.names = FALSE)
print('Rat PBPK Simulation complete! Saved to rat_simulation_results.csv')

write.csv(out_rat, file = 'dynamic_simulation_results.csv', row.names = FALSE)