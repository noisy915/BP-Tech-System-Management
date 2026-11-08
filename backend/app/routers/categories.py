"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Categories Router: Manage product categories.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.models.admin import Admin
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.auth_utils import get_current_admin

router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.get("", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Retrieve all product categories."""
    return db.query(Category).order_by(Category.category_name).all()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Retrieve a single category by ID."""
    cat = db.query(Category).filter(Category.category_id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Add a new product category (Admin only)."""
    existing = db.query(Category).filter(Category.category_name.ilike(payload.category_name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="A category with this name already exists")
    
    cat = Category(category_name=payload.category_name, description=payload.description)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Update category details (Admin only)."""
    cat = db.query(Category).filter(Category.category_id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if payload.category_name is not None:
        cat.category_name = payload.category_name
    if payload.description is not None:
        cat.description = payload.description

    db.commit()
    db.refresh(cat)
    return cat


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Delete a category if no products are assigned to it (Admin only)."""
    cat = db.query(Category).filter(Category.category_id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    if cat.products:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete category because it has linked products. Reassign or remove products first."
        )
    db.delete(cat)
    db.commit()
    return None
