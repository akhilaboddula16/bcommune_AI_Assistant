from datetime import datetime
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    storage_path: str
    status: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True