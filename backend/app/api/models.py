from typing import List, Optional

from pydantic import BaseModel


class UploadResponse(BaseModel):
    document_id: str
    file_name: str
    gcs_path: str
    status: str
    message: str


class AnalysisRequest(BaseModel):
    document_id: str


class MedicalEntity(BaseModel):
    entity_type: str
    entity_value: str
    confidence_score: float
    metadata: Optional[dict] = None


class SafetyAlert(BaseModel):
    severity: str
    title: str
    description: str
    action_required: bool


class AnalysisResult(BaseModel):
    document_id: str
    document_type: str
    summary: str
    key_findings: List[str]
    extracted_entities: List[MedicalEntity]
    safety_assessment: List[SafetyAlert]
    processing_status: str


class AnalysisStatus(BaseModel):
    document_id: str
    status: str
    message: Optional[str] = None
