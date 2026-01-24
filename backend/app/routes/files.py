from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, HTTPException
from fastapi.responses import FileResponse as FastAPIFileResponse
from sqlalchemy.orm import Session
from uuid import UUID
import os
import shutil

from app.database import SessionLocal
from app.models.file import File as FileModel
from app.schemas.file import FileResponse
from app.core.deps import get_current_user

router = APIRouter(prefix="/files", tags=["Files"])


# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- TRASH ----------------
@router.get("/trash", response_model=list[FileResponse])
def list_trash(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(FileModel).filter(
        FileModel.owner_id == user.id,
        FileModel.is_deleted == True
    ).all()
    
# ---------------- UPLOAD ----------------
@router.post("/upload", response_model=FileResponse)
def upload_file(
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    new_file = FileModel(
        name=file.filename,
        owner_id=user.id,
        size=file.size,
        mime_type=file.content_type,
        is_deleted=False,
        is_starred=False
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    # Save the file to disk
    with open(f"app/files/{new_file.id}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return new_file

# ---------------- LIST FILES (My Drive) ----------------
@router.get("", response_model=list[FileResponse])
def list_files(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(FileModel).filter(
        FileModel.owner_id == user.id,
        FileModel.is_deleted == False
    ).all()


# ---------------- SEARCH FILES ----------------
@router.get("/search", response_model=list[FileResponse])
def search_files(
    q: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(FileModel).filter(
        FileModel.owner_id == user.id,
        FileModel.is_deleted == False,
        FileModel.name.ilike(f"%{q}%")
    ).all()


# ---------------- VIEW FILE  ----------------
@router.get("/{file_id}")
def view_file(
    file_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_id == user.id
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file_path = f"app/files/{file.id}"
    if not os.path.exists(file_path):
        # Fallback to old path
        old_path = f"app/uploaded_files/{file.id}"
        if os.path.exists(old_path):
            file_path = old_path
        else:
            raise HTTPException(status_code=404, detail="File not found on disk")

    return FastAPIFileResponse(file_path, media_type=file.mime_type, filename=file.name)



# ---------------- STAR ----------------
@router.patch("/{file_id}/star")
def toggle_star(
    file_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_id == user.id
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file.is_starred = not file.is_starred
    db.commit()
    return {"starred": file.is_starred}


# ---------------- MOVE TO TRASH ----------------
@router.delete("/{file_id}")
def move_to_trash(
    file_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_id == user.id,
        FileModel.is_deleted == False
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    file.is_deleted = True
    db.commit()
    return {"message": "Moved to trash"}


# ---------------- RESTORE ----------------
@router.patch("/{file_id}/restore")
def restore_file(
    file_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_id == user.id,
        FileModel.is_deleted == True
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found in trash")

    file.is_deleted = False
    db.commit()
    return {"message": "Restored"}


# ---------------- PERMANENT DELETE (FIXED) ----------------
@router.delete("/{file_id}/permanent")
def permanent_delete(
    file_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.owner_id == user.id
    ).first()

    if not file:
        raise HTTPException(status_code=404, detail="File not found")

    # Delete the file from disk
    file_path = f"app/files/{file.id}"
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(file)
    db.commit()

    return {"message": "Permanently deleted"}


