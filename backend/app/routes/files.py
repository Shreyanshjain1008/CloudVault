from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database import get_db
from app.core.deps import get_current_user
from app.models.file import File as FileModel
from app.schemas.file import FileResponse
from app.utils.supabase import (
    upload_file_to_supabase,
    generate_signed_url,
    delete_file_from_supabase,
)

router = APIRouter(prefix="/files", tags=["Files"])


# ---------------- LIST FILES (My Drive) ----------------
@router.get("", response_model=List[FileResponse])
def list_files(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return db.query(FileModel).filter(
        FileModel.owner_id == user.id,
        FileModel.is_deleted == False
    ).order_by(FileModel.created_at.desc()).all()


# ---------------- UPLOAD ----------------
@router.post("/upload", response_model=FileResponse)
def upload_file(
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    storage_path = upload_file_to_supabase(file, str(user.id))

    new_file = FileModel(
        name=file.filename,
        owner_id=user.id,
        mime_type=file.content_type,
        size=file.size or 0,
        storage_path=storage_path,
        is_deleted=False,
        is_starred=False
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return new_file


# ---------------- SEARCH ----------------
@router.get("/search", response_model=List[FileResponse])
def search_files(
    q: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return db.query(FileModel).filter(
        FileModel.owner_id == user.id,
        FileModel.is_deleted == False,
        FileModel.name.ilike(f"%{q}%")
    ).all()


# ---------------- TRASH ----------------
@router.get("/trash", response_model=List[FileResponse])
def list_trash(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return db.query(FileModel).filter(
        FileModel.owner_id == user.id,
        FileModel.is_deleted == True
    ).all()


# ---------------- STAR / UNSTAR ----------------
@router.patch("/{file_id}/star")
def toggle_star(
    file_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_id == user.id
    ).first()

    if not file:
        raise HTTPException(404, "File not found")

    file.is_starred = not file.is_starred
    db.commit()

    return {"starred": file.is_starred}


# ---------------- MOVE TO TRASH ----------------
@router.delete("/{file_id}")
def move_to_trash(
    file_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_id == user.id,
        FileModel.is_deleted == False
    ).first()

    if not file:
        raise HTTPException(404, "File not found")

    file.is_deleted = True
    db.commit()

    return {"message": "Moved to trash"}


# ---------------- RESTORE ----------------
@router.patch("/{file_id}/restore")
def restore_file(
    file_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_id == user.id,
        FileModel.is_deleted == True
    ).first()

    if not file:
        raise HTTPException(404, "File not found in trash")

    file.is_deleted = False
    db.commit()

    return {"message": "Restored"}


# ---------------- PERMANENT DELETE ----------------
@router.delete("/{file_id}/permanent")
def permanent_delete(
    file_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_id == user.id
    ).first()

    if not file:
        raise HTTPException(404, "File not found")

    delete_file_from_supabase(file.storage_path)

    db.delete(file)
    db.commit()

    return {"message": "Permanently deleted"}


# ---------------- VIEW / DOWNLOAD ----------------
@router.get("/{file_id}/view")
def view_file(
    file_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_id == user.id
    ).first()

    if not file:
        raise HTTPException(404, "File not found")

    signed_url = generate_signed_url(file.storage_path)
    return {"url": signed_url}
