from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class ShareCreate(BaseModel):
    user_id: UUID
    file_id: Optional[UUID] = None
    folder_id: Optional[UUID] = None
    role: str
