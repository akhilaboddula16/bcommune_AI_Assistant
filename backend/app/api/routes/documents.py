from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.document import DocumentResponse
from app.security.rbac import require_roles
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    current_user=Depends(require_roles(["Super Admin", "Admin"])),
    db: Session = Depends(get_db),
):
    return DocumentService(db).upload_pdf(
        file=file,
        uploaded_by=current_user.id,
    )


@router.get("", response_model=list[DocumentResponse])
def list_documents(
    current_user=Depends(require_roles(["Super Admin", "Admin"])),
    db: Session = Depends(get_db),
):
    return DocumentService(db).list_documents()