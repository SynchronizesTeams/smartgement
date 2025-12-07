from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class TransactionSummaryRequest(BaseModel):
    """Request for transaction summary generation"""
    merchant_id: str
    date_from: Optional[str] = None  # ISO format date string
    date_to: Optional[str] = None
    payment_method: Optional[str] = None
    limit: int = Field(default=100, le=1000)


class TransactionInsight(BaseModel):
    """Individual transaction insight"""
    type: str  # e.g., "peak_hour", "popular_product", "revenue_trend"
    title: str
    description: str
    value: Optional[str] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class TransactionSummaryResponse(BaseModel):
    """AI-generated transaction summary"""
    summary: str  # Natural language summary
    total_transactions: int
    total_revenue: float
    average_transaction: float
    insights: List[TransactionInsight]
    period: str  # Description of the time period analyzed


class TransactionAnalyticsRequest(BaseModel):
    """Request for transaction analytics"""
    merchant_id: str
    query: str  # Natural language query like "show me trends"
