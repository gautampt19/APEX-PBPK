# APEX-PBPK: Automated Parameter Extraction & Execution for PBPK

**APEX-PBPK** is an end-to-end biocomputational framework that automatically extracts model architecture topologies and physiological parameters directly from scientific literature (PDFs) using LLMs (e.g. Gemma 4), programmatically compiles Ordinary Differential Equation (ODE) systems for R `deSolve`, runs biosimulated kinetics, and performs Non-Compartmental Analysis (NCA) validation.

---

## 🧬 Architecture Overview

```
                        +----------------------------+
                        |  Scientific PDF Literature  |
                        +--------------+-------------+
                                       |
                                       v
                        +----------------------------+
                        |   pdf_extractor.py         |
                        | (Keyword Page Scoring)     |
                        +--------------+-------------+
                                       |
                                       v
                        +----------------------------+
                        |   llm_manager.py           |
                        | (Ollama Gemma 4:31b JSON)  |
                        +--------------+-------------+
                                       |
                                       v
                        +----------------------------+
                        |   r_builder.py             |
                        | (deSolve ODE Synthesis)    |
                        +--------------+-------------+
                                       |
                                       v
                        +----------------------------+
                        |   r_executor.py            |
                        | (Rscript Execution Engine) |
                        +--------------+-------------+
                                       |
                                       v
                        +----------------------------+
                        |   validator.py             |
                        | (NCA Metrics & Plots)      |
                        +----------------------------+
```

---

## 🚀 Features

- **Automated Literature Mining**: Extracts physiological parameters ($BW$, $Dose$, organ flows, volume fractions, partition coefficients, $V_{max}$, $K_m$, clearances) and tissue compartment topologies from PDF papers using local LLMs.
- **Dynamic ODE Compiler**: Synthesizes R scripts utilizing `deSolve` to handle arbitrary compartment setups (e.g., organ systems, gut absorption, enterohepatic recirculation).
- **Physiological Verification**: Automatically validates concentration outputs for non-negativity and consistency.
- **Pharmacokinetic Metrics**: Computes Non-Compartmental Analysis (NCA) metrics including $C_{max}$, $T_{max}$, and $AUC_{0-24h}$.

---

## 📋 Requirements & Setup

### Python Dependencies
Install required Python libraries:
```bash
pip install -r requirements.txt
```

### R & deSolve
Ensure R is installed with the `deSolve` package:
```R
install.packages("deSolve")
```

### Local LLM Engine (Ollama)
Ensure [Ollama](https://ollama.ai/) is running with your preferred model (e.g. `gemma4:31b` or `qwen2.5-coder:7b`):
```bash
ollama run gemma4:31b
```

---

## 🖥️ Usage

Run **APEX-PBPK** on a research paper PDF:

```bash
python3 -m pbpk_generator_project.main --pdf "papers/s12249-023-02680-y.pdf"
```

### Command-Line Arguments
- `--pdf`: Path to input PBPK paper PDF.
- `--dose`: (Optional) Override dose parameter (mg/kg).
- `--bw`: (Optional) Override body weight parameter (kg).
- `--no-plot`: (Optional) Suppress generation of matplotlib visualization plots.

---

## 📊 Module Reference

- `pdf_extractor.py`: Ranks PDF pages by keyword match density to extract high-yield parameter sections.
- `llm_manager.py`: Interfaces with Ollama API to extract model schemas and numerical parameters in JSON format.
- `r_builder.py`: Generates R `deSolve` ODE scripts with sanitized compartment identifiers.
- `r_executor.py`: Executes generated R scripts via subprocess and parses output simulation CSVs.
- `validator.py`: Performs non-compartmental analysis (NCA) and physiological validation checks.
- `config.py`: Centralized configuration settings and fallback parameter dictionaries.
