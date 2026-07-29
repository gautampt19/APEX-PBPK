library(deSolve)

# Parameter definitions for flame retardant PBK model
params <- c(
  BW = 0.25,        # Body weight (kg)
  Dose = 10,        # Oral dose (mg/kg)
  Qc = 15.0,        # Cardiac output (L/h)
  
  # blood flow fractions of Qc
  QL = 0.174,       # Liver
  QK = 0.141,       # Kidney
  QB = 0.02,        # Brain
  QF = 0.07,        # Fat
  QS = 0.15,        # Slowly perfused
  QR = 0.449,       # Rapidly perfused
  
  # organ volume fractions of BW
  VL = 0.036,       # Liver
  VK = 0.0073,      # Kidney
  VB = 0.006,       # Brain
  VF = 0.07,        # Fat
  VS = 0.40,        # Slowly perfused
  VR = 0.25,        # Rapidly perfused
  VP = 0.074,       # Blood/Plasma
  
  # partition coefficients organ:plasma
  PL = 2.0,         # Liver
  PK = 3.0,         # Kidney
  PB = 1.5,         # Brain
  PF = 10.0,        # Fat
  PS = 1.0,         # Slowly
  PR = 1.5,         # Rapidly
  
  # biochemical parameters
  Kabs = 0.5,       # gut absorption rate constant (1/h)
  Vmax = 100000,    # liver metabolism Vmax
  Km = 50,          # MM constant
  Clurine = 0.1,    # renal clearance
  Kfeces = 0.01,    # fecal clearance
  Kehr = 0.05       # Enterohepatic recirculation rate
)

# Amount in compartments (mg)
Dose_mg <- as.numeric(params["Dose"] * params["BW"])
init_states <- c(
  A_gut = Dose_mg,
  A_liver = 0,
  A_kidney = 0,
  A_brain = 0,
  A_fat = 0,
  A_slow = 0,
  A_rapid = 0,
  A_blood = 0,
  A_urine = 0,
  A_feces = 0,
  A_bile = 0
)

pbk_ode <- function(time, state, parameters) {
  with(as.list(c(state, parameters)), {
    # 1. Volumes of compartments
    Vol_L <- VL * BW
    Vol_K <- VK * BW
    Vol_B <- VB * BW
    Vol_F <- VF * BW
    Vol_S <- VS * BW
    Vol_R <- VR * BW
    Vol_Blood <- VP * BW
    
    # 2. Flows
    Flow_c <- Qc
    Flow_L <- QL * Flow_c
    Flow_K <- QK * Flow_c
    Flow_B <- QB * Flow_c
    Flow_F <- QF * Flow_c
    Flow_S <- QS * Flow_c
    Flow_R <- QR * Flow_c
    
    # 3. Concentrations
    C_gut <- A_gut / Vol_Blood
    C_liver <- A_liver / Vol_L
    C_kidney <- A_kidney / Vol_K
    C_brain <- A_brain / Vol_B
    C_fat <- A_fat / Vol_F
    C_slow <- A_slow / Vol_S
    C_rapid <- A_rapid / Vol_R
    C_blood <- A_blood / Vol_Blood
    
    # 4. Metabolism & Excretion
    Vmet <- (Vmax * C_liver) / (Km + C_liver)
    
    # 5. Differential Equations (dA/dt)
    dA_gut_dt <- -Kabs * A_gut + Kehr * A_bile
    
    # Liver receives hepatic artery + gut absorption + EHR, minus metabolism
    dA_liver_dt <- Flow_L * (C_blood - C_liver / PL) + Kabs * A_gut - Vmet - Kfeces * A_liver
    
    # Kidney clears via urine
    dA_kidney_dt <- Flow_K * (C_blood - C_kidney / PK) - Clurine * (C_kidney / PK)
    
    # Organs
    dA_brain_dt <- Flow_B * (C_blood - C_brain / PB)
    dA_fat_dt <- Flow_F * (C_blood - C_fat / PF)
    dA_slow_dt <- Flow_S * (C_blood - C_slow / PS)
    dA_rapid_dt <- Flow_R * (C_blood - C_rapid / PR)
    
    # Blood pool receives outflows from all organs and flows out to all organs
    dA_blood_dt <- (Flow_L * (C_liver / PL) + Flow_K * (C_kidney / PK) + 
                    Flow_B * (C_brain / PB) + Flow_F * (C_fat / PF) + 
                    Flow_S * (C_slow / PS) + Flow_R * (C_rapid / PR)) - Flow_c * C_blood
                    
    dA_urine_dt <- Clurine * (C_kidney / PK)
    dA_feces_dt <- Kfeces * A_liver * 0.1 # fraction excreted in feces
    dA_bile_dt <- Kfeces * A_liver * 0.9 - Kehr * A_bile # EHR
    
    return(list(c(
      dA_gut_dt,
      dA_liver_dt,
      dA_kidney_dt,
      dA_brain_dt,
      dA_fat_dt,
      dA_slow_dt,
      dA_rapid_dt,
      dA_blood_dt,
      dA_urine_dt,
      dA_feces_dt,
      dA_bile_dt
    )))
  })
}

# Run simulation
times <- seq(0, 24, by = 0.1)
sol <- ode(y = init_states, times = times, func = pbk_ode, parms = params)
write.csv(sol, "pbpk_output.csv", row.names = FALSE)
