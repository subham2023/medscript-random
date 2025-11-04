from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "MedScript AI"
    API_V1_STR: str = "/api/v1"

    # Google Cloud Settings
    GOOGLE_CLOUD_PROJECT: str = "your-gcp-project-id"

    # Firestore Settings
    FIRESTORE_DATABASE: str = "medscript-db"

    # Cloud Storage Settings
    DOCUMENT_UPLOAD_BUCKET: str = "medscript-uploads"
    PROCESSED_DOCUMENTS_BUCKET: str = "medscript-processed"

    class Config:
        case_sensitive = True


settings = Settings()
