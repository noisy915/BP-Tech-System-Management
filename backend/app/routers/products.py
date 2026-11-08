"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Products Router: Core catalogue and product administration endpoints.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.database import get_db
from app.models.product import Product
from app.models.category import Category
from app.models.inventory import Inventory
from app.models.stock_movement import StockMovement
from app.models.admin import Admin
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductWithInventoryResponse,
)
from app.auth_utils import get_current_admin

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("", response_model=List[ProductWithInventoryResponse])
def get_products(
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    condition: Optional[str] = Query(None, description="Filter by condition: 'New' or 'Used'"),
    status: Optional[str] = Query(None, description="Filter by status: 'Active' or 'Discontinued'"),
    search: Optional[str] = Query(None, description="Search term in name or SKU"),
    include_discontinued: bool = Query(False, description="Whether to include discontinued products"),
    db: Session = Depends(get_db)
):
    """
    Retrieve products with inventory details for catalogue display and admin views.
    Filters by category, condition, status, and search keywords.
    """
    query = db.query(Product).options(
        joinedload(Product.category),
        joinedload(Product.supplier),
        joinedload(Product.inventory)
    )

    if not include_discontinued and not status:
        query = query.filter(Product.product_status == "Active")
    elif status:
        query = query.filter(Product.product_status == status)

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if condition:
        query = query.filter(Product.condition.ilike(condition))

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Product.product_name.ilike(search_pattern),
                Product.sku.ilike(search_pattern),
                Product.description.ilike(search_pattern)
            )
        )

    products = query.order_by(Product.product_id.desc()).all()

    # Annotate inventory with is_low_stock flag
    for p in products:
        if p.inventory:
            p.inventory.is_low_stock = p.inventory.quantity_available <= p.inventory.reorder_level

    return products


@router.get("/{product_id}", response_model=ProductWithInventoryResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieve details for a single product."""
    product = db.query(Product).options(
        joinedload(Product.category),
        joinedload(Product.supplier),
        joinedload(Product.inventory)
    ).filter(Product.product_id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.inventory:
        product.inventory.is_low_stock = product.inventory.quantity_available <= product.inventory.reorder_level

    return product


@router.post("", response_model=ProductWithInventoryResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Create a new product listing (Admin only).
    Automatically creates the associated 1:1 Inventory record as specified in Section 6.
    """
    # Verify category exists
    cat = db.query(Category).filter(Category.category_id == payload.category_id).first()
    if not cat:
        raise HTTPException(status_code=400, detail="Specified category does not exist")

    # Verify SKU uniqueness
    if db.query(Product).filter(Product.sku.ilike(payload.sku)).first():
        raise HTTPException(status_code=400, detail="A product with this SKU already exists")

    product = Product(
        category_id=payload.category_id,
        supplier_id=payload.supplier_id,
        product_name=payload.product_name,
        sku=payload.sku.upper().strip(),
        description=payload.description,
        condition=payload.condition,
        selling_price=payload.selling_price,
        image_url=payload.image_url,
        product_status=payload.product_status,
    )
    db.add(product)
    db.flush()  # Populates product.product_id

    # Automatically create the 1:1 Inventory entity
    inventory = Inventory(
        product_id=product.product_id,
        quantity_available=payload.initial_stock or 0,
        reorder_level=payload.reorder_level or 5,
    )
    db.add(inventory)

    # If initial stock was provided, record an initial stock movement
    if payload.initial_stock and payload.initial_stock > 0:
        movement = StockMovement(
            product_id=product.product_id,
            movement_type="IN",
            quantity=payload.initial_stock,
            remarks="Initial inventory opening stock"
        )
        db.add(movement)

    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductWithInventoryResponse)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """Update product information (Admin only)."""
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = payload.model_dump(exclude_unset=True)

    # Check SKU uniqueness if updated
    if "sku" in update_data:
        existing = db.query(Product).filter(
            Product.sku.ilike(update_data["sku"]),
            Product.product_id != product_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="SKU already taken by another product")
        update_data["sku"] = update_data["sku"].upper().strip()

    for field, val in update_data.items():
        setattr(product, field, val)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def delete_or_discontinue_product(
    product_id: int,
    force: bool = Query(False, description="Set true to hard delete if no movement history exists"),
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Remove or discontinue a product (Admin only).
    Per Section 6 rules: If historical movements exist, product is marked 'Discontinued' to preserve audit logs.
    """
    product = db.query(Product).filter(Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    movements_count = db.query(StockMovement).filter(StockMovement.product_id == product_id).count()

    if movements_count > 0 or not force:
        product.product_status = "Discontinued"
        db.commit()
        return {"message": "Product marked as Discontinued to preserve stock movement history.", "status": "Discontinued"}
    else:
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully.", "status": "Deleted"}
