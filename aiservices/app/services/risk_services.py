from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.models.product import Product, ProductRisk
from app.schemas.product import RiskAssessment, RiskResponse, HighRiskProductSummary, ProductResponse
from app.services.trend_service import analyze_product_trend


def assess_product_risk(db: Session, product_id: int) -> RiskResponse:
    """Comprehensive risk assessment for a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ValueError("Product not found")
    
    risks = []
    risk_scores = []
    
    # 1. Expiration Risk
    if product.expiration_date:
        days_until_expiration = (product.expiration_date - datetime.utcnow()).days
        
        if days_until_expiration < 0:
            risks.append(RiskAssessment(
                risk_type="expiration",
                risk_level="critical",
                risk_score=100.0,
                reason=f"Product expired {abs(days_until_expiration)} days ago",
                recommendation="Remove from inventory immediately. Do not sell."
            ))
            risk_scores.append(100.0)
        elif days_until_expiration <= 3:
            risks.append(RiskAssessment(
                risk_type="expiration",
                risk_level="high",
                risk_score=80.0,
                reason=f"Product expires in {days_until_expiration} days",
                recommendation="Urgent: Run clearance sale or donation. Use for in-house production if applicable."
            ))
            risk_scores.append(80.0)
        elif days_until_expiration <= 7:
            risks.append(RiskAssessment(
                risk_type="expiration",
                risk_level="medium",
                risk_score=50.0,
                reason=f"Product expires in {days_until_expiration} days",
                recommendation="Offer discounts or promotions to move inventory quickly."
            ))
            risk_scores.append(50.0)
        elif days_until_expiration <= 14:
            risks.append(RiskAssessment(
                risk_type="expiration",
                risk_level="low",
                risk_score=25.0,
                reason=f"Product expires in {days_until_expiration} days",
                recommendation="Monitor closely. Plan promotions if stock is high."
            ))
            risk_scores.append(25.0)
    
    # 2. Stock Risk (based on demand)
    try:
        trend_analysis = analyze_product_trend(db, product_id, days=30)
        avg_daily_sales = trend_analysis.average_daily_sales
        
        if avg_daily_sales > 0:
            days_of_stock = product.stock / avg_daily_sales
            
            if days_of_stock < 3:
                risks.append(RiskAssessment(
                    risk_type="stock",
                    risk_level="high",
                    risk_score=75.0,
                    reason=f"Only {days_of_stock:.1f} days of stock remaining based on demand",
                    recommendation=f"Reorder immediately. Stock will run out in {days_of_stock:.0f} days at current sales rate."
                ))
                risk_scores.append(75.0)
            elif days_of_stock < 7:
                risks.append(RiskAssessment(
                    risk_type="stock",
                    risk_level="medium",
                    risk_score=45.0,
                    reason=f"{days_of_stock:.1f} days of stock remaining",
                    recommendation="Plan reorder soon to avoid stockout."
                ))
                risk_scores.append(45.0)
        elif trend_analysis.trend_direction != "no_data" and product.stock == 0:
            risks.append(RiskAssessment(
                risk_type="stock",
                risk_level="critical",
                risk_score=90.0,
                reason="Product is out of stock with historical demand",
                recommendation="Restock immediately. Customers are looking for this product."
            ))
            risk_scores.append(90.0)
    except Exception:
        pass  # No trend data available
    
    # 3. Trend Risk (declining popularity)
    try:
        trend_analysis = analyze_product_trend(db, product_id, days=60)
        
        if trend_analysis.trend_direction == "decreasing":
            risks.append(RiskAssessment(
                risk_type="trend",
                risk_level="medium",
                risk_score=40.0,
                reason="Product demand is declining",
                recommendation="Consider refreshing product, adjusting pricing, or running promotions. May be seasonal effect."
            ))
            risk_scores.append(40.0)
    except Exception:
        pass
    
    # 4. Financial Risk (high value inventory not moving)
    inventory_value = product.stock * product.price
    if inventory_value > 1000000:  # Adjust threshold as needed
        try:
            trend_analysis = analyze_product_trend(db, product_id, days=30)
            if trend_analysis.average_daily_sales < 1:
                risks.append(RiskAssessment(
                    risk_type="financial",
                    risk_level="high",
                    risk_score=70.0,
                    reason=f"High inventory value (Rp {inventory_value:,.0f}) with low turnover",
                    recommendation="Significant capital locked in slow-moving inventory. Consider discounts or return to supplier if possible."
                ))
                risk_scores.append(70.0)
        except Exception:
            pass
    
    # Calculate overall risk
    if not risks:
        overall_risk_score = 0.0
        overall_risk_level = "low"
    else:
        overall_risk_score = max(risk_scores)
        if overall_risk_score >= 80:
            overall_risk_level = "critical"
        elif overall_risk_score >= 60:
            overall_risk_level = "high"
        elif overall_risk_score >= 30:
            overall_risk_level = "medium"
        else:
            overall_risk_level = "low"
    
    # Save risk assessment to database
    db.query(ProductRisk).filter(ProductRisk.product_id == product_id).delete()
    
    for risk in risks:
        db_risk = ProductRisk(
            product_id=product_id,
            risk_type=risk.risk_type,
            risk_level=risk.risk_level,
            risk_score=risk.risk_score,
            reason=risk.reason,
            recommendation=risk.recommendation
        )
        db.add(db_risk)
    
    db.commit()
    
    return RiskResponse(
        product_id=product_id,
        product_name=product.name,
        overall_risk_level=overall_risk_level,
        overall_risk_score=overall_risk_score,
        risks=risks,
        assessed_at=datetime.utcnow()
    )


def get_high_risk_products(db: Session, merchant_id: str) -> HighRiskProductSummary:
    """Get all high-risk products for a merchant"""
    products = db.query(Product).filter(Product.merchant_id == merchant_id).all()
    
    high_risk_products = []
    critical_risk_products = []
    
    for product in products:
        try:
            risk_response = assess_product_risk(db, product.id)
            
            if risk_response.overall_risk_level in ["high", "critical"]:
                high_risk_products.append(product)
                
                if risk_response.overall_risk_level == "critical":
                    critical_risk_products.append(product)
        except Exception:
            continue
    
    # Convert to ProductResponse
    product_responses = [
        ProductResponse.model_validate(p) for p in high_risk_products
    ]
    
    return HighRiskProductSummary(
        total_high_risk=len(high_risk_products),
        total_critical_risk=len(critical_risk_products),
        products=product_responses
    )


def generate_risk_report(db: Session, merchant_id: str) -> dict:
    """Generate comprehensive risk report for merchant"""
    products = db.query(Product).filter(Product.merchant_id == merchant_id).all()
    
    report = {
        "merchant_id": merchant_id,
        "generated_at": datetime.utcnow().isoformat(),
        "total_products": len(products),
        "risk_breakdown": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        },
        "top_risks": []
    }
    
    all_risks = []
    
    for product in products:
        try:
            risk_response = assess_product_risk(db, product.id)
            
            # Count by level
            report["risk_breakdown"][risk_response.overall_risk_level] += 1
            
            # Collect for sorting
            if risk_response.overall_risk_score > 0:
                all_risks.append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "risk_level": risk_response.overall_risk_level,
                    "risk_score": risk_response.overall_risk_score,
                    "risks": [r.model_dump() for r in risk_response.risks]
                })
        except Exception:
            continue
    
    # Sort by risk score and take top 10
    all_risks.sort(key=lambda x: x["risk_score"], reverse=True)
    report["top_risks"] = all_risks[:10]
    
    return report
