from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import RiskResponse, HighRiskProductSummary
from app.services import risk_services

router = APIRouter()


@router.post("/assess/{product_id}", response_model=RiskResponse)
def assess_risk(product_id: int, db: Session = Depends(get_db)):
    """Assess risk for a single product"""
    try:
        return risk_services.assess_product_risk(db, product_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/high-risk", response_model=HighRiskProductSummary)
def get_high_risk_products(merchant_id: str, db: Session = Depends(get_db)):
    """Get all high-risk products for a merchant"""
    return risk_services.get_high_risk_products(db, merchant_id)


@router.get("/report/{merchant_id}")
def get_risk_report(merchant_id: str, db: Session = Depends(get_db)):
    """Generate comprehensive risk report"""
    return risk_services.generate_risk_report(db, merchant_id)
