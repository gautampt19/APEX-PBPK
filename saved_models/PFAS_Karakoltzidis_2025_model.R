# ==============================================================================
# APEX-PBPK Generated Standalone Model
# Paper: Parsed from PFAS_Karakoltzidis_2025
# Compound: PFOA | Route: oral | Dose: 42.0 mg/kg
# Model Type: 4 — A mechanistic PBPK model for PFOA considering the distribution and metabolism in the human body.
# ==============================================================================

# Install deSolve if missing
if (!requireNamespace("deSolve", quietly = TRUE)) install.packages("deSolve")
library(deSolve)

# --- Extracted Parameters ---
BW <- 70.0
QCC <- 0.25
Vliver <- 0.026
V_plasma <- 0.184
Qliver <- 0.25
Kp_liver <- 0.1
CL_hep <- 0.04
k_a <- 0.001
P_eff <- 0
R_gut <- 0

# --- 1. Calculate Micro-Rate Constants ---
V_liv <- (Vliver / 100) * BW
V_pla <- (V_plasma / 100) * BW
Q_liv <- (Qliver / 100) * QCC * BW

k12 <- Q_liv / V_pla
k21 <- Q_liv / (Kp_liver * V_liv)
k10 <- CL_hep / V_liv
ka  <- k_a

rate_parms <- list(
  k_a = ka, k12 = k12, k21 = k21, k10 = k10,
  V_pla = V_pla, V_liv = V_liv, Kp = Kp_liver
)

# --- 2. ODE Equations ---
pbpk_ode <- function(t, state, parms) {
  with(as.list(c(state, parms)), {
    dA_gut         <- -k_a * A_gut
    dA_plasma      <-  k_a * A_gut + k21 * A_liver - k12 * A_plasma
    dA_liver       <-  k12 * A_plasma - k21 * A_liver - k10 * A_liver
    dA_metabolized <-  k10 * A_liver
    
    C_plasma <- A_plasma / V_pla
    C_liver  <- A_liver / (V_liv * Kp)
    
    list(c(dA_gut, dA_plasma, dA_liver, dA_metabolized), 
         C_plasma = C_plasma, 
         C_liver = C_liver)
  })
}

# --- 3. Simulation Execution ---
init_state <- c(A_gut = 42.0, A_plasma = 0, A_liver = 0, A_metabolized = 0)

times <- seq(0, 24.0, by = 0.05)
out <- as.data.frame(ode(y = init_state, times = times, func = pbpk_ode, parms = rate_parms, method = "lsoda"))

# --- 4. Plotting ---
if (requireNamespace("ggplot2", quietly = TRUE)) {
  library(ggplot2)
  p <- ggplot(out, aes(x = time)) +
    geom_line(aes(y = C_plasma, color = "Plasma Concentration"), linewidth = 1.2) +
    geom_line(aes(y = C_liver,  color = "Liver Concentration"), linewidth = 1.0, linetype = "dashed") +
    scale_color_manual(values = c("Plasma Concentration" = "#1f77b4", "Liver Concentration" = "#d62728")) +
    labs(title = "PFOA PBPK Simulation (Model 4)", x = "Time (h)", y = "Concentration", color = "") +
    theme_minimal()
  print(p)
} else {
  plot(out$time, out$C_plasma, type="l", col="blue", lwd=2, xlab="Time (h)", ylab="Concentration", main="PFOA PBPK")
  lines(out$time, out$C_liver, col="red", lwd=2, lty=2)
  legend("topright", legend=c("Plasma", "Liver"), col=c("blue", "red"), lty=c(1,2), lwd=2)
}

# Cmax and AUC
cat("Cmax:", max(out$C_plasma), "\n")
cat("AUC:", sum(diff(out$time) * (head(out$C_plasma, -1) + tail(out$C_plasma, -1)) / 2), "\n")
