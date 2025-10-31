from fastapi import APIRouter, HTTPException
from app.api import models

router = APIRouter()

# This is a mock database to store analysis results for now.
# In a real application, this would be replaced by a service that
# interacts with Firestore.
mock_analysis_db = {}

@router.get("/analysis/{document_id}/status", response_model=models.AnalysisStatus)
async def get_analysis_status(document_id: str):
    """
    Get the status of a document analysis.
    """
    if document_id in mock_analysis_db:
        return mock_analysis_db[document_id]
    
    # Simulate a document that is still being processed
    if "processing" in document_id:
        return {
            "document_id": document_id,
            "status": "processing",
            "message": "Document analysis is in progress."
        }
        
    raise HTTPException(status_code=404, detail="Document not found.")

@router.get("/analysis/{document_id}", response_model=models.AnalysisResult)
async def get_analysis_result(document_id: str):
    """
    Get the full analysis results for a document.
    """
    if document_id in mock_analysis_db and mock_analysis_db[document_id]["status"] == "complete":
        return mock_analysis_db[document_id]

    # Add a mock result for demonstration purposes
    mock_analysis_db[document_id] = {
        "document_id": document_id,
        "document_type": "prescription",
        "summary": "This is a prescription for Metformin, a common medication for Type 2 diabetes.",
        "key_findings": [
            "Medication: Metformin 500mg",
            "Dosage: Twice daily"
        ],
        "extracted_entities": [
            {"entity_type": "medication", "entity_value": "Metformin", "confidence_score": 0.98},
            {"entity_type": "dosage", "entity_value": "500mg", "confidence_score": 0.95},
            {"entity_type": "frequency", "entity_value": "twice daily", "confidence_score": 0.92}
        ],
        "safety_assessment": [
            {"severity": "low", "title": "No critical interactions found", "description": "No critical drug interactions were found with the provided information.", "action_required": False}
        ],
        "processing_status": "complete"
    }
    
    if document_id in mock_analysis_db:
        return mock_analysis_db[document_id]
        
    raise HTTPException(status_code=404, detail="Analysis not complete or document not found.")
