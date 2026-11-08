"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Entity 3: Product Model
"""

from sqlalchemy import Column, Integer, String, Text, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("categories.category_id", ondelete="RESTRICT"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id", ondelete="SET NULL"), nullable=True)
    product_name = Column(String(150), nullable=False, index=True)
    sku = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    condition = Column(String(20), nullable=False, default="New")  # 'New' or 'Used'
    selling_price = Column(Numeric(10, 2), nullable=False)
    image_url = Column(Text, nullable=True)
    product_status = Column(String(20), nullable=False, default="Active")  # 'Active' or 'Discontinued'

    __table_args__ = (
        CheckConstraint("selling_price >= 0", name="check_positive_price"),
        CheckConstraint("condition IN ('New', 'Used')", name="check_valid_condition"),
        CheckConstraint("product_status IN ('Active', 'Discontinued')", name="check_valid_status"),
    )

    # Relationships
    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    inventory = relationship("Inventory", back_populates="product", uselist=False, cascade="all, delete-orphan")
    stock_movements = relationship("StockMovement", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product(id={self.product_id}, name='{self.product_name}', condition='{self.condition}', price={self.selling_price})>"
