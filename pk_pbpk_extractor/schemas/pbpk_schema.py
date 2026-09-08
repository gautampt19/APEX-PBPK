from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class TableContext(BaseModel):
    caption: Optional[str] = None
    species: Optional[str] = None
    route: Optional[str] = None
    dose_value: Optional[float] = None
    dose_unit: Optional[str] = None
    dose_raw: Optional[str] = None
    formulation: Optional[str] = None
    global_notes: List[str] = Field(default_factory=list)

class ExtractionRecord(BaseModel):
    record_id: str
    source_row_index: int
    source_column_index: int
    source_row_label: Optional[str] = None
    source_column_header: Optional[str] = None

    parameter_raw: Optional[str] = None
    parameter_normalized: Optional[str] = None
    parameter_category: Optional[str] = None
    is_target_parameter: bool = False
    organ_or_tissue: Optional[str] = None

    compound: Optional[str] = None
    species: Optional[str] = None
    sex: Optional[str] = None
    route: Optional[str] = None
    dose_value: Optional[float] = None
    dose_unit: Optional[str] = None
    dose_raw: Optional[str] = None
    formulation: Optional[str] = None

    cohort_or_condition: Optional[str] = None
    replicate_or_subject: Optional[str] = None
    value_index: int = 1

    value: Optional[float] = None
    unit: Optional[str] = None
    qualifier: Optional[str] = None

    deviation_value: Optional[float] = None
    deviation_unit: Optional[str] = None
    deviation_type: Optional[str] = None

    interval_lower: Optional[float] = None
    interval_upper: Optional[float] = None
    interval_unit: Optional[str] = None
    interval_type: Optional[str] = None

    raw_value: Optional[str] = None
    footnotes: List[str] = Field(default_factory=list)
    notes: Optional[str] = None

class RowAudit(BaseModel):
    source_row_index: int
    status: str
    record_ids: List[str] = Field(default_factory=list)

class ExtractedTablePayload(BaseModel):
    paper_id: str
    table_id: str
    table_context: TableContext = Field(default_factory=TableContext)
    records: List[ExtractionRecord] = Field(default_factory=list)
    row_audit: List[RowAudit] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
