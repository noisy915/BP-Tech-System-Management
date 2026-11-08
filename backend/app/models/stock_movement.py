"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Entity 5: Stock Movement Model
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class StockMovement(Base):
    __tablename__ = "stock_movements"

    movement_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.product_id", ondelete="CASCADE"), nullable=False)
    movement_type = Column(String(20), nullable=False)  # 'IN', 'OUT', 'ADJUSTMENT'
    quantity = Column(Integer, nullable=False)
    movement_date = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    remarks = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_positive_movement_quantity"),
        CheckConstraint("movement_type IN ('IN', 'OUT', 'ADJUSTMENT')", name="check_valid_movement_type"),
    )

    # Relationships
    product = relationship("Product", back_populates="stock_movements")

    def __repr__(self):
        return f"<StockMovement(id={self.movement_id}, product_id={self.product_id}, type='{self.movement_type}', qty={self.quantity})>"
