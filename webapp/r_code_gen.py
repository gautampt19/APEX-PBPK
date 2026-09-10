import json
import os

def generate_standalone_r_script(staged, flat_params, dose_val, compound, paper_id, safe_slug):
    model_type = int(staged.get("model_type", 1))
    route = staged.get("route", "oral").lower()
    t_end = float(staged.get("t_end", 24.0))
    ode_method = staged.get("ode_method", "lsoda")
    
    # Safely get a param
    def get_p(key, default=0):
        val = flat_params.get(key)
        return float(val) if val is not None else default

    # Model parameters extracted directly into R code
    r_script = f"""# ==============================================================================
# APEX-PBPK Generated Standalone Model
# Paper: {staged.get('paper_title', paper_id)}
# Compound: {compound} | Route: {route} | Dose: {dose_val} mg/kg
# Model Type: {model_type} — {staged.get('model_description', '')}
# ==============================================================================

# Install deSolve if missing
if (!requireNamespace("deSolve", quietly = TRUE)) install.packages("deSolve")
library(deSolve)

# --- Extracted Parameters ---
BW <- {get_p('BW')}
QCC <- {get_p('QCC')}
Vliver <- {get_p('Vliver', get_p('V_liver'))}
V_plasma <- {get_p('V_plasma')}
Qliver <- {get_p('Qliver', get_p('QLiver'))}
Kp_liver <- {get_p('Kp_liver', 1.0)}
CL_hep <- {get_p('CL_hep')}
k_a <- {get_p('k_a')}
P_eff <- {get_p('P_eff')}
R_gut <- {get_p('R_gut')}

# --- 1. Calculate Micro-Rate Constants ---
"""
    if model_type == 1:
        r_script += """V_liv <- (Vliver / 100) * BW
V_pla <- (V_plasma / 100) * BW
Q_liv <- (Qliver / 100) * QCC * BW

k12 <- Q_liv / V_pla
k21 <- Q_liv / (Kp_liver * V_liv)
k10 <- CL_hep / V_liv
ka  <- k_a
"""
    elif model_type == 2:
        r_script += """V_liv <- Vliver
V_pla <- V_plasma
Q_liv <- Qliver

k12 <- Q_liv / V_pla
k21 <- Q_liv / (Kp_liver * V_liv)
k10 <- CL_hep / V_liv
ka  <- k_a
"""
    elif model_type == 3:
        r_script += """V_liv <- (Vliver / 100) * BW
V_pla <- (V_plasma / 100) * BW
Q_liv <- (Qliver / 100) * QCC * BW

k12 <- Q_liv / V_pla
k21 <- Q_liv / (Kp_liver * V_liv)
k10 <- CL_hep / V_liv

if (!is.na(P_eff) && !is.na(R_gut) && R_gut > 0) {
  ka <- P_eff * (2 / R_gut)
} else {
  ka <- k_a
}
"""
    elif model_type == 4:
        r_script += """V_liv <- (Vliver / 100) * BW
V_pla <- (V_plasma / 100) * BW
Q_liv <- (Qliver / 100) * QCC

k12 <- Q_liv / V_pla
k21 <- Q_liv / (Kp_liver * V_liv)
k10 <- CL_hep / V_liv
ka  <- k_a
"""
    
    r_script += f"""
rate_parms <- list(
  k_a = ka, k12 = k12, k21 = k21, k10 = k10,
  V_pla = V_pla, V_liv = V_liv, Kp = Kp_liver
)

# --- 2. ODE Equations ---
pbpk_ode <- function(t, state, parms) {{
  with(as.list(c(state, parms)), {{
    dA_gut         <- -k_a * A_gut
    dA_plasma      <-  k_a * A_gut + k21 * A_liver - k12 * A_plasma
    dA_liver       <-  k12 * A_plasma - k21 * A_liver - k10 * A_liver
    dA_metabolized <-  k10 * A_liver
    
    C_plasma <- A_plasma / V_pla
    C_liver  <- A_liver / (V_liv * Kp)
    
    list(c(dA_gut, dA_plasma, dA_liver, dA_metabolized), 
         C_plasma = C_plasma, 
         C_liver = C_liver)
  }})
}}

# --- 3. Simulation Execution ---
"""
    if route == "oral" or route == "dermal":
        r_script += f"init_state <- c(A_gut = {dose_val}, A_plasma = 0, A_liver = 0, A_metabolized = 0)\n"
    else:
        r_script += f"init_state <- c(A_gut = 0, A_plasma = {dose_val}, A_liver = 0, A_metabolized = 0)\n"
        
    r_script += f"""
times <- seq(0, {t_end}, by = 0.05)
out <- as.data.frame(ode(y = init_state, times = times, func = pbpk_ode, parms = rate_parms, method = "{ode_method}"))

# --- 4. Plotting ---
if (requireNamespace("ggplot2", quietly = TRUE)) {{
  library(ggplot2)
  p <- ggplot(out, aes(x = time)) +
    geom_line(aes(y = C_plasma, color = "Plasma Concentration"), linewidth = 1.2) +
    geom_line(aes(y = C_liver,  color = "Liver Concentration"), linewidth = 1.0, linetype = "dashed") +
    scale_color_manual(values = c("Plasma Concentration" = "#1f77b4", "Liver Concentration" = "#d62728")) +
    labs(title = "{compound} PBPK Simulation (Model {model_type})", x = "Time (h)", y = "Concentration", color = "") +
    theme_minimal()
  print(p)
}} else {{
  plot(out$time, out$C_plasma, type="l", col="blue", lwd=2, xlab="Time (h)", ylab="Concentration", main="{compound} PBPK")
  lines(out$time, out$C_liver, col="red", lwd=2, lty=2)
  legend("topright", legend=c("Plasma", "Liver"), col=c("blue", "red"), lty=c(1,2), lwd=2)
}}

# Cmax and AUC
cat("Cmax:", max(out$C_plasma), "\\n")
cat("AUC:", sum(diff(out$time) * (head(out$C_plasma, -1) + tail(out$C_plasma, -1)) / 2), "\\n")
"""
    return r_script
