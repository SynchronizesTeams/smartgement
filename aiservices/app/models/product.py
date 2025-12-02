from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Product(Base):
    """Product model for storing product information"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    stock = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    ingredients = Column(Text)  # Comma-separated or JSON
    expiration_date = Column(DateTime, nullable=True)
    category = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trends = relationship("ProductTrend", back_populates="product", cascade="all, delete-orphan")
    risks = relationship("ProductRisk", back_populates="product", cascade="all, delete-orphan")


class ProductTrend(Base):
    """Product trend data for demand analysis"""
    __tablename__ = "product_trends"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    
    # Sales metrics
    quantity_sold = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    views = Column(Integer, default=0)
    popularity_score = Column(Float, default=0.0)
    
    # Additional context
    meta_data = Column(JSON, nullable=True)  # For storing extra contextual data
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="trends")


class ProductRisk(Base):
    """Risk assessment records for products"""
    __tablename__ = "product_risks"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Risk information
    risk_type = Column(String, nullable=False)  # e.g., "expiration", "stock", "trend", "financial"
    risk_level = Column(String, nullable=False)  # e.g., "low", "medium", "high", "critical"
    risk_score = Column(Float, default=0.0)  # Numerical score 0-100
    reason = Column(Text)
    
    # Recommendations
    recommendation = Column(Text)
    
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    product = relationship("Product", back_populates="risks")


class AutomationHistory(Base):
    """History of automation operations for undo functionality"""
    __tablename__ = "automation_history"
    
    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(String, index=True, nullable=False)
    
    # Operation details
    operation_type = Column(String, nullable=False)  # e.g., "bulk_update_stock", "bulk_delete"
    command = Column(Text)  # Original command from user
    affected_product_ids = Column(JSON)  # List of product IDs affected
    
    # State before operation (for undo)
    previous_state = Column(JSON)  # Stores previous values
    
    executed_at = Column(DateTime, default=datetime.utcnow)
    executed_by = Column(String, default="chatbot")
