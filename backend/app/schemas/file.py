from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class FileCreate(BaseModel):
    name: str
    folder_id: Optional[UUID] = None
    mime_type: Optional[str] = None
    size: Optional[str] = None

class FileResponse(BaseModel):
    id: UUID
    name: str
    folder_id: Optional[UUID]
    is_starred: bool

    class Config:
        from_attributes = True
