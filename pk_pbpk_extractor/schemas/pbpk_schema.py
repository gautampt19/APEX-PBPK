from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class StudyContext(BaseModel):
    compound: Optional[str] = Field(None, description="The specific compound or analyte (e.g. BPA, BPS)")
    cohort_or_condition: Optional[str] = Field(None, description="The demographic cohort, subject ID, or experimental condition (e.g. Male, Volunteer 3, Fasted, Model Predicted)")
    species: str = Field(description="Species like human, rat, mouse, dog, etc.")
    formulation: str = Field(description="Formulation like ASD, tablet, solution, suspension, etc.")
    route: str = Field(description="Administration route like oral, IV, SC, IP, etc.")
    dose: float = Field(description="Dose amount")
    dose_unit: str = Field(description="Dose unit like mg, mg/kg, ug, etc.")

class PKParameterRecord(BaseModel):
    compound: Optional[str] = Field(None, description="The specific compound or analyte for this row (e.g. BPA, BPS)")
    cohort_or_condition: Optional[str] = Field(None, description="The specific demographic cohort, subject ID, or condition for this row")
    parameter_name: str = Field(description="The PK parameter name, e.g., CL_ren, Vmax, Km, Kp")
    value: float = Field(description="The extracted value")
    deviation_value: Optional[float] = Field(None, description="Standard deviation or standard error, if any")
    measure_type: str = Field(description="Type of measure: mean, SD, SE, median, etc.")
    unit: str = Field(description="Unit of the parameter, e.g., ul/h/kg^0.25, mg/L")

class ExtractedTablePayload(BaseModel):
    paper_identifier: str = Field(description="DOI or PMCID of the paper")
    table_id: str = Field(description="Table identifier, e.g., Table 1, Table 2")
    caption: str = Field(description="Table caption text")
    study_context: StudyContext = Field(description="Context of the study for this table")
    blood_flow_fractions: Dict[str, float] = Field(description="Organ blood flow fractions (Q)")
    volume_fractions: Dict[str, float] = Field(description="Organ volume fractions (V)")
    biochemical_parameters: List[PKParameterRecord] = Field(description="List of biochemical and PK parameters")
