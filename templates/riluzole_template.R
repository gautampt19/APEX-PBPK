library(deSolve)

# Parameter definitions (values extracted or user-specified)
params <- c(
  BW = 0.25,        # Body weight (kg)
  Dose = 10,        # Dose (mg/kg)
  Qc = 15.0,        # Cardiac output (L/h)
  
  # blood flow fractions of Qc
  QL = 0.174,       # Liver
  QK = 0.141,       # Kidney
  QH = 0.051,       # Heart
  QB = 0.02,        # Brain
  QF = 0.07,        # Fat
  
  # organ volume fractions of BW
  VL = 0.036,       # Liver
  VLu = 0.006,      # Lung
  VK = 0.0073,      # Kidney
  VH = 0.004,       # Heart
  VB = 0.006,       # Brain
  VF = 0.07,        # Fat
  VP = 0.074,       # Plasma
  
  # partition coefficients organ:plasma
  PL = 2.2,         # Liver
  PLu = 5.96,       # Lung
  PK = 4.62,        # Kidney
  PH = 4.25,        # Heart
  PB = 2.44,        # Brain
  PF = 14.12,       # Fat
  PR = 1.0,         # Rest of body
  
  # biochemical parameters
  Kabs = 0.69,      # gut absorption rate constant (1/h)
  Fu = 0.04,        # fraction unbound in plasma
  Vmax = 250000,    # liver metabolism Vmax (nmol/h/kg^0.75)
  Km = 140,         # MM constant (umol/L)
  Clurine = 0.3771, # renal clearance (uL/h)
  Kfeces = 0.013    # fecal elimination rate constant (1/h)
)

# Amount in compartments (mg)
# Gut has the oral dose: Dose (mg/kg) * BW (kg)
Dose_mg <- as.numeric(params["Dose"] * params["BW"])
init_states <- c(
  A_gut = Dose_mg,
  A_liver = 0,
  A_lung = 0,
  A_kidney = 0,
  A_heart = 0,
  A_brain = 0,
  A_fat = 0,
  A_rest = 0,
  A_venous = 0,
  A_arterial = 0,
  A_urine = 0,
  A_feces = 0
)

pbpk_ode <- function(time, state, parameters) {
  with(as.list(c(state, parameters)), {
    # 1. Volumes of compartments (L or kg)
    Vol_L <- VL * BW
    Vol_Lu <- VLu * BW
    Vol_K <- VK * BW
    Vol_H <- VH * BW
    Vol_B <- VB * BW
    Vol_F <- VF * BW
    Vol_P <- VP * BW
    
    # Rest of body volume
    Vol_R <- BW - (Vol_L + Vol_Lu + Vol_K + Vol_H + Vol_B + Vol_F + Vol_P)
    if (Vol_R <= 0) Vol_R <- 0.01 * BW
    
    # 2. Flows (L/h)
    Flow_c <- Qc
    Flow_L <- QL * Flow_c
    Flow_K <- QK * Flow_c
    Flow_H <- QH * Flow_c
    Flow_B <- QB * Flow_c
    Flow_F <- QF * Flow_c
    
    # Rest of body flow
    Flow_R <- Flow_c - (Flow_L + Flow_K + Flow_H + Flow_B + Flow_F)
    if (Flow_R <= 0) Flow_R <- 0.01 * Flow_c
    
    # 3. Concentrations (mg/L)
    C_gut <- A_gut / Vol_P
    C_liver <- A_liver / Vol_L
    C_lung <- A_lung / Vol_Lu
    C_kidney <- A_kidney / Vol_K
    C_heart <- A_heart / Vol_H
    C_brain <- A_brain / Vol_B
    C_fat <- A_fat / Vol_F
    C_rest <- A_rest / Vol_R
    C_art <- A_arterial / (Vol_P * 0.3)
    C_ven <- A_venous / (Vol_P * 0.7)
    
    # 4. Metabolic Clearance (mg/h)
    C_liver_uM <- (C_liver / 234.2) * 1000
    Vmet_uM_h <- (Vmax * C_liver_uM * Fu) / (Km + C_liver_uM * Fu)
    Vmet <- Vmet_uM_h * (BW^0.75) * 1e-6 * 234.2
    
    # 5. Differential Equations (dA/dt)
    dA_gut_dt <- -Kabs * A_gut - Kfeces * A_gut
    dA_liver_dt <- Flow_L * (C_art - C_liver / PL) + Kabs * A_gut - Vmet
    dA_lung_dt <- Flow_c * (C_ven - C_lung / PLu)
    dA_kidney_dt <- Flow_K * (C_art - C_kidney / PK) - Clurine * (C_kidney / PK) * Fu
    dA_brain_dt <- Flow_B * (C_art - C_brain / PB)
    dA_heart_dt <- Flow_H * (C_art - C_heart / PH)
    dA_fat_dt <- Flow_F * (C_art - C_fat / PF)
    dA_rest_dt <- Flow_R * (C_art - C_rest / PR)
    
    # Blood pools
    dA_venous_dt <- (Flow_L * (C_liver / PL) + Flow_K * (C_kidney / PK) + 
                     Flow_B * (C_brain / PB) + Flow_H * (C_heart / PH) + 
                     Flow_F * (C_fat / PF) + Flow_R * (C_rest / PR)) - Flow_c * C_ven
                     
    dA_arterial_dt <- Flow_c * (C_lung / PLu - C_art)
    
    dA_urine_dt <- Clurine * (C_kidney / PK) * Fu
    dA_feces_dt <- Kfeces * A_gut
    
    return(list(c(
      dA_gut_dt,
      dA_liver_dt,
      dA_lung_dt,
      dA_kidney_dt,
      dA_heart_dt,
      dA_brain_dt,
      dA_fat_dt,
      dA_rest_dt,
      dA_venous_dt,
      dA_arterial_dt,
      dA_urine_dt,
      dA_feces_dt
    )))
  })
}

# Run simulation
times <- seq(0, 24, by = 0.1)
sol <- ode(y = init_states, times = times, func = pbpk_ode, parms = params)
write.csv(sol, "pbpk_output.csv", row.names = FALSE)
