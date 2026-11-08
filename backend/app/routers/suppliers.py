"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Suppliers Router: Manage component suppliers.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.supplier import Supplier
from app.models.admin import Admin
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from app.auth_utils import get_current_admin

router = APIRouter(prefix="/api/suppliers", tags=["Suppliers"])


@router.get("", response_model=List[SupplierResponse])
def get_suppliers(
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Retrieve all suppliers (Admin only)."""
    return db.query(Supplier).order_by(Supplier.supplier_name).all()


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Retrieve a supplier by ID (Admin only)."""
    sup = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not sup:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return sup


@router.post("", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    payload: SupplierCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Create a new supplier (Admin only)."""
    sup = Supplier(
        supplier_name=payload.supplier_name,
        contact_number=payload.contact_number,
        email=payload.email,
        address=payload.address
    )
    db.add(sup)
    db.commit()
    db.refresh(sup)
    return sup


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    payload: SupplierUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Update supplier information (Admin only)."""
    sup = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not sup:
        raise HTTPException(status_code=404, detail="Supplier not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(sup, field, value)

    db.commit()
    db.refresh(sup)
    return sup


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Delete a supplier (Admin only)."""
    sup = db.query(Supplier).filter(Supplier.supplier_id == supplier_id).first()
    if not sup:
        raise HTTPException(status_code=404, detail="Supplier not found")
    db.delete(sup)
    db.commit()
    return None
