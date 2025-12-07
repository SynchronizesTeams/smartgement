from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER, BIGINT
from datetime import datetime
from app.database import Base


class Product(Base):
    """Product model for storing product information"""
    __tablename__ = "products"
    __table_args__ = {'extend_existing': True}
    
    # Use MySQL specific INTEGER(unsigned=True) to match Go's uint
    id = Column(BIGINT(unsigned=True), primary_key=True, index=True)
    merchant_id = Column(BIGINT(unsigned=True), index=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    stock = Column(Integer, default=0)
    price = Column(Float, default=0.0)
    ingredients = Column(Text)
    expiration_date = Column(DateTime, nullable=True)
    category = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trends = relationship("ProductTrend", back_populates="product", cascade="all, delete-orphan")
    risks = relationship("ProductRisk", back_populates="product", cascade="all, delete-orphan")


class ProductTrend(Base):
    __tablename__ = "product_trends"
    
    id = Column(BIGINT(unsigned=True), primary_key=True, index=True)
    product_id = Column(BIGINT(unsigned=True), ForeignKey("products.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)

    quantity_sold = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    views = Column(Integer, default=0)
    popularity_score = Column(Float, default=0.0)

    meta_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="trends")



class ProductRisk(Base):
    __tablename__ = "product_risks"

    id = Column(BIGINT(unsigned=True), primary_key=True, index=True)
    product_id = Column(BIGINT(unsigned=True), ForeignKey("products.id"), nullable=False)

    risk_type = Column(String(50), nullable=False)
    risk_level = Column(String(20), nullable=False)
    risk_score = Column(Float, default=0.0)
    reason = Column(Text)

    recommendation = Column(Text)
    calculated_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="risks")



class AutomationHistory(Base):
    """History of automation operations for undo functionality"""
    __tablename__ = "automation_history"
    
    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(String(50), index=True, nullable=False)
    
    # Operation details
    operation_type = Column(String(50), nullable=False)
    command = Column(Text)
    affected_product_ids = Column(JSON)
    
    # State before operation (for undo)
    previous_state = Column(JSON)
    
    executed_at = Column(DateTime, default=datetime.utcnow)
    executed_by = Column(String(50), default="chatbot")


class ChatHistory(Base):
    """Chat conversation history"""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    merchant_id = Column(String(50), index=True, nullable=False)
    
    # Message details
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text)
    intent = Column(String(50))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
