"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Entity 4: Inventory Model
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"), unique=True, nullable=False)
    quantity_available = Column(Integer, nullable=False, default=0)
    reorder_level = Column(Integer, nullable=False, default=5)
    last_updated = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    __table_args__ = (
        CheckConstraint("quantity_available >= 0", name="check_positive_quantity"),
        CheckConstraint("reorder_level >= 0", name="check_positive_reorder_level"),
    )

    # Relationships
    product = relationship("Product", back_populates="inventory")

    def __repr__(self):
        return f"<Inventory(id={self.inventory_id}, product_id={self.product_id}, qty={self.quantity_available}, reorder={self.reorder_level})>"
