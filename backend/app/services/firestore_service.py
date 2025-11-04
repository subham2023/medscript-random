import datetime
from typing import Any, Dict, Optional

# Firestore async client may not be available or credentials may be missing in CI.
# Provide a safe import with fallback to an in-memory store for tests.
try:
    from google.cloud import \
        firestore as firestore_sync  # for SERVER_TIMESTAMP
    from google.cloud import firestore_async as firestore

    db = firestore.AsyncClient()
    SERVER_TIMESTAMP = firestore_sync.SERVER_TIMESTAMP
except Exception:
    db = None
    SERVER_TIMESTAMP = datetime.datetime.utcnow()

# In-memory fallback store used when Firestore is unavailable (e.g., in CI/tests)
_IN_MEMORY_STORE: Dict[str, Dict[str, Any]] = {}
_COLLECTION_NAME = "document_analyses"


async def get_analysis_by_id(document_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a document analysis result from Firestore or the in-memory fallback.
    """
    if db is None:
        return _IN_MEMORY_STORE.get(document_id)

    doc_ref = db.collection(_COLLECTION_NAME).document(document_id)
    doc = await doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None


async def create_analysis_record(document_id: str, data: Dict[str, Any]) -> None:
    """
    Creates a new document analysis record in Firestore or the in-memory fallback.
    """
    if db is None:
        _IN_MEMORY_STORE[document_id] = dict(data)
        return

    doc_ref = db.collection(_COLLECTION_NAME).document(document_id)
    await doc_ref.set(data)


async def update_analysis_record(document_id: str, data: Dict[str, Any]) -> None:
    """
    Updates an existing document analysis record in Firestore or the in-memory fallback.
    """
    if db is None:
        current = _IN_MEMORY_STORE.get(document_id, {})
        current.update(dict(data))
        _IN_MEMORY_STORE[document_id] = current
        return

    doc_ref = db.collection(_COLLECTION_NAME).document(document_id)
    await doc_ref.update(data)
