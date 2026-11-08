"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Pydantic schemas for Inventory entity.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class InventoryBase(BaseModel):
    quantity_available: int = Field(default=0, ge=0)
    reorder_level: int = Field(default=5, ge=0)


class InventoryUpdate(BaseModel):
    quantity_available: Optional[int] = Field(default=None, ge=0)
    reorder_level: Optional[int] = Field(default=None, ge=0)


class InventoryResponse(InventoryBase):
    inventory_id: int
    product_id: int
    last_updated: datetime
    is_low_stock: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
