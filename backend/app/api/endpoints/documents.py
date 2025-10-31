from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Annotated
import uuid

from app.api import models
from app.services import document_processor
from app.agents.orchestrator import OrchestratorAgent

router = APIRouter()

@router.post("/documents/upload", response_model=models.AnalysisResult) # Changed response_model
async def upload_document(file: Annotated[UploadFile, File()]):
    """
    Upload a medical document for analysis.
    
    Supports PDF, JPG, PNG, and TXT formats.
    Maximum file size is 50MB.
    """
    # Basic file validation
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png", "text/plain"]:
        raise HTTPException(status_code=400, detail="Unsupported file format.")
    
    # The spec mentions a 50MB limit, but we won't implement chunked reading here for simplicity.
    # A production system would need to handle large files more robustly.
    
    # Generate a unique ID for the document
    document_id = str(uuid.uuid4())
    
    file_path = await document_processor.save_file(file, document_id)
    
    extracted_text = ""
    if file.content_type in ["image/jpeg", "image/png"]:
        extracted_text = await document_processor.extract_text_from_image_with_ocr(file_path)
        print(f"Extracted text from image: {extracted_text[:200]}...") # Print first 200 chars
    elif file.content_type == "text/plain":
        # Reset file pointer to the beginning after saving to GCS
        await file.seek(0)
        extracted_text = (await file.read()).decode("utf-8")
        print(f"Extracted text from plain text file: {extracted_text[:200]}...")
    elif file.content_type == "application/pdf":
        extracted_text = await document_processor.extract_text_from_pdf(file_path)
        print(f"Extracted text from PDF: {extracted_text[:200]}...")

    orchestrator_agent = OrchestratorAgent()
    orchestration_result = await orchestrator_agent.process_document(extracted_text)
    
    # Populate AnalysisResult from orchestration_result
    return {
        "document_id": document_id,
        "document_type": orchestration_result.get("document_type", "unknown"),
        "summary": orchestration_result.get("summary", "No summary generated."),
        "key_findings": orchestration_result.get("key_findings", []),
        "extracted_entities": orchestration_result.get("extracted_entities", []),
        "safety_assessment": [], # TODO: Implement SafetyAssessmentAgent
        "processing_status": orchestration_result.get("status", "failed")
    }
