import datetime
import uuid
from typing import Annotated

from app.api import models
from app.services import (document_processor, firestore_service,
                          medical_analyzer)
from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from google.cloud import firestore

router = APIRouter()


@router.post("/documents/upload", response_model=models.AnalysisStatus)
async def upload_document(
    background_tasks: BackgroundTasks, file: Annotated[UploadFile, File()]
):
    """
    Upload a medical document for asynchronous analysis.
    This endpoint immediately returns a document ID and starts the analysis in the background.

    Supports PDF, JPG, PNG, and TXT formats.
    Maximum file size is 50MB.
    """
    # Basic file validation
    if file.content_type not in [
        "application/pdf",
        "image/jpeg",
        "image/png",
        "text/plain",
    ]:
        raise HTTPException(status_code=400, detail="Unsupported file format.")

    document_id = str(uuid.uuid4())

    try:
        # Save the uploaded file to GCS
        gcs_path = await document_processor.save_file(file, document_id)

        # Create an initial record in Firestore
        initial_data = {
            "document_id": document_id,
            "file_name": file.filename,
            "gcs_path": gcs_path,
            "status": "processing",
            "message": "Document uploaded and queued for analysis.",
            "uploaded_at": firestore.SERVER_TIMESTAMP,
        }
        await firestore_service.create_analysis_record(document_id, initial_data)

        # Reset file pointer to read content for text extraction
        await file.seek(0)

        # Extract text from the document
        extracted_text = ""
        if file.content_type in ["image/jpeg", "image/png"]:
            extracted_text = await document_processor.extract_text_from_image_with_ocr(
                gcs_path
            )
        elif file.content_type == "text/plain":
            extracted_text = (await file.read()).decode("utf-8")
        elif file.content_type == "application/pdf":
            # pypdf needs a local file path, so we download it from GCS
            local_path = await document_processor.download_file_from_gcs(gcs_path)
            extracted_text = await document_processor.extract_text_from_pdf(local_path)

        # Add the analysis task to run in the background
        background_tasks.add_task(
            medical_analyzer.analyze_document_in_background, document_id, extracted_text
        )

        return models.AnalysisStatus(
            document_id=document_id,
            status="processing",
            message="Document upload successful, analysis has started.",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
