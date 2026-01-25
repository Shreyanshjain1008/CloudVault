"""
Defensive supabase helper. Patches httpx for legacy 'proxy' kwarg (temporary),
validates required env/config, logs responses, and provides robust upload/delete helpers.
"""

import os
import uuid
import logging
import httpx as _httpx
from typing import Optional

logger = logging.getLogger(__name__)

# Temporary shim: drop legacy 'proxy' kwarg if passed
if not getattr(_httpx, "_cv_shim_patched", False):
    _orig_client_init = _httpx.Client.__init__

    def _patched_client_init(self, *args, **kwargs):
        kwargs.pop("proxy", None)
        return _orig_client_init(self, *args, **kwargs)

    _httpx.Client.__init__ = _patched_client_init
    _httpx._cv_shim_patched = True

# Remove proxy env vars only if you are sure you DON'T want system proxies to apply
for v in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
    os.environ.pop(v, None)

# Now import supabase client factory
from supabase import create_client
from app.core.config import (
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_BUCKET,
)
from fastapi import UploadFile

# Validate required config and fail fast with clear message
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in environment/config")
if not SUPABASE_BUCKET:
    raise RuntimeError("SUPABASE_BUCKET must be set in environment/config")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def upload_file_to_supabase(file: UploadFile, user_id: str) -> str:
    """
    Upload a FastAPI UploadFile to Supabase storage and return the storage path.
    This reads file bytes (safe for small/medium files). If you need streaming for
    very large files, adapt to pass file.file but ensure the client accepts a file-like.
    """
    file_ext = file.filename.rsplit(".", 1)[-1] if "." in (file.filename or "") else ""
    path = f"{user_id}/{uuid.uuid4().hex}{('.' + file_ext) if file_ext else ''}"

    # Ensure pointer is at start then read bytes
    try:
        file.file.seek(0)
    except Exception:
        pass

    try:
        content = file.file.read()
        if not content:
            raise ValueError("Uploaded file is empty")

        # Build options consistently (avoid passing None)
        options = {}
        if getattr(file, "content_type", None):
            options["content-type"] = file.content_type

        # Perform upload. Some versions accept bytes directly.
        res = supabase.storage.from_(SUPABASE_BUCKET).upload(path, content, options or None)
        logger.info("Supabase upload response for %s: %s", path, res)

        # Some client versions return {'error':..., 'data':...}
        if isinstance(res, dict):
            # If error field present, raise with details
            err = res.get("error") or (res.get("data") and res["data"].get("error"))
            if err:
                logger.error("Supabase reported error during upload: %s", err)
                raise RuntimeError(f"Supabase upload failed: {err}")

        # Success: return storage path
        return path

    except Exception as exc:
        logger.exception("Exception while uploading file to Supabase: %s", exc)
        # Re-raise a clear error for caller (route should map to HTTP 500)
        raise RuntimeError(f"Supabase upload exception: {exc}") from exc


def generate_signed_url(path: str, expires: int = 3600) -> str:
    try:
        res = supabase.storage.from_(SUPABASE_BUCKET).create_signed_url(path, expires)
        logger.debug("create_signed_url response: %s", res)

        # handle common shapes
        url = None
        if isinstance(res, dict):
            url = res.get("signedURL") or res.get("signed_url")
            if not url and "data" in res and isinstance(res["data"], dict):
                url = res["data"].get("signedURL") or res["data"].get("signed_url")

        if not url:
            raise RuntimeError(f"Unexpected create_signed_url response: {res}")

        return url
    except Exception as exc:
        logger.exception("Failed to create signed URL for %s: %s", path, exc)
        raise


def delete_file_from_supabase(path: str) -> None:
    try:
        res = supabase.storage.from_(SUPABASE_BUCKET).remove([path])
        logger.info("delete response for %s: %s", path, res)
        if isinstance(res, dict) and res.get("error"):
            raise RuntimeError(f"Supabase delete failed: {res['error']}")
    except Exception:
        logger.exception("Failed to delete %s from supabase", path)
        raise