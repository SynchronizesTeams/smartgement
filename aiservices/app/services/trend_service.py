from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, date, timedelta
from app.models.product import Product, ProductTrend
from app.schemas.product import RecordSaleRequest, TrendAnalysisResponse, TrendDataPoint, DemandPrediction
import statistics


def record_sale(db: Session, sale: RecordSaleRequest) -> ProductTrend:
    """Record a product sale for trend tracking"""
    sale_date = sale.date or date.today()
    
    # Check if trend record exists for this date
    existing_trend = db.query(ProductTrend).filter(
        ProductTrend.product_id == sale.product_id,
        ProductTrend.date == sale_date
    ).first()
    
    if existing_trend:
        # Update existing record
        existing_trend.quantity_sold += sale.quantity
        product = db.query(Product).filter(Product.id == sale.product_id).first()
        if product:
            existing_trend.revenue += sale.quantity * product.price
        db.commit()
        db.refresh(existing_trend)
        return existing_trend
    else:
        # Create new record
        product = db.query(Product).filter(Product.id == sale.product_id).first()
        revenue = sale.quantity * product.price if product else 0.0
        
        trend = ProductTrend(
            product_id=sale.product_id,
            date=sale_date,
            quantity_sold=sale.quantity,
            revenue=revenue,
            popularity_score=sale.quantity  # Simple popularity metric
        )
        db.add(trend)
        db.commit()
        db.refresh(trend)
        return trend


def analyze_product_trend(
    db: Session,
    product_id: int,
    days: int = 30
) -> TrendAnalysisResponse:
    """Analyze product trend over specified period"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ValueError("Product not found")
    
    # Get trend data
    start_date = date.today() - timedelta(days=days)
    trends = db.query(ProductTrend).filter(
        ProductTrend.product_id == product_id,
        ProductTrend.date >= start_date
    ).order_by(ProductTrend.date).all()
    
    if not trends:
        return TrendAnalysisResponse(
            product_id=product_id,
            product_name=product.name,
            analysis_period_days=days,
            average_daily_sales=0.0,
            peak_dates=[],
            trend_direction="no_data",
            seasonality_detected=False,
            data_points=[]
        )
    
    # Calculate metrics
    total_sales = sum(t.quantity_sold for t in trends)
    average_daily_sales = total_sales / len(trends) if trends else 0
    
    # Find peak dates (top 20% of sales days)
    sorted_trends = sorted(trends, key=lambda t: t.quantity_sold, reverse=True)
    peak_count = max(1, len(sorted_trends) // 5)
    peak_dates = [t.date for t in sorted_trends[:peak_count]]
    
    # Determine trend direction
    if len(trends) >= 7:
        first_week_avg = statistics.mean([t.quantity_sold for t in trends[:7]])
        last_week_avg = statistics.mean([t.quantity_sold for t in trends[-7:]])
        
        if last_week_avg > first_week_avg * 1.2:
            trend_direction = "increasing"
        elif last_week_avg < first_week_avg * 0.8:
            trend_direction = "decreasing"
        else:
            trend_direction = "stable"
    else:
        trend_direction = "insufficient_data"
    
    # Check for seasonality (simple weekly pattern detection)
    seasonality_detected = False
    if len(trends) >= 14:
        # Group by day of week
        day_groups = {}
        for t in trends:
            day_of_week = t.date.weekday()
            if day_of_week not in day_groups:
                day_groups[day_of_week] = []
            day_groups[day_of_week].append(t.quantity_sold)
        
        # Check if there's significant variation between days
        if len(day_groups) >= 5:
            day_averages = [statistics.mean(sales) for sales in day_groups.values() if sales]
            if day_averages:
                std_dev = statistics.stdev(day_averages) if len(day_averages) > 1 else 0
                mean_sales = statistics.mean(day_averages)
                if mean_sales > 0 and std_dev / mean_sales > 0.3:
                    seasonality_detected = True
    
    # Prepare data points
    data_points = [
        TrendDataPoint(
            date=t.date,
            quantity_sold=t.quantity_sold,
            revenue=t.revenue,
            popularity_score=t.popularity_score
        )
        for t in trends
    ]
    
    return TrendAnalysisResponse(
        product_id=product_id,
        product_name=product.name,
        analysis_period_days=days,
        average_daily_sales=average_daily_sales,
        peak_dates=peak_dates,
        trend_direction=trend_direction,
        seasonality_detected=seasonality_detected,
        data_points=data_points
    )


def predict_demand(
    db: Session,
    product_id: int
) -> DemandPrediction:
    """Predict future demand based on historical trends"""
    # Get last 60 days of data
    start_date = date.today() - timedelta(days=60)
    trends = db.query(ProductTrend).filter(
        ProductTrend.product_id == product_id,
        ProductTrend.date >= start_date
    ).order_by(ProductTrend.date).all()
    
    if not trends or len(trends) < 7:
        return DemandPrediction(
            product_id=product_id,
            predicted_demand_next_7_days=0.0,
            predicted_demand_next_30_days=0.0,
            confidence_level="low",
            recommendation="Not enough historical data for accurate prediction. Continue tracking sales."
        )
    
    # Simple moving average prediction
    recent_sales = [t.quantity_sold for t in trends[-14:]]  # Last 2 weeks
    daily_average = statistics.mean(recent_sales)
    
    # Adjust for trend
    if len(trends) >= 14:
        older_sales = [t.quantity_sold for t in trends[-28:-14]]
        older_average = statistics.mean(older_sales)
        
        if daily_average > older_average:
            growth_rate = (daily_average - older_average) / older_average if older_average > 0 else 0
            daily_average *= (1 + growth_rate * 0.5)  # Conservative growth projection
    
    predicted_7_days = daily_average * 7
    predicted_30_days = daily_average * 30
    
    # Determine confidence
    if len(trends) >= 30:
        confidence = "high"
    elif len(trends) >= 14:
        confidence = "medium"
    else:
        confidence = "low"
    
    # Generate recommendation
    product = db.query(Product).filter(Product.id == product_id).first()
    current_stock = product.stock if product else 0
    
    if current_stock < predicted_7_days:
        recommendation = f"Low stock alert! Current stock ({current_stock}) may not cover next week's demand ({predicted_7_days:.0f}). Consider restocking."
    elif current_stock > predicted_30_days * 2:
        recommendation = f"Overstock detected. Current stock ({current_stock}) is more than 2 months of predicted demand. Consider promotions."
    else:
        recommendation = f"Stock level is adequate. Current stock ({current_stock}) should cover {(current_stock / daily_average):.0f} days at current demand rate."
    
    return DemandPrediction(
        product_id=product_id,
        predicted_demand_next_7_days=predicted_7_days,
        predicted_demand_next_30_days=predicted_30_days,
        confidence_level=confidence,
        recommendation=recommendation
    )


def recommend_order_quantity(db: Session, product_id: int) -> dict:
    """Recommend purchase quantity based on trends"""
    prediction = predict_demand(db, product_id)
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        return {"error": "Product not found"}
    
    current_stock = product.stock
    weekly_demand = prediction.predicted_demand_next_7_days
    
    # Calculate recommended order quantity
    # Target: 2 weeks of stock
    target_stock = weekly_demand * 2
    recommended_order = max(0, target_stock - current_stock)
    
    return {
        "product_id": product_id,
        "product_name": product.name,
        "current_stock": current_stock,
        "weekly_demand": weekly_demand,
        "target_stock": target_stock,
        "recommended_order_quantity": recommended_order,
        "reasoning": f"To maintain 2 weeks of inventory based on predicted demand of {weekly_demand:.0f} units per week"
    }
