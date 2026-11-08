"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Pydantic schemas for Category entity.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class CategoryBase(BaseModel):
    category_name: str
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    description: Optional[str] = None


class CategoryResponse(CategoryBase):
    category_id: int

    model_config = ConfigDict(from_attributes=True)
