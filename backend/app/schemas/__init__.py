"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Pydantic Schemas exports.
"""

from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.schemas.supplier import SupplierCreate, SupplierUpdate, SupplierResponse
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductWithInventoryResponse
from app.schemas.inventory import InventoryUpdate, InventoryResponse
from app.schemas.stock_movement import StockMovementCreate, StockMovementResponse
from app.schemas.auth import Token, AdminLogin, AdminResponse

__all__ = [
    "CategoryCreate", "CategoryUpdate", "CategoryResponse",
    "SupplierCreate", "SupplierUpdate", "SupplierResponse",
    "ProductCreate", "ProductUpdate", "ProductResponse", "ProductWithInventoryResponse",
    "InventoryUpdate", "InventoryResponse",
    "StockMovementCreate", "StockMovementResponse",
    "Token", "AdminLogin", "AdminResponse",
]
