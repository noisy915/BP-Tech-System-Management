"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
FastAPI Application Entry Point.
Provides REST API endpoints, CORS handling, auto-migration, and static frontend serving.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import CORS_ORIGINS
from app.database import Base, engine, SessionLocal
from app.models import Admin, Category, Supplier, Product, Inventory, StockMovement
from app.auth_utils import get_password_hash
from app.config import DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD, DEFAULT_ADMIN_EMAIL
from app.routers import (
    auth_router,
    categories_router,
    suppliers_router,
    products_router,
    inventory_router,
    stock_movements_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: run table creation and default admin verification on startup."""
    # Create tables automatically
    Base.metadata.create_all(bind=engine)

    # Ensure default admin exists
    db = SessionLocal()
    try:
        admin = db.query(Admin).filter(Admin.username == DEFAULT_ADMIN_USERNAME).first()
        if not admin:
            admin = Admin(
                username=DEFAULT_ADMIN_USERNAME,
                hashed_password=get_password_hash(DEFAULT_ADMIN_PASSWORD),
                email=DEFAULT_ADMIN_EMAIL,
            )
            db.add(admin)
            db.commit()
    finally:
        db.close()

    yield


app = FastAPI(
    title="BP Tech Inventory Management & Catalogue API",
    description="REST API for BP Tech computer shop inventory management and online catalogue.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Comprehensive CORS configuration supporting all dev hosts, ports, and file:// protocols
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5000",
        "http://localhost:5500",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5000",
        "http://127.0.0.1:5500",
        "http://127.0.0.1:8000",
        "null",
    ],
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1)(:[0-9]+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(suppliers_router)
app.include_router(products_router)
app.include_router(inventory_router)
app.include_router(stock_movements_router)


@app.get("/api/health", tags=["Health"])
def health_check():
    """Health check endpoint to verify backend status."""
    return {"status": "healthy", "service": "BP Tech Inventory API", "version": "1.0.0"}


# Mount frontend static directory if exists (enables single-port fullstack testing)
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/app", StaticFiles(directory=frontend_path, html=True), name="frontend")
