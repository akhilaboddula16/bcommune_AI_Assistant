from sqlalchemy.orm import Session

from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.services.embedding_service import EmbeddingService


class SearchService:
    def __init__(self, db: Session):
        self.chunk_repo = DocumentChunkRepository(db)
        self.embedding_service = EmbeddingService()

    def search(self, question: str):
        embedding = self.embedding_service.generate_embedding(question)

        results = self.chunk_repo.search_similar_chunks(
            embedding=embedding,
            limit=5,
        )

        if not results:
            return {
                "answer": "I'm designed to answer only Bcommune company-related questions. I don't have information about that topic.",
                "chunks": [],
            }

        best_distance = results[0]["distance"]

        if best_distance > 0.65:
            return {
                "answer": "I'm designed to answer only Bcommune company-related questions. I don't have information about that topic.",
                "chunks": [],
            }

        return {
            "answer": "Relevant company information found.",
            "chunks": results,
        }