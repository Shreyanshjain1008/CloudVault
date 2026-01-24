from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import SessionLocal
from app.models.folder import Folder
from app.schemas.folder import FolderCreate, FolderResponse
from app.core.deps import get_current_user

router = APIRouter(prefix="/folders", tags=["Folders"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=FolderResponse)
def create_folder(
    data: FolderCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    folder = Folder(
        name=data.name,
        parent_id=data.parent_id,
        owner_id=user.id
    )
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder

@router.get("/{folder_id}", response_model=list[FolderResponse])
def list_subfolders(
    folder_id: UUID,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(Folder).filter(
        Folder.parent_id == folder_id,
        Folder.owner_id == user.id
    ).all()

@router.get("/search")
def search_folders(
    q: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(Folder).filter(
        Folder.owner_id == user.id,
        Folder.name.ilike(f"%{q}%")
    ).all()
