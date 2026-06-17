import uuid
from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Boolean, Numeric, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.database import Base

EMBEDDING_DIM = 1024

class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    cuisine_type = Column(String)
    description = Column(String)
    floor_number = Column(String)
    opening_time = Column(String)
    closing_time = Column(String)
    is_open = Column(Boolean, default=False)
    rating = Column(Numeric(3, 1))
    image_url = Column(String)
    min_order_amount = Column(Numeric(10, 2))
    estimated_delivery_minutes = Column(Integer)

class MenuCategory(Base):
    __tablename__ = "menu_categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=False)
    name = Column(String, nullable=False)
    display_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

class MenuItem(Base):
    __tablename__ = "menu_items"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = Column(UUID(as_uuid=True), ForeignKey("menu_categories.id"), nullable=False)
    restaurant_id = Column(UUID(as_uuid=True), ForeignKey("restaurants.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True)
    is_vegetarian = Column(Boolean, default=False)
    image_url = Column(String)
    prep_time_minutes = Column(Integer)
    embedding = Column(Vector(EMBEDDING_DIM), nullable=True)
