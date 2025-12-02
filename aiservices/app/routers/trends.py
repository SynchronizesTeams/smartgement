from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import (
    RecordSaleRequest, TrendAnalysisResponse, DemandPrediction
)
from app.services import trend_service

router = APIRouter()


@router.post("/record-sale")
def record_sale(sale: RecordSaleRequest, db: Session = Depends(get_db)):
    """Record a product sale for trend tracking"""
    trend = trend_service.record_sale(db, sale)
    return {
        "success": True,
        "message": "Sale recorded successfully",
        "trend_id": trend.id,
        "date": trend.date.isoformat()
    }


@router.get("/analysis/{product_id}", response_model=TrendAnalysisResponse)
def get_trend_analysis(
    product_id: int,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get trend analysis for a product"""
    try:
        return trend_service.analyze_product_trend(db, product_id, days)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/predict/{product_id}", response_model=DemandPrediction)
def predict_demand(product_id: int, db: Session = Depends(get_db)):
    """Get demand prediction for a product"""
    return trend_service.predict_demand(db, product_id)


@router.get("/recommendations/{product_id}")
def get_recommendations(product_id: int, db: Session = Depends(get_db)):
    """Get purchase quantity recommendations"""
    return trend_service.recommend_order_quantity(db, product_id)
