import re

def normalize_unit(raw_unit: str) -> str:
    if not raw_unit:
        return ""
        
    unit = raw_unit.lower().strip()
    
    # Replace 'per' with '/'
    unit = unit.replace(" per ", "/")
    unit = unit.replace("per ", "/")
    
    # Handle kg0.25 -> kg^0.25
    unit = re.sub(r'kg([0-9.]+)', r'kg^\1', unit)
    
    # Standardize common symbols
    unit = unit.replace("ucl", "ul")
    unit = unit.replace("µl", "ul")
    unit = unit.replace("mcg", "ug")
    unit = unit.replace("µg", "ug")
    
    return unit
