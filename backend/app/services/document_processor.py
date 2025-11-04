import os
import tempfile
import uuid

from fastapi import UploadFile
from google.cloud import storage, vision
from pypdf import PdfReader

BUCKET_NAME = os.getenv("DOCUMENT_UPLOAD_BUCKET", "medscript-uploads")


async def save_file(file: UploadFile, document_id: str) -> str:
    """
    Saves an uploaded file to Google Cloud Storage.
    Returns the GCS URI of the saved file.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    blob_name = f"uploads/{document_id}/{file.filename}"
    blob = bucket.blob(blob_name)

    contents = await file.read()
    blob.upload_from_string(contents, content_type=file.content_type)

    return f"gs://{BUCKET_NAME}/{blob_name}"


async def download_file_from_gcs(gcs_uri: str) -> str:
    """
    Downloads a file from GCS to a temporary local path.
    Required for libraries like pypdf that need a file path.
    """
    storage_client = storage.Client()
    bucket_name = gcs_uri.split("/")[2]
    blob_name = "/".join(gcs_uri.split("/")[3:])

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Create a temporary file and return its path
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=os.path.splitext(blob_name)[1]
    ) as temp_file:
        blob.download_to_file(temp_file)
        return temp_file.name


async def extract_text_from_image_with_ocr(gcs_uri: str) -> str:
    """
    Performs OCR on an image file in GCS using the Vision API.
    """
    client = vision.ImageAnnotatorAsyncClient()
    image = vision.Image()
    image.source.image_uri = gcs_uri

    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    request = vision.AnnotateImageRequest(image=image, features=[feature])

    response = await client.async_batch_annotate_images(requests=[request])

    full_text = ""
    for image_response in response.responses:
        if image_response.full_text_annotation:
            full_text += image_response.full_text_annotation.text
        if image_response.error.message:
            raise Exception(f"Vision API Error: {image_response.error.message}")

    return full_text


async def extract_text_from_pdf(local_file_path: str) -> str:
    """
    Extracts text from a local PDF file using pypdf.
    """
    extracted_text = ""
    try:
        reader = PdfReader(local_file_path)
        for page in reader.pages:
            extracted_text += page.extract_text() + "\n"
    finally:
        os.remove(local_file_path)  # Clean up the temporary file

    return extracted_text
