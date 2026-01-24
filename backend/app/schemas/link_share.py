from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime

class LinkShareCreate(BaseModel):
    file_id: Optional[UUID] = None
    folder_id: Optional[UUID] = None
    password: Optional[str] = None
    expires_at: Optional[datetime] = None
