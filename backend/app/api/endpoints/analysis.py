from fastapi import APIRouter, HTTPException
from app.api import models
from app.services import firestore_service

router = APIRouter()

@router.get("/analysis/{document_id}/status", response_model=models.AnalysisStatus)
async def get_analysis_status(document_id: str):
    """
    Get the current status of a document analysis from Firestore.
    """
    result = await firestore_service.get_analysis_by_id(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found.")

    return models.AnalysisStatus(
        document_id=result.get("document_id"),
        status=result.get("processing_status", "unknown"),
        message=result.get("message")
    )

@router.get("/analysis/{document_id}", response_model=models.AnalysisResult)
async def get_analysis_result(document_id: str):
    """
    Get the full analysis results for a document from Firestore.
    """
    result = await firestore_service.get_analysis_by_id(document_id)
    if not result:
        raise HTTPException(status_code=404, detail="Document not found.")

    if result.get("processing_status") != "complete":
        raise HTTPException(status_code=404, detail="Analysis not yet complete. Please check status endpoint.")

    # Pydantic will validate the structure against the AnalysisResult model
    return result