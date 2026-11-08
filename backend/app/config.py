"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Configuration and environment variable management.
"""

import os
from dotenv import load_dotenv

# Load .env file from backend directory if present
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bp_tech.db")
SECRET_KEY = os.getenv("SECRET_KEY", "bp_tech_secret_key_change_in_production_2026")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))

DEFAULT_ADMIN_USERNAME = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
DEFAULT_ADMIN_PASSWORD = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")
DEFAULT_ADMIN_EMAIL = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@bptech.com")

WHATSAPP_PHONE_NUMBER = os.getenv("WHATSAPP_PHONE_NUMBER", "60123456789")

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:5500,http://127.0.0.1:5500,http://localhost:8000,http://127.0.0.1:8000"
    ).split(",")
    if origin.strip()
]
