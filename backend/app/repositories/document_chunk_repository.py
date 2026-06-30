from sqlalchemy import text
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
        embedding=None,
    ):
        chunk = DocumentChunk(
            document_id=document_id,
            chunk_index=chunk_index,
            chunk_text=chunk_text,
            embedding=embedding,
        )

        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)

        return chunk

    def search_similar_chunks(
        self,
        embedding: list[float],
        limit: int = 5,
    ):
        sql = text("""
            SELECT
                id,
                document_id,
                chunk_text,
                embedding <=> CAST(:embedding AS vector) AS distance
            FROM document_chunks
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)

        result = self.db.execute(
            sql,
            {
                "embedding": str(embedding),
                "limit": limit,
            },
        )

        return result.mappings().all()