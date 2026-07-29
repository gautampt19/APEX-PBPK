import re
import json
import requests
import logging
from .config import OLLAMA_API_URL, OLLAMA_MODEL, OLLAMA_CONTEXT_SIZE, OLLAMA_TEMPERATURE

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_pbpk_json_prompt(paper_text: str) -> str:
    """
    Formulates a prompt asking Ollama to extract PBPK parameters in JSON format.
    """
    system_instructions = (
        "You are an expert data extractor for pharmacokinetic models. Your task is to read the provided paper excerpt "
        "and extract all PBPK parameters (body weight, cardiac output, organ blood flows, organ volumes, partition coefficients, "
        "and biochemical constants like Km, Vmax, clearances, and absorption rates) into a flat JSON object.\n\n"
        "Please map the extracted parameters to the following keys where applicable:\n"
        "- BW (body weight in kg)\n"
        "- Dose (mg/kg)\n"
        "- Qc (cardiac output in L/h)\n"
        "- QL, QK, QH, QB, QF (liver, kidney, heart, brain, fat blood flow fractions of Qc)\n"
        "- VL, VLu, VK, VH, VB, VF, VP (liver, lung, kidney, heart, brain, fat, plasma volume fractions of body weight)\n"
        "- PL, PLu, PK, PH, PB, PF, PR (liver, lung, kidney, heart, brain, fat, rest of body partition coefficients)\n"
        "- Kabs (absorption rate constant, 1/h)\n"
        "- Fu (fraction unbound in plasma)\n"
        "- Vmax (maximum metabolism velocity in nmol/h/kg^0.75)\n"
        "- Km (Michaelis-Menten constant, umol/L)\n"
        "- Clurine (renal clearance, uL/h)\n"
        "- Kfeces (fecal clearance, 1/h)\n\n"
        "Requirements:\n"
        "1. Extract the actual numerical values from the paper text (especially Table I or optimized value sections).\n"
        "2. If multiple values are given (e.g. for tablet vs ASD, or rat vs human), extract the rat values or the default tablet values.\n"
        "3. Output ONLY the JSON block wrapped in ```json ... ```. Do not include any explanation or extra text outside the JSON block."
    )
    
    user_request = (
        f"Here are the PBPK paper details containing the parameters:\n\n"
        f"{paper_text}\n\n"
        "Please extract the parameters as a JSON object."
    )
    
    return f"{system_instructions}\n\nUser Request:\n{user_request}"

def extract_parameters_json(paper_text: str) -> dict:
    """
    Asks Ollama to extract parameters as JSON and returns a Python dictionary.
    """
    prompt = get_pbpk_json_prompt(paper_text)
    
    payload = {
        'model': OLLAMA_MODEL,
        'prompt': prompt,
        'stream': False,
        'options': {
            'temperature': 0.0,
            'num_ctx': OLLAMA_CONTEXT_SIZE
        }
    }
    
    logging.info(f"Extracting parameters via Ollama JSON mode...")
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
    except Exception as e:
        raise ConnectionError(f"Failed to communicate with local Ollama: {e}")
        
    result_text = response.json().get('response', '').strip()
    
    json_match = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1).strip()
    else:
        json_str = result_text
        
    try:
        data = json.loads(json_str)
        logging.info("Successfully extracted and parsed JSON parameters.")
        return data
    except Exception as e:
        logging.warning(f"Failed to parse JSON output: {e}. Output was:\n{result_text}")
        return {}

def get_model_schema_prompt(paper_text: str) -> str:
    """
    Formulates a prompt asking Ollama to extract PBPK model structure AND parameters in JSON format.
    """
    system_instructions = (
        "You are an expert pharmacokinetic modeling scientist. Your task is to read the provided PBPK paper text "
        "and extract both the model architecture schema AND all numerical parameters into a single JSON object.\n\n"
        "Output JSON Structure required:\n"
        "{\n"
        "  \"schema\": {\n"
        "    \"species\": \"rat\" or \"human\",\n"
        "    \"route\": \"oral\" or \"iv\",\n"
        "    \"compartments\": [\"liver\", \"kidney\", \"brain\", \"fat\", \"lung\", \"rest\"],\n"
        "    \"has_lung_compartment\": true or false,\n"
        "    \"has_ehr\": true or false\n"
        "  },\n"
        "  \"parameters\": {\n"
        "    \"BW\": 0.25,\n"
        "    \"Dose\": 10.0,\n"
        "    \"Qc\": 15.0,\n"
        "    \"QL\": 0.174,\n"
        "    \"QK\": 0.141,\n"
        "    \"QB\": 0.02,\n"
        "    \"QF\": 0.07,\n"
        "    \"VL\": 0.036,\n"
        "    \"VK\": 0.0073,\n"
        "    \"VB\": 0.006,\n"
        "    \"VF\": 0.07,\n"
        "    \"VP\": 0.074,\n"
        "    \"PL\": 2.2,\n"
        "    \"PK\": 4.62,\n"
        "    \"PB\": 2.44,\n"
        "    \"PF\": 14.12,\n"
        "    \"Kabs\": 0.69,\n"
        "    \"Fu\": 0.04,\n"
        "    \"Vmax\": 250000.0,\n"
        "    \"Km\": 140.0,\n"
        "    \"Clurine\": 0.3771,\n"
        "    \"Kfeces\": 0.013\n"
        "  }\n"
        "}\n\n"
        "Requirements:\n"
        "1. Identify the compartments described in the paper.\n"
        "2. Extract real numeric parameter values present in the text/tables.\n"
        "3. Output ONLY valid JSON wrapped in ```json ... ```. No additional commentary."
    )
    
    user_request = (
        f"Here are the PBPK paper details:\n\n"
        f"{paper_text}\n\n"
        "Please extract the model schema and parameters JSON."
    )
    
    return f"{system_instructions}\n\nUser Request:\n{user_request}"

def extract_model_schema_and_params(paper_text: str) -> dict:
    """
    Asks Ollama to extract model schema and parameters as JSON.
    Returns dict with keys 'schema' and 'parameters'.
    """
    prompt = get_model_schema_prompt(paper_text)
    
    payload = {
        'model': OLLAMA_MODEL,
        'prompt': prompt,
        'stream': False,
        'options': {
            'temperature': 0.0,
            'num_ctx': OLLAMA_CONTEXT_SIZE
        }
    }
    
    logging.info(f"Extracting PBPK model schema and parameters via Ollama...")
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
    except Exception as e:
        logging.warning(f"Ollama connection error: {e}")
        return {"schema": {}, "parameters": {}}
        
    result_text = response.json().get('response', '').strip()
    
    json_match = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1).strip()
    else:
        json_str = result_text
        
    try:
        data = json.loads(json_str)
        logging.info("Successfully extracted model schema and parameters.")
        return data
    except Exception as e:
        logging.warning(f"Failed to parse model schema JSON: {e}")
        return {"schema": {}, "parameters": {}}

