"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Entity 2: Supplier Model
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    supplier_name = Column(String(150), nullable=False, index=True)
    contact_number = Column(String(20), nullable=True)
    email = Column(String(150), nullable=True)
    address = Column(Text, nullable=True)

    # Relationships
    products = relationship("Product", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier(id={self.supplier_id}, name='{self.supplier_name}')>"
