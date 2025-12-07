from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.transaction import (
    TransactionSummaryRequest,
    TransactionSummaryResponse,
    TransactionAnalyticsRequest,
    TransactionInsight
)
from app.services import transaction_summary_service

router = APIRouter()


@router.post("/summary", response_model=TransactionSummaryResponse)
async def get_transaction_summary(
    request: TransactionSummaryRequest,
    db: Session = Depends(get_db)
):
    """Generate AI-powered transaction summary"""
    result = await transaction_summary_service.generate_transaction_summary(
        db=db,
        merchant_id=request.merchant_id,
        date_from=request.date_from,
        date_to=request.date_to,
        payment_method=request.payment_method,
        limit=request.limit
    )
    
    return TransactionSummaryResponse(
        summary=result["summary"],
        total_transactions=result["total_transactions"],
        total_revenue=result["total_revenue"],
        average_transaction=result["average_transaction"],
        insights=[TransactionInsight(**insight) for insight in result["insights"]],
        period=result["period"]
    )


@router.post("/analyze")
async def analyze_transactions(
    request: TransactionAnalyticsRequest,
    db: Session = Depends(get_db)
):
    """Analyze transactions based on natural language query"""
    result = await transaction_summary_service.analyze_transaction_query(
        db=db,
        merchant_id=request.merchant_id,
        query=request.query
    )
    
    return TransactionSummaryResponse(
        summary=result["summary"],
        total_transactions=result["total_transactions"],
        total_revenue=result["total_revenue"],
        average_transaction=result["average_transaction"],
        insights=[TransactionInsight(**insight) for insight in result["insights"]],
        period=result["period"]
    )


@router.get("/insights/{merchant_id}")
async def get_transaction_insights(
    merchant_id: str,
    days: int = Query(default=7, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """Get transaction insights for the past N days"""
    from datetime import datetime, timedelta
    
    today = datetime.now().date()
    date_from = (today - timedelta(days=days)).isoformat()
    date_to = today.isoformat()
    
    result = await transaction_summary_service.generate_transaction_summary(
        db=db,
        merchant_id=merchant_id,
        date_from=date_from,
        date_to=date_to
    )
    
    return TransactionSummaryResponse(
        summary=result["summary"],
        total_transactions=result["total_transactions"],
        total_revenue=result["total_revenue"],
        average_transaction=result["average_transaction"],
        insights=[TransactionInsight(**insight) for insight in result["insights"]],
        period=result["period"]
    )
