import os
import uuid
import httpx as _httpx

# Patch httpx.Client.__init__ to silently drop the legacy 'proxy' kwarg.
if not getattr(_httpx, "_cv_shim_patched", False):
    _orig_client_init = _httpx.Client.__init__

    def _patched_client_init(self, *args, **kwargs):
        kwargs.pop("proxy", None)  # silently drop it (Option A)
        return _orig_client_init(self, *args, **kwargs)

    _httpx.Client.__init__ = _patched_client_init
    _httpx._cv_shim_patched = True

# Optionally remove proxy environment variables so no upstream lib picks them up.
# Keep this only if you are sure your environment should not use HTTP(S) proxies.
for v in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
    os.environ.pop(v, None)

# Now import and create the supabase client
from supabase import create_client
from app.core.config import (
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_BUCKET,
)
from fastapi import UploadFile  # for type hinting (optional)
import logging

logger = logging.getLogger(__name__)

# Fail fast with a clear message if credentials are missing
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment/config")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def upload_file_to_supabase(file: UploadFile, user_id: str) -> str:
    """
    Uploads an UploadFile (FastAPI) to Supabase storage and returns the storage path.
    """
    file_ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else ""
    path = f"{user_id}/{uuid.uuid4().hex}{('.' + file_ext) if file_ext else ''}"

    # Ensure file pointer is at start
    try:
        file.file.seek(0)
    except Exception:
        pass

    # Upload; passing the file.file (file-like) lets the client stream
    res = supabase.storage.from_(SUPABASE_BUCKET).upload(
        path,
        file.file,
        {"content-type": file.content_type} if file.content_type else None,
    )

    # Check for common response shapes across supabase versions
    # The library may return dicts such as {'error': ..., 'data': ...} or raise exceptions
    if isinstance(res, dict) and res.get("error"):
        logger.error("Supabase upload error: %s", res["error"])
        raise RuntimeError(f"Supabase upload failed: {res['error']}")

    return path


def generate_signed_url(path: str, expires: int = 3600) -> str:
    """
    Returns a signed URL for `path`. Raises on failure.
    """
    res = supabase.storage.from_(SUPABASE_BUCKET).create_signed_url(path, expires)

    # Different versions may return 'signedURL' or 'signed_url', or wrap inside 'data'
    url = None
    if isinstance(res, dict):
        url = res.get("signedURL") or res.get("signed_url")
        if not url and "data" in res and isinstance(res["data"], dict):
            url = res["data"].get("signedURL") or res["data"].get("signed_url")

    if not url:
        logger.error("Failed to create signed URL: %s", res)
        raise RuntimeError(f"Failed to create signed URL for {path}: {res}")

    return url


def delete_file_from_supabase(path: str) -> None:
    """
    Remove file at `path` from the SUPABASE_BUCKET. Raises on failure.
    """
    res = supabase.storage.from_(SUPABASE_BUCKET).remove([path])

    # Check for errors in response
    if isinstance(res, dict) and res.get("error"):
        logger.error("Supabase delete error: %s", res["error"])
        raise RuntimeError(f"Supabase delete failed: {res['error']}")