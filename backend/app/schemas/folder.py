from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class FolderCreate(BaseModel):
    name: str
    parent_id: Optional[UUID] = None

class FolderResponse(BaseModel):
    id: UUID
    name: str
    parent_id: Optional[UUID]

    class Config:
        from_attributes = True
