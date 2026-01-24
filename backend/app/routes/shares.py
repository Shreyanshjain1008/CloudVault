from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import SessionLocal
from app.models.share import Share
from app.schemas.share import ShareCreate
from app.core.deps import get_current_user

router = APIRouter(prefix="/shares", tags=["Sharing"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def share_resource(
    data: ShareCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    share = Share(
        user_id=data.user_id,
        file_id=data.file_id,
        folder_id=data.folder_id,
        role=data.role
    )
    db.add(share)
    db.commit()
    return {"message": "Resource shared successfully"}
