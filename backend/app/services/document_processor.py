from google.cloud import storage
from google.cloud import vision_v1 as vision
import os
import uuid
import tempfile
from pypdf import PdfReader

async def save_file(file: UploadFile, document_id: str) -> str:
    """
    Saves an uploaded file to Google Cloud Storage.
    
    Args:
        file: The UploadFile object from FastAPI.
        document_id: A unique identifier for the document.
        
    Returns:
        The GCS URI of the saved file.
    """
    bucket_name = os.getenv("DOCUMENT_UPLOAD_BUCKET", "medscript-uploads")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    # Create a unique blob name to avoid collisions
    blob_name = f"uploads/{document_id}/{file.filename}"
    blob = bucket.blob(blob_name)
    
    # Upload the file
    contents = await file.read()
    blob.upload_from_string(contents, content_type=file.content_type)
    
    return f"gs://{bucket_name}/{blob_name}"

async def extract_text_from_image_with_ocr(gcs_uri: str) -> str:
    """
    Performs OCR on an image file stored in Google Cloud Storage using Google Cloud Vision API.
    
    Args:
        gcs_uri: The GCS URI of the image file (e.g., "gs://your-bucket/your-image.jpg").
        
    Returns:
        The extracted text from the image.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = gcs_uri
    
    response = client.document_text_detection(image=image)
    full_text = response.full_text_annotation.text
    
    return full_text

async def extract_text_from_pdf(gcs_uri: str) -> str:
    """
    Extracts text from a PDF file stored in Google Cloud Storage using pypdf.
    
    Args:
        gcs_uri: The GCS URI of the PDF file (e.g., "gs://your-bucket/your-document.pdf").
        
    Returns:
        The extracted text from the PDF.
    """
    storage_client = storage.Client()
    
    # Parse bucket name and blob name from GCS URI
    bucket_name = gcs_uri.split('/')[2]
    blob_name = '/'.join(gcs_uri.split('/')[3:])
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Download the PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        blob.download_to_file(temp_file)
        temp_file_path = temp_file.name
    
    extracted_text = ""
    try:
        reader = PdfReader(temp_file_path)
        for page in reader.pages:
            extracted_text += page.extract_text() + "\n"
    finally:
        os.remove(temp_file_path) # Clean up the temporary file
        
    return extracted_text
