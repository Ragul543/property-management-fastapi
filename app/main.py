import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import engine, Base
from app.routers import items
from app.routers import properties
from app.routers import enquiries
from app.models.property import Property, PropertyImage  # noqa: F401 - ensure tables are created
from app.models.enquiry import Enquiry  # noqa: F401 - ensure tables are created

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", "properties")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Mount static files for image serving
uploads_root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
app.mount("/uploads", StaticFiles(directory=uploads_root), name="uploads")

app.include_router(items.router, prefix="/api/v1")
app.include_router(properties.router, prefix="/api/v1")
app.include_router(enquiries.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!", "version": settings.version}


@app.get("/health")
def health_check():
    return {"status": "ok", "database": "mariadb @ localhost"}
