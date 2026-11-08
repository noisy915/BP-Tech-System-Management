"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
API Routers exports.
"""

from app.routers.auth import router as auth_router
from app.routers.categories import router as categories_router
from app.routers.suppliers import router as suppliers_router
from app.routers.products import router as products_router
from app.routers.inventory import router as inventory_router
from app.routers.stock_movements import router as stock_movements_router

__all__ = [
    "auth_router",
    "categories_router",
    "suppliers_router",
    "products_router",
    "inventory_router",
    "stock_movements_router",
]
