"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Authentication Router: Administrator login and profile.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Union

from app.database import get_db
from app.models.admin import Admin
from app.schemas.auth import Token, AdminLogin, AdminResponse
from app.auth_utils import verify_password, create_access_token, get_current_admin

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
def login_for_access_token(
    login_data: AdminLogin,
    db: Session = Depends(get_db)
):
    """Admin login endpoint using JSON body."""
    admin = db.query(Admin).filter(Admin.username == login_data.username).first()
    if not admin or not verify_password(login_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": admin.username})
    return {"access_token": token, "token_type": "bearer", "username": admin.username}


@router.post("/token", response_model=Token, include_in_schema=False)
def login_form_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 password form endpoint for Swagger UI test integration."""
    admin = db.query(Admin).filter(Admin.username == form_data.username).first()
    if not admin or not verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(data={"sub": admin.username})
    return {"access_token": token, "token_type": "bearer", "username": admin.username}


@router.get("/me", response_model=AdminResponse)
def read_current_admin(current_admin: Admin = Depends(get_current_admin)):
    """Retrieve logged-in administrator information."""
    return current_admin
