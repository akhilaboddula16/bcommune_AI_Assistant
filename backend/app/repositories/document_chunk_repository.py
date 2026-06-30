from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class DocumentChunkRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_chunk(
        self,
        document_id: int,
        chunk_index: int,
        chunk_text: str,
    ):
        chunk = DocumentChunk(
            document_id=document_id,
            chunk_index=chunk_index,
            chunk_text=chunk_text,
        )

        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)

        return chunk