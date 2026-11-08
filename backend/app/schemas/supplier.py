"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Pydantic schemas for Supplier entity.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict


class SupplierBase(BaseModel):
    supplier_name: str
    contact_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class SupplierCreate(SupplierBase):
    pass


class SupplierUpdate(BaseModel):
    supplier_name: Optional[str] = None
    contact_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None


class SupplierResponse(SupplierBase):
    supplier_id: int

    model_config = ConfigDict(from_attributes=True)
