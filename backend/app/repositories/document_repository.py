from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_document(
        self,
        filename: str,
        storage_path: str,
        uploaded_by: int,
    ) -> Document:
        document = Document(
            filename=filename,
            storage_path=storage_path,
            uploaded_by=uploaded_by,
            status="uploaded",
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document

    def get_all_documents(self):
        return (
            self.db.query(Document)
            .order_by(Document.created_at.desc())
            .all()
        )