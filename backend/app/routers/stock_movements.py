"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Stock Movements Router: Audit trail and inventory transaction updates.
"""

from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.stock_movement import StockMovement
from app.models.inventory import Inventory
from app.models.product import Product
from app.models.admin import Admin
from app.schemas.stock_movement import StockMovementCreate, StockMovementResponse
from app.auth_utils import get_current_admin

router = APIRouter(prefix="/api/stock-movements", tags=["Stock Movements"])


@router.get("", response_model=List[StockMovementResponse])
def get_stock_movements(
    product_id: Optional[int] = Query(None, description="Filter history by product ID"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Retrieve stock movement transaction audit log (Admin only)."""
    query = db.query(StockMovement).options(joinedload(StockMovement.product))

    if product_id:
        query = query.filter(StockMovement.product_id == product_id)

    movements = query.order_by(StockMovement.movement_date.desc(), StockMovement.movement_id.desc()).limit(limit).all()

    # Populate product_name for response convenience
    result = []
    for m in movements:
        resp = StockMovementResponse.model_validate(m)
        resp.product_name = m.product.product_name if m.product else None
        result.append(resp)
    return result


@router.post("", response_model=StockMovementResponse, status_code=status.HTTP_201_CREATED)
def record_stock_movement(
    payload: StockMovementCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Record a stock movement transaction and synchronize inventory quantities.
    - IN: Adds quantity to inventory.
    - OUT: Subtracts quantity from inventory (fails if stock is insufficient).
    - ADJUSTMENT: Sets or adjusts stock with audit remark.
    """
    product = db.query(Product).filter(Product.product_id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    inventory = db.query(Inventory).filter(Inventory.product_id == payload.product_id).first()
    if not inventory:
        inventory = Inventory(product_id=product.product_id, quantity_available=0, reorder_level=5)
        db.add(inventory)
        db.flush()

    if payload.movement_type == "IN":
        inventory.quantity_available += payload.quantity
    elif payload.movement_type == "OUT":
        if inventory.quantity_available < payload.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock. Available: {inventory.quantity_available}, Requested: {payload.quantity}"
            )
        inventory.quantity_available -= payload.quantity
    elif payload.movement_type == "ADJUSTMENT":
        # Adjustment quantity replaces or aligns physical stock
        inventory.quantity_available = payload.quantity

    inventory.last_updated = datetime.now(timezone.utc)

    movement = StockMovement(
        product_id=payload.product_id,
        movement_type=payload.movement_type,
        quantity=payload.quantity,
        remarks=payload.remarks
    )
    db.add(movement)
    db.commit()
    db.refresh(movement)

    resp = StockMovementResponse.model_validate(movement)
    resp.product_name = product.product_name
    return resp
