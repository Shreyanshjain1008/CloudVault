from sqlalchemy import Column, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database import Base

class Share(Base):
    __tablename__ = "shares"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"), nullable=True)
    folder_id = Column(UUID(as_uuid=True), ForeignKey("folders.id"), nullable=True)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    role = Column(Enum("owner", "editor", "viewer", name="share_role"))

    created_at = Column(DateTime, default=datetime.utcnow)
