from pk_pbpk_extractor.schemas.pbpk_schema import StudyContext, PKParameterRecord, ExtractedTablePayload

def test_study_context_validation():
    ctx = StudyContext(species="Human", formulation="IV", route="IV", dose=10.0, dose_unit="mg")
    assert ctx.species == "Human"

def test_payload_validation():
    data = {
        "paper_identifier": "10.123/abc",
        "table_id": "Table 1",
        "caption": "PK Params",
        "study_context": {
            "species": "Rat",
            "formulation": "Tablet",
            "route": "Oral",
            "dose": 50,
            "dose_unit": "mg/kg"
        },
        "blood_flow_fractions": {"Liver": 0.25},
        "volume_fractions": {"Liver": 0.04},
        "biochemical_parameters": [
            {
                "parameter_name": "CL_ren",
                "value": 1.5,
                "measure_type": "mean",
                "unit": "L/h"
            }
        ]
    }
    
    payload = ExtractedTablePayload(**data)
    assert payload.paper_identifier == "10.123/abc"
    assert len(payload.biochemical_parameters) == 1
