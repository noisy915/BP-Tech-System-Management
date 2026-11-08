"""
BP Tech Inventory Management System
[MEMBER 1: Backend and Database Developer]
Entity 1: Category Model
"""

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_name = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)

    # Relationships
    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category(id={self.category_id}, name='{self.category_name}')>"
