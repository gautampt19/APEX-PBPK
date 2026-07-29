import os
import re
import subprocess
import pandas as pd
import logging
from typing import Dict, Any
from .config import R_EXECUTABLE, TEMP_RUN_SCRIPT, SIMULATION_OUTPUT_CSV

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def inject_parameters(r_script_content: str, parameters: Dict[str, Any]) -> str:
    """
    Substitutes custom values for parameters inside the params <- c(...) R vector.
    """
    modified_content = r_script_content
    for param, value in parameters.items():
        # Match parameter definition: name = <number> or name= <number> followed by comma, space, or close parenthesis
        pattern = re.compile(r'(' + re.escape(param) + r'\s*=\s*)[-+]?\d*\.?\d+(e[-+]?\d+)?')
        if pattern.search(modified_content):
            modified_content = pattern.sub(f'\\g<1>{value}', modified_content)
            logging.info(f"Overrode parameter: {param} = {value}")
        else:
            logging.warning(f"Parameter '{param}' not found in R script params vector.")
            
    return modified_content

def execute_r_simulation(r_script_path: str, parameters: Dict[str, Any] = None) -> pd.DataFrame:
    """
    Injects parameters (if any), runs the R simulation, and returns the result DataFrame.
    """
    if not os.path.exists(R_EXECUTABLE):
        raise FileNotFoundError(f"Rscript executable not found at: {R_EXECUTABLE}")
        
    with open(r_script_path, 'r', encoding='utf-8') as f:
        r_content = f.read()
        
    if parameters:
        logging.info("Injecting custom parameters into script...")
        r_content = inject_parameters(r_content, parameters)
        
    # Write to a temporary run script
    with open(TEMP_RUN_SCRIPT, 'w', encoding='utf-8') as f:
        f.write(r_content)
    logging.info(f"Temporary simulation script saved to: {TEMP_RUN_SCRIPT}")
    
    # Execute Rscript
    logging.info("Executing R simulation...")
    result = subprocess.run([R_EXECUTABLE, TEMP_RUN_SCRIPT], capture_output=True, text=True)
    
    if result.returncode != 0:
        logging.error("R simulation failed!")
        logging.error(f"STDOUT: {result.stdout}")
        logging.error(f"STDERR: {result.stderr}")
        raise RuntimeError(f"R script execution failed: {result.stderr}")
        
    logging.info("R simulation completed successfully.")
    
    # Read the output CSV
    if not os.path.exists(SIMULATION_OUTPUT_CSV):
        raise FileNotFoundError(f"Expected simulation output CSV not found at: {SIMULATION_OUTPUT_CSV}")
        
    df = pd.read_csv(SIMULATION_OUTPUT_CSV)
    logging.info(f"Loaded simulation data: {len(df)} rows, columns: {list(df.columns)}")
    return df
