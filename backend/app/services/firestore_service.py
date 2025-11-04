from google.cloud import firestore
from typing import Dict, Any, Optional

# Initialize Firestore client
db = firestore.AsyncClient()

async def get_analysis_by_id(document_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a document analysis result from Firestore.
    """
    doc_ref = db.collection("document_analyses").document(document_id)
    doc = await doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

async def create_analysis_record(document_id: str, data: Dict[str, Any]) -> None:
    """
    Creates a new document analysis record in Firestore.
    """
    doc_ref = db.collection("document_analyses").document(document_id)
    await doc_ref.set(data)

async def update_analysis_record(document_id: str, data: Dict[str, Any]) -> None:
    """
    Updates an existing document analysis record in Firestore.
    """
    doc_ref = db.collection("document_analyses").document(document_id)
    await doc_ref.update(data)