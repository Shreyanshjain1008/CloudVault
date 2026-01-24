from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from app.database import Base

class LinkShare(Base):
    __tablename__ = "link_shares"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    token = Column(String, unique=True, index=True)
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id"), nullable=True)
    folder_id = Column(UUID(as_uuid=True), ForeignKey("folders.id"), nullable=True)

    password = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

