import os
import logging
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database import Base, engine
from app.routes import auth, folders, files, shares, public_links

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Ensure DB tables exist (use migrations in production)
Base.metadata.create_all(bind=engine)

# Ensure the files.storage_path column exists (safe quick fix if migrations not applied).
# This uses a non-destructive ALTER TABLE IF NOT EXISTS for immediate recovery.
try:
    with engine.begin() as conn:
        logger.info("Ensuring storage_path column exists on files table...")
        # Use driver-level SQL to be compatible with SQLAlchemy versions
        conn.exec_driver_sql(
            "ALTER TABLE files ADD COLUMN IF NOT EXISTS storage_path TEXT;"
        )
        logger.info("storage_path column ensured.")
except Exception as exc:
    # Log but do not crash -- if your DB is in a state where this fails you should inspect logs.
    logger.exception("Error ensuring storage_path column exists: %s", exc)

app = FastAPI(title="CloudVault API")

# Allow list for CORS. You can set FRONTEND_ORIGINS as a comma-separated list in Render env.
# Example: FRONTEND_ORIGINS="https://cloud-vault-psi.vercel.app,https://cloud-vault-weld.vercel.app"
_frontend_env = os.getenv("FRONTEND_ORIGINS", "")
if _frontend_env:
    allowed_origins: List[str] = [o.strip() for o in _frontend_env.split(",") if o.strip()]
else:
    # sensible defaults for local dev + common Vercel preview host(s)
    allowed_origins = [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://cloud-vault-psi.vercel.app",
        "https://cloud-vault-weld.vercel.app",
    ]

logger.info("CORS allowed_origins: %s", allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # use explicit origins; do NOT use ["*"] with credentials=True
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers after middleware is configured
app.include_router(files.router)
app.include_router(auth.router)
app.include_router(folders.router)
app.include_router(shares.router)
app.include_router(public_links.router)


@app.get("/")
def root():
    return {"status": "CloudVault backend running"}