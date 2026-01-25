from supabase import create_client
import uuid

from app.core.config import (
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_BUCKET,
)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY
)


def upload_file_to_supabase(file, user_id: str) -> str:
    file_ext = file.filename.split(".")[-1]
    path = f"{user_id}/{uuid.uuid4()}.{file_ext}"

    supabase.storage.from_(SUPABASE_BUCKET).upload(
        path,
        file.file,
        {"content-type": file.content_type},
    )

    return path


def generate_signed_url(path: str) -> str:
    res = supabase.storage.from_(SUPABASE_BUCKET).create_signed_url(
        path,
        3600
    )
    return res["signedURL"]


def delete_file_from_supabase(path: str):
    supabase.storage.from_(SUPABASE_BUCKET).remove([path])
