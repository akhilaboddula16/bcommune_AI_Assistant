from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.security.auth_dependencies import get_current_user
from app.services.search_service import SearchService

router = APIRouter(
    prefix="/search",
    tags=["Semantic Search"],
)


class SearchRequest(BaseModel):
    question: str


@router.post("")
def semantic_search(
    request: SearchRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return SearchService(db).search(request.question)