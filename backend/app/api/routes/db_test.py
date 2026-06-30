from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(prefix="/db-test", tags=["Database"])


@router.get("")
def test_database(db: Session = Depends(get_db)):
    result = db.execute(text("select 'supabase_connected' as status"))
    row = result.fetchone()

    return {
        "database": row.status
    }