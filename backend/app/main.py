import os
from fastapi import FastAPI
from app.models.database import engine, Base
from app.models import models
from app.api import auth, organizations, events, fonts, templates, participants, generation, certificates
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Certificate Platform API",
    description="PRODUCTION Certificate Generation system",
    version="1.0.0"
)

# Parse CORS_ORIGINS from environment variable, default to localhost for dev
cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:5174,http://localhost:5173")
origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(organizations.router)
app.include_router(events.router)
app.include_router(fonts.router)
app.include_router(templates.router)
app.include_router(participants.router)
app.include_router(generation.router)
app.include_router(certificates.router)

@app.on_event("startup")
def startup_event():
    try:
        import seed
    except Exception:
        pass

@app.get("/")
def read_root():
    return {"message": "Certificate Platform API is running"}