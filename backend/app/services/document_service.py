import uuid

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.supabase_client import get_supabase_client
from app.repositories.document_repository import DocumentRepository
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.utils.pdf_parser import extract_text_from_pdf
from app.utils.text_chunker import split_text

settings = get_settings()


class DocumentService:
    def __init__(self, db: Session):
        self.document_repository = DocumentRepository(db)
        self.chunk_repository = DocumentChunkRepository(db)
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

        try:
            extracted_text = extract_text_from_pdf(file_bytes)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"PDF parsing failed. Please upload a valid PDF file. Error: {str(exc)}",
            )

        if not extracted_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No readable text found in PDF",
            )

        chunks = split_text(
            text=extracted_text,
            chunk_size=1000,
        )

        for index, chunk_text in enumerate(chunks):
            self.chunk_repository.create_chunk(
                document_id=document.id,
                chunk_index=index,
                chunk_text=chunk_text,
            )

        return {
            "id": document.id,
            "filename": document.filename,
            "storage_path": document.storage_path,
            "status": document.status,
            "chunks_created": len(chunks),
        }

    def list_documents(self):
        return self.document_repository.get_all_documents()