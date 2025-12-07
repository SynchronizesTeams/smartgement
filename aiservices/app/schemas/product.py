from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date


# ===== Product Schemas =====

class ProductBase(BaseModel):
    """Base product schema"""
    name: str
    description: Optional[str] = None
    stock: int = 0
    price: float = 0.0
    ingredients: Optional[str] = None
    expiration_date: Optional[datetime] = None
    category: Optional[str] = None


class ProductCreate(ProductBase):
    """Schema for creating a product"""
    merchant_id: str


class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    name: Optional[str] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    price: Optional[float] = None
    ingredients: Optional[str] = None
    expiration_date: Optional[datetime] = None
    category: Optional[str] = None


class ProductResponse(ProductBase):
    """Schema for product response"""
    id: int
    merchant_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ===== Trend Schemas =====

class TrendDataPoint(BaseModel):
    """Single data point for trend"""
    date: date
    quantity_sold: int
    revenue: float
    popularity_score: float


class RecordSaleRequest(BaseModel):
    """Request to record a sale"""
    product_id: int
    merchant_id: str
    quantity: int
    date: Optional[date] = None


class TrendAnalysisResponse(BaseModel):
    """Response with trend analysis"""
    product_id: int
    product_name: str
    analysis_period_days: int
    average_daily_sales: float
    peak_dates: List[date]
    trend_direction: str  # "increasing", "stable", "decreasing"
    seasonality_detected: bool
    data_points: List[TrendDataPoint]


class DemandPrediction(BaseModel):
    """Demand prediction response"""
    product_id: int
    predicted_demand_next_7_days: float
    predicted_demand_next_30_days: float
    confidence_level: str  # "low", "medium", "high"
    recommendation: str


# ===== Risk Schemas =====

class RiskAssessment(BaseModel):
    """Risk assessment for a product"""
    risk_type: str
    risk_level: str
    risk_score: float
    reason: str
    recommendation: str


class RiskResponse(BaseModel):
    """Complete risk response for a product"""
    product_id: int
    product_name: str
    overall_risk_level: str
    overall_risk_score: float
    risks: List[RiskAssessment]
    assessed_at: datetime


class HighRiskProductSummary(BaseModel):
    """Summary of high-risk products"""
    total_high_risk: int
    total_critical_risk: int
    products: List[ProductResponse]


# ===== Chatbot Schemas =====

class ChatMessage(BaseModel):
    """Chat message from user"""
    merchant_id: str
    message: str
    conversation_history: Optional[List[dict]] = None  # Last N messages for context
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    """Chat response from bot"""
    response: str
    intent: str  # "query", "automation", "report", "help"
    confidence: float
    suggested_actions: Optional[List[str]] = None
    context: Optional[dict] = None


# ===== Automation Schemas =====

class AutomationPreview(BaseModel):
    """Preview of automation impact"""
    operation_type: str
    description: str
    affected_products: List[ProductResponse]
    affected_count: int
    estimated_impact: str
    requires_confirmation: bool


class AutomationExecuteRequest(BaseModel):
    """Request to execute automation"""
    merchant_id: str
    command: str
    confirmed: bool = False


class AutomationResult(BaseModel):
    """Result of automation execution"""
    success: bool
    operation_type: str
    affected_count: int
    affected_product_ids: List[int]
    message: str
    can_undo: bool
    operation_id: Optional[int] = None


class UndoRequest(BaseModel):
    """Request to undo an operation"""
    merchant_id: str
    operation_id: Optional[int] = None  # If None, undo last operation


# ===== Search Schemas =====

class SemanticSearchRequest(BaseModel):
    """Request for semantic product search"""
    merchant_id: str
    query: str
    limit: int = 10


class SemanticSearchResponse(BaseModel):
    """Response from semantic search"""
    query: str
    results: List[ProductResponse]
    scores: List[float]
