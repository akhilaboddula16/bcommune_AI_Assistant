import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.supabase_client import get_supabase_client
from app.repositories.document_repository import DocumentRepository

settings = get_settings()


class DocumentService:
    def __init__(self, db: Session):
        self.document_repository = DocumentRepository(db)
        self.supabase = get_supabase_client()

    def upload_pdf(
        self,
        file: UploadFile,
        uploaded_by: int,
    ):
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File name is missing",
            )

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed",
            )

        file_bytes = file.file.read()

        if not file_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty",
            )

        unique_filename = f"{uuid.uuid4()}_{file.filename}"
        storage_path = f"pdfs/{unique_filename}"

        try:
            self.supabase.storage.from_(
                settings.supabase_storage_bucket
            ).upload(
                path=storage_path,
                file=file_bytes,
                file_options={
                    "content-type": "application/pdf",
                    "upsert": "false",
                },
            )

        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to upload file to Supabase Storage: {str(exc)}",
            )

        document = self.document_repository.create_document(
            filename=file.filename,
            storage_path=storage_path,
            uploaded_by=uploaded_by,
        )

        return {
            "id": document.id,
            "filename": document.filename,
            "storage_path": document.storage_path,
            "status": document.status,
        }

    def list_documents(self):
        return self.document_repository.get_all_documents()