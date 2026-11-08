"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Pydantic schemas for StockMovement entity.
"""

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, ConfigDict, Field


class StockMovementCreate(BaseModel):
    product_id: int
    movement_type: Literal["IN", "OUT", "ADJUSTMENT"]
    quantity: int = Field(gt=0, description="Quantity must be greater than zero")
    remarks: Optional[str] = None


class StockMovementResponse(BaseModel):
    movement_id: int
    product_id: int
    movement_type: str
    quantity: int
    movement_date: datetime
    remarks: Optional[str] = None
    product_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
