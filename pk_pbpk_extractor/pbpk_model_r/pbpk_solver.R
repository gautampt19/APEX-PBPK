#!/usr/bin/env Rscript
# ==============================================================================
# PBPK Simulation Engine in R (Models 1, 2, 3, 4 from Final_Pharmacokinetic_ODEs)
# Dependencies: deSolve, jsonlite, ggplot2
# ==============================================================================

suppressPackageStartupMessages({
  library(deSolve)
  library(jsonlite)
  library(ggplot2)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) {
  stop("Usage: Rscript pbpk_solver.R <input_params.json> [output_prefix]")
}

input_json_path <- args[1]
output_prefix   <- ifelse(length(args) >= 2, args[2], "pbpk_result")

params_data <- fromJSON(input_json_path)

model_type <- as.integer(params_data$model_type)
dose       <- as.numeric(params_data$dose)
route      <- tolower(params_data$route)
t_end      <- ifelse(!is.null(params_data$t_end), as.numeric(params_data$t_end), 24.0)
p          <- params_data$parameters

cat(sprintf("[PBPK-R] Running Model %d (%s) for %s | Dose: %g | Route: %s\n", 
            model_type, params_data$model_description, params_data$compound, dose, route))

# Helper to safely get parameter or default
get_val <- function(x, default = 0) {
  if (is.null(x)) return(default)
  return(as.numeric(x))
}

# ── 1. Calculate Micro-Rate Constants (k12, k21, k10, ka) ──────────────────────
if (model_type == 1) {
  # Model 1: Percentages of BW & QCC
  V_liv <- (get_val(p$Vliver) / 100) * get_val(p$BW)
  V_pla <- (get_val(p$V_plasma) / 100) * get_val(p$BW)
  Q_liv <- (get_val(p$Qliver) / 100) * get_val(p$QCC) * get_val(p$BW)
  
  k12 <- Q_liv / V_pla
  k21 <- Q_liv / (get_val(p$Kp_liver, 1) * V_liv)
  k10 <- get_val(p$CL_hep) / V_liv
  ka  <- get_val(p$k_a)

} else if (model_type == 2) {
  # Model 2: Absolute Physiological Values (L, L/h)
  V_liv <- get_val(p$V_liver, get_val(p$Vliver))
  V_pla <- get_val(p$V_plasma)
  
  Q_liv <- get_val(p$QLiver, get_val(p$Qliver))
  k12 <- Q_liv / V_pla
  k21 <- Q_liv / (get_val(p$Kp_liver, 1) * V_liv)
  k10 <- get_val(p$CL_hep) / V_liv
  ka  <- get_val(p$k_a)

} else if (model_type == 3) {
  # Model 3: Mechanistic Absorption via Peff & Rgut
  V_liv <- (get_val(p$Vliver) / 100) * get_val(p$BW)
  V_pla <- (get_val(p$V_plasma) / 100) * get_val(p$BW)
  Q_liv <- (get_val(p$Qliver) / 100) * get_val(p$QCC) * get_val(p$BW)
  
  k12 <- Q_liv / V_pla
  k21 <- Q_liv / (get_val(p$Kp_liver, 1) * V_liv)
  k10 <- get_val(p$CL_hep) / V_liv
  
  if (!is.null(p$P_eff) && !is.null(p$R_gut) && p$R_gut > 0) {
    ka  <- get_val(p$P_eff) * (2 / get_val(p$R_gut))
  } else {
    ka <- get_val(p$k_a)
  }

} else if (model_type == 4) {
  # Model 4: Flow as % of QCC
  V_liv <- (get_val(p$Vliver) / 100) * get_val(p$BW)
  V_pla <- (get_val(p$V_plasma) / 100) * get_val(p$BW)
  Q_liv <- (get_val(p$Qliver) / 100) * get_val(p$QCC) * get_val(p$BW)
  
  k12 <- Q_liv / V_pla
  k21 <- Q_liv / (get_val(p$Kp_liver, 1) * V_liv)
  k10 <- get_val(p$CL_hep) / V_liv
  ka  <- get_val(p$k_a)
}

rate_parms <- list(
  k_a = ka, k12 = k12, k21 = k21, k10 = k10,
  V_pla = V_pla, V_liv = V_liv, Kp = p$Kp_liver
)

# ── 2. ODE Equations ─────────────────────────────────────────────────────────
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

# ── 3. Simulation Execution ──────────────────────────────────────────────────
init_state <- if (route == "oral") {
  c(A_gut = dose, A_plasma = 0, A_liver = 0, A_metabolized = 0)
} else {
  c(A_gut = 0, A_plasma = dose, A_liver = 0, A_metabolized = 0)
}

times <- seq(0, t_end, by = 0.05)
ode_method <- ifelse(!is.null(params_data$ode_method), params_data$ode_method, "lsoda")
out <- as.data.frame(ode(y = init_state, times = times, func = pbpk_ode, parms = rate_parms, method = ode_method))

# ── 4. PK Metrics Calculation ────────────────────────────────────────────────
c_max  <- max(out$C_plasma)
t_max  <- out$time[which.max(out$C_plasma)]
auc    <- sum(diff(out$time) * (head(out$C_plasma, -1) + tail(out$C_plasma, -1)) / 2)

metrics <- list(
  compound   = params_data$compound,
  model_type = model_type,
  Cmax       = round(c_max, 4),
  Tmax       = round(t_max, 2),
  AUC_0_t    = round(auc, 4),
  dose       = dose,
  route      = route
)

# Save Metrics JSON & Simulation CSV
write_json(metrics, paste0(output_prefix, "_metrics.json"), pretty = TRUE)
write.csv(out, paste0(output_prefix, "_simulation.csv"), row.names = FALSE)

# ── 5. Generate Plot ─────────────────────────────────────────────────────────
p_plot <- ggplot(out, aes(x = time)) +
  geom_line(aes(y = C_plasma, color = "Plasma Concentration"), linewidth = 1.2) +
  geom_line(aes(y = C_liver,  color = "Liver Concentration"), linewidth = 1.0, linetype = "dashed") +
  scale_color_manual(values = c("Plasma Concentration" = "#1f77b4", "Liver Concentration" = "#d62728")) +
  labs(
    title = sprintf("PBPK Model Simulation: %s (Model %d)", params_data$compound, model_type),
    subtitle = sprintf("Dose: %g (%s) | Cmax: %g | AUC(0-%gh): %g", dose, route, metrics$Cmax, t_end, metrics$AUC_0_t),
    x = "Time (hours)", y = "Concentration (mg/L or mass/vol)",
    color = "Compartment"
  ) +
  theme_minimal(base_size = 13) +
  theme(legend.position = "bottom")

ggsave(paste0(output_prefix, "_plot.png"), plot = p_plot, width = 8, height = 5, dpi = 300)
cat(sprintf("[PBPK-R] Simulation complete! Saved: %s_plot.png\n", output_prefix))
