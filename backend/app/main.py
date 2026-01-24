from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, folders, files, shares, public_links
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CloudVault API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://cloud-vault-weld.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files.router)
app.include_router(auth.router)
app.include_router(folders.router)
app.include_router(files.router)
app.include_router(shares.router)
app.include_router(public_links.router)

@app.get("/")
def root():
    return {"status": "CloudVault backend running"}

