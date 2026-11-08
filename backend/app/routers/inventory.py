"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Inventory Router: Monitor stock levels, reorder thresholds, and low-stock alerts.
"""

from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.admin import Admin
from app.schemas.inventory import InventoryUpdate, InventoryResponse
from app.auth_utils import get_current_admin

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])


@router.get("", response_model=List[InventoryResponse])
def get_inventory(
    low_stock_only: bool = Query(False, description="Filter for products at or below reorder level"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Retrieve all inventory records with low-stock calculation (Admin only)."""
    query = db.query(Inventory).options(joinedload(Inventory.product))

    if low_stock_only:
        query = query.filter(Inventory.quantity_available <= Inventory.reorder_level)

    records = query.all()
    for rec in records:
        rec.is_low_stock = rec.quantity_available <= rec.reorder_level
    return records


@router.get("/{product_id}", response_model=InventoryResponse)
def get_product_inventory(product_id: int, db: Session = Depends(get_db)):
    """Retrieve inventory record for a specific product."""
    record = db.query(Inventory).filter(Inventory.product_id == product_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    record.is_low_stock = record.quantity_available <= record.reorder_level
    return record


@router.put("/{inventory_id}", response_model=InventoryResponse)
def update_inventory(
    inventory_id: int,
    payload: InventoryUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Update inventory quantity or reorder level directly (Admin only)."""
    inv = db.query(Inventory).filter(Inventory.inventory_id == inventory_id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory record not found")

    if payload.quantity_available is not None:
        inv.quantity_available = payload.quantity_available
    if payload.reorder_level is not None:
        inv.reorder_level = payload.reorder_level

    inv.last_updated = datetime.now(timezone.utc)
    db.commit()
    db.refresh(inv)
    inv.is_low_stock = inv.quantity_available <= inv.reorder_level
    return inv
