from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database import SessionLocal
from app.models.file import File as FileModel
from app.schemas.file import FileResponse
from app.core.deps import get_current_user
from app.utils.supabase import (
    upload_file_to_supabase,
    generate_signed_url,
    delete_file_from_supabase,
)

router = APIRouter(prefix="/files", tags=["Files"])


# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- UPLOAD ----------------
@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    path = upload_file_to_supabase(file, user.id)

    new_file = FileModel(
        filename=file.filename,
        storage_path=path,
        owner_id=user.id,
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {"message": "Uploaded successfully", "id": new_file.id}


# ---------------- LIST FILES (My Drive) ----------------
@router.get("", response_model=list[FileResponse])
def list_files(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return db.query(FileModel).filter(
        FileModel.owner_id == user.id,
        FileModel.is_deleted == False
    ).all()


# ---------------- SEARCH ----------------
@router.get("/search", response_model=list[FileResponse])
def search_files(
    q: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return db.query(FileModel).filter(
        FileModel.owner_id == user.id,
        FileModel.is_deleted == False,
        FileModel.filename.ilike(f"%{q}%")
    ).all()


# ---------------- TRASH ----------------
@router.get("/trash", response_model=list[FileResponse])
def list_trash(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return db.query(FileModel).filter(
        FileModel.owner_id == user.id,
        FileModel.is_deleted == True
    ).all()


# ---------------- STAR ----------------
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


# ---------------- DOWNLOAD ----------------
@router.get("/{file_id}/download")
def download_file(
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

    url = generate_signed_url(file.storage_path)
    return {"url": url}
