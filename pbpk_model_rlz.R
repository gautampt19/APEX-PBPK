# Load necessary library
if (!require("deSolve")) {
  install.packages("deSolve", repos = "http://cran.us.r-project.org")
  library(deSolve)
}

# 1. Define Physiological and Biochemical Parameters (From Riluzole ASD Paper)
# Using the Extracted Human/Rat values from Table 1
parameters <- c(
  # Blood Flow Fractions (fraction of cardiac output)
  Qc     = 15.0,     # Cardiac output (L/h) - Generic rat value (needs exact allometric scaling depending on BW)
  Q_liv  = 0.257,
  Q_lung = 0.034,
  Q_kid  = 0.177,
  Q_heart= 0.090,
  Q_brain= 0.117,
  Q_fat  = 0.052,
  Q_rest = 1 - (0.257 + 0.034 + 0.177 + 0.090 + 0.117 + 0.052), # Rest of body
  
  # Volume Fractions (fraction of body weight, approx L/kg)
  BW     = 0.250,    # Body weight (kg) for rat
  V_liv  = 0.026,
  V_lung = 0.014,
  V_kid  = 0.004,
  V_heart= 0.012,
  V_brain= 0.021,
  V_fat  = 0.187,
  V_plas = 0.03976,
  V_rest = 1 - (0.026 + 0.014 + 0.004 + 0.012 + 0.021 + 0.187 + 0.03976),
  
  # Partition Coefficients (Tissue:Plasma)
  P_liv  = 2.2,
  P_brain= 2.44,
  P_kid  = 4.622509,
  P_lung = 5.958539,
  P_fat  = 14.12276,
  P_heart= 4.251126,
  P_rest = 1.0, # Assumed for rest of body
  
  # Absorption & Metabolism Parameters
  GE     = 2.61,     # Gastric Emptying
  Kabs   = 0.69,     # Gut absorption (tablet) or 2.19 (ASD)
  fu     = 0.04,     # Fraction unbound in plasma
  Vmax   = 250000.0, # nmol/h/Kg^0.75
  Km     = 140.0,    # umol/L
  
  # Excretion
  Cl_urine = 0.3771, # ul/h/kg^0.25
  K_feces  = 0.013   # 1/h/kg^0.25 (tablet) or 0.011 (ASD)
)

# 2. Define the PBPK Model Equations (ODEs)
pbpk_model <- function(t, state, parameters) {
  with(as.list(c(state, parameters)), {
    
    # Absolute Flows (L/h)
    Q_liv_abs   <- Q_liv * Qc
    Q_lung_abs  <- Q_lung * Qc
    Q_kid_abs   <- Q_kid * Qc
    Q_heart_abs <- Q_heart * Qc
    Q_brain_abs <- Q_brain * Qc
    Q_fat_abs   <- Q_fat * Qc
    Q_rest_abs  <- Q_rest * Qc
    
    # Absolute Volumes (L)
    V_liv_abs   <- V_liv * BW
    V_lung_abs  <- V_lung * BW
    V_kid_abs   <- V_kid * BW
    V_heart_abs <- V_heart * BW
    V_brain_abs <- V_brain * BW
    V_fat_abs   <- V_fat * BW
    V_plas_abs  <- V_plas * BW
    V_rest_abs  <- V_rest * BW
    
    # Venous concentrations from tissues
    Cv_liv   <- C_liv / P_liv
    Cv_brain <- C_brain / P_brain
    Cv_kid   <- C_kid / P_kid
    Cv_heart <- C_heart / P_heart
    Cv_fat   <- C_fat / P_fat
    Cv_rest  <- C_rest / P_rest
    
    # Venous Blood Pool (Mixed Venous Concentration)
    Cv_mix <- (Q_liv_abs * Cv_liv + Q_brain_abs * Cv_brain + Q_kid_abs * Cv_kid + 
               Q_heart_abs * Cv_heart + Q_fat_abs * Cv_fat + Q_rest_abs * Cv_rest) / Qc
    
    # Metabolism in Liver (Michaelis-Menten)
    # Vmet = (Vmax * Cliver * fu) / (Km + Cliver * fu)
    Vmet <- (Vmax * C_liv * fu) / (Km + C_liv * fu)
    
    # Arterial blood concentration exiting lungs
    C_art <- C_lung / P_lung 
    
    # Differential Equations
    
    # 1. Stomach (Dosing compartment)
    dAmount_stomach <- -GE * Amount_stomach
    
    # 2. Gut (Absorption)
    dAmount_gut <- GE * Amount_stomach - Kabs * Amount_gut - K_feces * Amount_gut
    
    # 3. Liver
    # Receives input from arterial blood AND absorbed drug from Gut
    dC_liv <- (Q_liv_abs * (C_art - Cv_liv) + Kabs * Amount_gut - Vmet) / V_liv_abs
    
    # 4. Lungs (receives mixed venous blood, sends to arterial)
    dC_lung <- (Qc * (Cv_mix - C_lung / P_lung)) / V_lung_abs
    
    # 5. Brain
    dC_brain <- (Q_brain_abs * (C_art - Cv_brain)) / V_brain_abs
    
    # 6. Kidney (Excretion via Cl_urine)
    dC_kid <- (Q_kid_abs * (C_art - Cv_kid) - Cl_urine * Cv_kid) / V_kid_abs
    
    # 7. Heart
    dC_heart <- (Q_heart_abs * (C_art - Cv_heart)) / V_heart_abs
    
    # 8. Fat
    dC_fat <- (Q_fat_abs * (C_art - Cv_fat)) / V_fat_abs
    
    # 9. Rest of Body
    dC_rest <- (Q_rest_abs * (C_art - Cv_rest)) / V_rest_abs
    
    # 10. Central Plasma Pool (approximated based on arterial/venous equilibration)
    dC_plas <- (Qc * (Cv_mix - C_plas)) / V_plas_abs
    
    return(list(c(dAmount_stomach, dAmount_gut, dC_liv, dC_lung, dC_brain, dC_kid, 
                  dC_heart, dC_fat, dC_rest, dC_plas)))
  })
}

# 3. Initial State & Dosing (Oral dose: 10 mg/kg)
Dose_mg_kg <- 10.0
Initial_Dose <- unname(Dose_mg_kg * parameters["BW"]) 

initial_state <- c(
  Amount_stomach = Initial_Dose, 
  Amount_gut     = 0.0,
  C_liv          = 0.0, 
  C_lung         = 0.0, 
  C_brain        = 0.0, 
  C_kid          = 0.0, 
  C_heart        = 0.0, 
  C_fat          = 0.0, 
  C_rest         = 0.0, 
  C_plas         = 0.0
)

# 4. Run Simulation (0 to 24 hours, output every 0.1 hour)
times <- seq(0, 24, by = 0.1)
out <- ode(y = initial_state, times = times, func = pbpk_model, parms = parameters)

# 5. Output Results
# Save raw results
write.csv(as.data.frame(out), file = "pbpk_simulation_results.csv", row.names = FALSE)
print("Simulation complete! Results saved to pbpk_simulation_results.csv")

# Quick plot check (if running interactively)
# plot(out, select = c("C_plas", "C_brain", "C_liv"), xlab="Time (h)", ylab="Concentration", main="Riluzole PBPK Profile")
