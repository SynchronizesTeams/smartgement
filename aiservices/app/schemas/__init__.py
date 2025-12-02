# Import all schemas for easy access
from app.schemas.product import (
    ProductBase, ProductCreate, ProductUpdate, ProductResponse,
    TrendDataPoint, RecordSaleRequest, TrendAnalysisResponse, DemandPrediction,
    RiskAssessment, RiskResponse, HighRiskProductSummary,
    ChatMessage, ChatResponse,
    AutomationPreview, AutomationExecuteRequest, AutomationResult, UndoRequest,
    SemanticSearchRequest, SemanticSearchResponse
)

__all__ = [
    "ProductBase", "ProductCreate", "ProductUpdate", "ProductResponse",
    "TrendDataPoint", "RecordSaleRequest", "TrendAnalysisResponse", "DemandPrediction",
    "RiskAssessment", "RiskResponse", "HighRiskProductSummary",
    "ChatMessage", "ChatResponse",
    "AutomationPreview", "AutomationExecuteRequest", "AutomationResult", "UndoRequest",
    "SemanticSearchRequest", "SemanticSearchResponse"
]
