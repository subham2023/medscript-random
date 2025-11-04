from app.core.config import settings
from app.main import app
from app.services import firestore_service
from fastapi.testclient import TestClient

client = TestClient(app)


def test_analysis_status_not_found():
    doc_id = "does-not-exist"
    url = f"{settings.API_V1_STR}/analysis/{doc_id}/status"
    resp = client.get(url)
    assert resp.status_code == 404


def test_analysis_status_processing():
    doc_id = "doc-processing"
    firestore_service._IN_MEMORY_STORE.clear()
    # Seed record as processing
    client.app
    import anyio

    anyio.run(
        firestore_service.create_analysis_record,
        doc_id,
        {
            "document_id": doc_id,
            "processing_status": "processing",
            "message": "In progress",
        },
    )

    url = f"{settings.API_V1_STR}/analysis/{doc_id}/status"
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert data["document_id"] == doc_id
    assert data["status"] in ("processing", "analyzing", "unknown")


def test_analysis_result_not_ready():
    doc_id = "doc-not-ready"
    firestore_service._IN_MEMORY_STORE.clear()
    import anyio

    anyio.run(
        firestore_service.create_analysis_record,
        doc_id,
        {
            "document_id": doc_id,
            "processing_status": "processing",
            "message": "In progress",
        },
    )

    url = f"{settings.API_V1_STR}/analysis/{doc_id}"
    resp = client.get(url)
    assert resp.status_code == 404


def test_analysis_result_complete():
    doc_id = "doc-complete"
    firestore_service._IN_MEMORY_STORE.clear()
    complete_record = {
        "document_id": doc_id,
        "document_type": "prescription",
        "summary": "All good",
        "key_findings": ["finding-1"],
        "extracted_entities": [],
        "safety_assessment": [],
        "processing_status": "complete",
        "message": "done",
    }

    import anyio

    anyio.run(firestore_service.create_analysis_record, doc_id, complete_record)

    url = f"{settings.API_V1_STR}/analysis/{doc_id}"
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert data["document_id"] == doc_id
    assert data["processing_status"] == "complete"
    assert data["summary"] == "All good"
