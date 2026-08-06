# ==========================================
# AUTO-GENERATED PBPK MODEL (Rat & Human)
# ==========================================
if (!require('deSolve')) {
  install.packages('deSolve', repos='http://cran.us.r-project.org')
  library(deSolve)
}

# --- GLOBAL / BIOCHEMICAL PARAMETERS ---
global_params <- list(
  fu = 0.04,          # Unbound fraction in plasma
  Km = 140.0,         # Michaelis-Menten constant (uM)
  Vmax = 250000.0,     # Max. metabolic velocity (ug/h)
  GE = 2.61,         # Gastric emptying (1/h)
  Kabs = 2.19,       # Absorption rate (1/h)
  K_feces = 0.011,   # Fecal elimination (1/h)
  K_met_elim = 0.5       # Metabolite (RLZ-OH) &0elimination rate (1/h)
)

# ==========================================
# RAT PBPK MODEL
# ==========================================
params_rat <- unlist(list(
  BW = 0.25,  # Body weight (kg)
  Qc = 14.0,   # Cardiac output (L/h)
  fu = global_params$fu,
  Km = global_params$Km,
  Vmax = global_params$Vmax,
  GE = global_params$GE,
  Kabs = global_params$Kabs,
  K_feces = global_params$K_feces,
  K_met_elim = global_params$K_met_elim,
  Q_liver = 0.174,
  Q_kidney = 0.021,
  Q_brain = 0.141,
  Q_lungs = 0.051,
  Q_heart = 0.02,
  Q_fat = 0.07,
  Q_rest = max(0, 1.0 - 0.426),
  V_liver = 0.036,
  V_kidney = 0.006,
  V_brain = 0.0073,
  V_lungs = 0.004,
  V_heart = 0.006,
  V_fat = 0.07,
  V_plasma = 0.074,
  V_rest = max(0.05, 1.0 - (0.1293 + 0.04)),
  P_liver = 2.2,
  P_kidney = 4.622509,
  P_brain = 2.44,
  P_lungs = 1.0,
  P_heart = 4.251126,
  P_fat = 14.12276,
  P_rest = 1.0
))

pbpk_ode_rat <- function(t, state, parms) {
  with(as.list(c(state, parms)), {
    Q_liver_abs <- Q_liver * Qc
    V_liver_abs <- V_liver * BW
    Cv_liver <- C_liver / P_liver
    Q_kidney_abs <- Q_kidney * Qc
    V_kidney_abs <- V_kidney * BW
    Cv_kidney <- C_kidney / P_kidney
    Q_brain_abs <- Q_brain * Qc
    V_brain_abs <- V_brain * BW
    Cv_brain <- C_brain / P_brain
    Q_lungs_abs <- Q_lungs * Qc
    V_lungs_abs <- V_lungs * BW
    Cv_lungs <- C_lungs / P_lungs
    Q_heart_abs <- Q_heart * Qc
    V_heart_abs <- V_heart * BW
    Cv_heart <- C_heart / P_heart
    Q_fat_abs <- Q_fat * Qc
    V_fat_abs <- V_fat * BW
    Cv_fat <- C_fat / P_fat
    Q_rest_abs <- Q_rest * Qc
    V_rest_abs <- V_rest * BW
    Cv_rest <- C_rest / P_rest
    Cv_mix <- (Q_liver_abs * Cv_liver + Q_kidney_abs * Cv_kidney + Q_brain_abs * Cv_brain + Q_heart_abs * Cv_heart + Q_fat_abs * Cv_fat + Q_rest_abs * Cv_rest) / Qc
    C_art <- C_lungs / P_lungs
    # Michaelis-Menten Metabolism in Liver (RLZ -> RLZ-OH)
    Vmet <- (Vmax * C_liver * fu) / (Km + C_liver * fu)
    dAmount_metabolite <- Vmet - K_met_elim * Amount_metabolite

    # GI Tract Absorption
    dAmount_stomach <- -GE * Amount_stomach
    dAmount_gut <- GE * Amount_stomach - Kabs * Amount_gut - K_feces * Amount_gut

    dC_liver <- (Q_liver_abs * (C_art - Cv_liver) + Kabs * Amount_gut - Vmet) / V_liver_abs
    dC_kidney <- (Q_kidney_abs * (C_art - Cv_kidney)) / V_kidney_abs
    dC_brain <- (Q_brain_abs * (C_art - Cv_brain)) / V_brain_abs
    dC_lungs <- (Qc * (Cv_mix - Cv_lungs)) / V_lungs_abs
    dC_heart <- (Q_heart_abs * (C_art - Cv_heart)) / V_heart_abs
    dC_fat <- (Q_fat_abs * (C_art - Cv_fat)) / V_fat_abs
    dC_rest <- (Q_rest_abs * (C_art - Cv_rest)) / V_rest_abs

    return(list(c(dAmount_stomach, dAmount_gut, dAmount_metabolite, dC_liver, dC_kidney, dC_brain, dC_lungs, dC_heart, dC_fat, dC_rest)))
  })
}

# --- ALLOMETRIC SCALING FOR HUMAN ---
# Scaling Cardiac Output and Clearance:0Q_human = Q_rat * (BW_human / BW_rat)^0.75
BW_rat <- 0.250
BW_human <- 70.0
Qc_human_scaled <- 14.0 * ((BW_human / BW_rat) ** 0.75)

# ==========================================
# HUMAN PBPK MODEL
# ==========================================
params_human <- unlist(list(
  BW = 70.0,  # Body weight (kg)
  Qc = Qc_human_scaled,   # Cardiac output (L/h)
  fu = global_params$fu,
  Km = global_params$Km,
  Vmax = global_params$Vmax,
  GE = global_params$GE,
  Kabs = global_params$Kabs,
  K_feces = global_params$K_feces,
  K_met_elim = global_params$K_met_elim,
  Q_liver = 0.257,
  Q_kidney = 0.034,
  Q_brain = 0.177,
  Q_lungs = 0.09,
  Q_heart = 0.117,
  Q_fat = 0.052,
  Q_rest = max(0, 1.0 - 0.637),
  V_liver = 0.026,
  V_kidney = 0.014,
  V_brain = 0.004,
  V_lungs = 0.012,
  V_heart = 0.021,
  V_fat = 0.187,
  V_plasma = 0.03976,
  V_rest = max(0.05, 1.0 - (0.264 + 0.04)),
  P_liver = 2.2,
  P_kidney = 4.622509,
  P_brain = 2.44,
  P_lungs = 1.0,
  P_heart = 4.251126,
  P_fat = 14.12276,
  P_rest = 1.0
))

pbpk_ode_human <- function(t, state, parms) {
  with(as.list(c(state, parms)), {
    Q_liver_abs <- Q_liver * Qc
    V_liver_abs <- V_liver * BW
    Cv_liver <- C_liver / P_liver
    Q_kidney_abs <- Q_kidney * Qc
    V_kidney_abs <- V_kidney * BW
    Cv_kidney <- C_kidney / P_kidney
    Q_brain_abs <- Q_brain * Qc
    V_brain_abs <- V_brain * BW
    Cv_brain <- C_brain / P_brain
    Q_lungs_abs <- Q_lungs * Qc
    V_lungs_abs <- V_lungs * BW
    Cv_lungs <- C_lungs / P_lungs
    Q_heart_abs <- Q_heart * Qc
    V_heart_abs <- V_heart * BW
    Cv_heart <- C_heart / P_heart
    Q_fat_abs <- Q_fat * Qc
    V_fat_abs <- V_fat * BW
    Cv_fat <- C_fat / P_fat
    Q_rest_abs <- Q_rest * Qc
    V_rest_abs <- V_rest * BW
    Cv_rest <- C_rest / P_rest
    Cv_mix <- (Q_liver_abs * Cv_liver + Q_kidney_abs * Cv_kidney + Q_brain_abs * Cv_brain + Q_heart_abs * Cv_heart + Q_fat_abs * Cv_fat + Q_rest_abs * Cv_rest) / Qc
    C_art <- C_lungs / P_lungs
    # Michaelis-Menten Metabolism in Liver (RLZ -> RLZ-OH)
    Vmet <- (Vmax * C_liver * fu) / (Km + C_liver * fu)
    dAmount_metabolite <- Vmet - K_met_elim * Amount_metabolite

    # GI Tract Absorption
    dAmount_stomach <- -GE * Amount_stomach
    dAmount_gut <- GE * Amount_stomach - Kabs * Amount_gut - K_feces * Amount_gut

    dC_liver <- (Q_liver_abs * (C_art - Cv_liver) + Kabs * Amount_gut - Vmet) / V_liver_abs
    dC_kidney <- (Q_kidney_abs * (C_art - Cv_kidney)) / V_kidney_abs
    dC_brain <- (Q_brain_abs * (C_art - Cv_brain)) / V_brain_abs
    dC_lungs <- (Qc * (Cv_mix - Cv_lungs)) / V_lungs_abs
    dC_heart <- (Q_heart_abs * (C_art - Cv_heart)) / V_heart_abs
    dC_fat <- (Q_fat_abs * (C_art - Cv_fat)) / V_fat_abs
    dC_rest <- (Q_rest_abs * (C_art - Cv_rest)) / V_rest_abs

    return(list(c(dAmount_stomach, dAmount_gut, dAmount_metabolite, dC_liver, dC_kidney, dC_brain, dC_lungs, dC_heart, dC_fat, dC_rest)))
  })
}

# ==========================================
# SIMULATION EXECUTION
# ==========================================
Dose_mg_kg <- 10.0
# 1. Rat Simulation
init_rat <- c(
  Amount_stomach = unname(Dose_mg_kg * params_rat['BW']),
  Amount_gut = 0, Amount_metabolite = 0,
  C_liver = 0, C_kidney = 0, C_brain = 0, C_lungs = 0, C_heart = 0, C_fat = 0, C_rest = 0
)
times <- seq(0, 24, by = 0.1)
out_rat <- as.data.frame(ode(y = init_rat, times = times, func = pbpk_ode_rat, parms = params_rat))
write.csv(out_rat, file = 'rat_simulation_results.csv', row.names = FALSE)
print('Rat PBPK Simulation complete! Saved to rat_simulation_results.csv')

# 2. Human Simulation
init_human <- c(
  Amount_stomach = 50.0, # 50 mg dose
  Amount_gut = 0, Amount_metabolite = 0,
  C_liver = 0, C_kidney = 0, C_brain = 0, C_lungs = 0, C_heart = 0, C_fat = 0, C_rest = 0
)
out_human <- as.data.frame(ode(y = init_human, times = times, func = pbpk_ode_human, parms = params_human))
write.csv(out_human, file = 'human_simulation_results.csv', row.names = FALSE)
write.csv(out_human, file = 'dynamic_simulation_results.csv', row.names = FALSE)
print('Human PBPK Simulation complete! Saved to human_simulation_results.csv')
