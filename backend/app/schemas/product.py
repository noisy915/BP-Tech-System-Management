"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Pydantic schemas for Product entity.
"""

from typing import Optional, Literal
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.category import CategoryResponse
from app.schemas.supplier import SupplierResponse
from app.schemas.inventory import InventoryResponse


class ProductBase(BaseModel):
    category_id: int
    supplier_id: Optional[int] = None
    product_name: str
    sku: str
    description: Optional[str] = None
    condition: Literal["New", "Used"] = "New"
    selling_price: Decimal = Field(ge=0, decimal_places=2)
    image_url: Optional[str] = None
    product_status: Literal["Active", "Discontinued"] = "Active"


class ProductCreate(ProductBase):
    # Optional initial quantity to seed inventory upon creation
    initial_stock: Optional[int] = Field(default=0, ge=0)
    reorder_level: Optional[int] = Field(default=5, ge=0)


class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    supplier_id: Optional[int] = None
    product_name: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    condition: Optional[Literal["New", "Used"]] = None
    selling_price: Optional[Decimal] = Field(default=None, ge=0, decimal_places=2)
    image_url: Optional[str] = None
    product_status: Optional[Literal["Active", "Discontinued"]] = None


class ProductResponse(ProductBase):
    product_id: int
    category: Optional[CategoryResponse] = None
    supplier: Optional[SupplierResponse] = None

    model_config = ConfigDict(from_attributes=True)


class ProductWithInventoryResponse(ProductResponse):
    inventory: Optional[InventoryResponse] = None

    model_config = ConfigDict(from_attributes=True)
