"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Pydantic schemas for Admin Authentication and Tokens.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AdminLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


class TokenData(BaseModel):
    username: Optional[str] = None


class AdminResponse(BaseModel):
    admin_id: int
    username: str
    email: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
