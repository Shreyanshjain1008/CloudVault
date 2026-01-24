from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import uuid4

from app.database import SessionLocal
from app.models.link_share import LinkShare
from app.schemas.link_share import LinkShareCreate

router = APIRouter(prefix="/public-link", tags=["Public Sharing"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_public_link(
    data: LinkShareCreate,
    db: Session = Depends(get_db)
):
    token = str(uuid4())

    link = LinkShare(
        token=token,
        file_id=data.file_id,
        folder_id=data.folder_id,
        password=data.password,
        expires_at=data.expires_at
    )

    db.add(link)
    db.commit()

    return {"public_url": f"/public/{token}"}
