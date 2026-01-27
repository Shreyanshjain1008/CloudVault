from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, HTTPException, Request
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
import logging

from app.database import get_db
from app.core.deps import get_current_user
from app.models.file import File as FileModel
from app.utils.supabase import (
    upload_file_to_supabase,
    generate_signed_url,
    delete_file_from_supabase,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/files", tags=["Files"])


def file_to_dict(f: FileModel) -> dict:
    """Convert SQLAlchemy File model to JSON-serializable dict, including signed URL when possible."""
    url = None
    if getattr(f, "storage_path", None):
        try:
            url = generate_signed_url(f.storage_path)
        except Exception:
            # Log but do not fail the whole request if signed URL creation fails
            logger.exception("Failed to create signed URL for %s", f.storage_path)

    return {
        "id": str(f.id),
        "name": f.name,
        "mime_type": f.mime_type,
        "size": f.size,
        "owner_id": str(f.owner_id) if f.owner_id else None,
        "folder_id": str(f.folder_id) if f.folder_id else None,
        "storage_path": f.storage_path,
        "url": url,
        "is_starred": bool(f.is_starred),
        "is_deleted": bool(f.is_deleted),
        "created_at": f.created_at.isoformat() if f.created_at else None,
        "updated_at": f.updated_at.isoformat() if f.updated_at else None,
    }


# ---------------- LIST FILES (My Drive) ----------------
@router.get("")
def list_files(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    files = (
        db.query(FileModel)
        .filter(FileModel.owner_id == user.id, FileModel.is_deleted == False)
        .order_by(FileModel.created_at.desc())
        .all()
    )
    return [file_to_dict(f) for f in files]


# ---------------- UPLOAD ----------------
@router.post("/upload")
def upload_file(
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    # Upload file to Supabase storage (returns storage_path)
    storage_path = upload_file_to_supabase(file, str(user.id))

    new_file = FileModel(
        name=file.filename,
        owner_id=user.id,
        mime_type=file.content_type,
        size=getattr(file, "size", None) or 0,
        storage_path=storage_path,
        is_deleted=False,
        is_starred=False,
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    # Return file metadata + signed URL for frontend to fetch
    return file_to_dict(new_file)


# ---------------- SEARCH ----------------
@router.get("/search")
def search_files(
    q: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    files = (
        db.query(FileModel)
        .filter(
            FileModel.owner_id == user.id,
            FileModel.is_deleted == False,
            FileModel.name.ilike(f"%{q}%"),
        )
        .all()
    )
    return [file_to_dict(f) for f in files]


# ---------------- TRASH ----------------
@router.get("/trash")
def list_trash(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    files = (
        db.query(FileModel)
        .filter(FileModel.owner_id == user.id, FileModel.is_deleted == True)
        .all()
    )
    return [file_to_dict(f) for f in files]


# ---------------- STAR / UNSTAR ----------------
@router.patch("/{file_id}/star")
def toggle_star(
    file_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    file = (
        db.query(FileModel)
        .filter(FileModel.id == file_id, FileModel.owner_id == user.id)
        .first()
    )

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
    file = (
        db.query(FileModel)
        .filter(
            FileModel.id == file_id,
            FileModel.owner_id == user.id,
            FileModel.is_deleted == False,
        )
        .first()
    )

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
    file = (
        db.query(FileModel)
        .filter(
            FileModel.id == file_id,
            FileModel.owner_id == user.id,
            FileModel.is_deleted == True,
        )
        .first()
    )

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
    file = (
        db.query(FileModel)
        .filter(FileModel.id == file_id, FileModel.owner_id == user.id)
        .first()
    )

    if not file:
        raise HTTPException(404, "File not found")

    # delete from supabase then DB row
    try:
        delete_file_from_supabase(file.storage_path)
    except Exception:
        logger.exception("Failed to delete from supabase: %s", file.storage_path)
        raise HTTPException(500, "Failed to delete file from storage")

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
    file = (
        db.query(FileModel)
        .filter(FileModel.id == file_id, FileModel.owner_id == user.id)
        .first()
    )

    if not file:
        raise HTTPException(404, "File not found")

    signed_url = generate_signed_url(file.storage_path)
    return {"url": signed_url}