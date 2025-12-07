from sqlalchemy.orm import Session
from sqlalchemy import text, func
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
from app.services.llm_client import generate_text


async def generate_transaction_summary(
    db: Session,
    merchant_id: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    payment_method: Optional[str] = None,
    limit: int = 100
) -> Dict[str, Any]:
    """Generate AI-powered transaction summary"""
    
    # Build query
    query = """
        SELECT 
            t.id, t.total_amount, t.payment_method, t.customer_name,
            t.status, t.created_at,
            GROUP_CONCAT(CONCAT(ti.product_name, ' (', ti.quantity, ')') SEPARATOR ', ') as items
        FROM transactions t
        LEFT JOIN transaction_items ti ON t.id = ti.transaction_id
        WHERE t.merchant_id = :merchant_id
    """
    
    params = {"merchant_id": int(merchant_id)}
    
    # Add filters
    if date_from:
        query += " AND DATE(t.created_at) >= :date_from"
        params["date_from"] = date_from
    
    if date_to:
        query += " AND DATE(t.created_at) <= :date_to"
        params["date_to"] = date_to
    
    if payment_method:
        query += " AND t.payment_method = :payment_method"
        params["payment_method"] = payment_method
    
    query += " GROUP BY t.id ORDER BY t.created_at DESC LIMIT :limit"
    params["limit"] = limit
    
    # Execute query
    result = db.execute(text(query), params)
    transactions = [dict(row._mapping) for row in result]
    
    # Calculate statistics
    total_transactions = len(transactions)
    completed_transactions = [t for t in transactions if t['status'] == 'completed']
    total_revenue = sum(float(t['total_amount']) for t in completed_transactions)
    average_transaction = total_revenue / len(completed_transactions) if completed_transactions else 0
    
    # Payment method breakdown
    payment_methods = {}
    for t in completed_transactions:
        method = t['payment_method'] or 'unknown'
        payment_methods[method] = payment_methods.get(method, 0) + 1
    
    # Generate insights
    insights = []
    
    # Peak time analysis
    if transactions:
        hours = {}
        for t in transactions:
            hour = t['created_at'].hour
            hours[hour] = hours.get(hour, 0) + 1
        
        if hours:
            peak_hour = max(hours.items(), key=lambda x: x[1])
            insights.append({
                "type": "peak_hour",
                "title": "Peak Sales Hour",
                "description": f"Most transactions occur at {peak_hour[0]}:00 with {peak_hour[1]} sales",
                "value": f"{peak_hour[0]}:00",
                "confidence": 0.9
            })
    
    # Payment method preference
    if payment_methods:
        top_method = max(payment_methods.items(), key=lambda x: x[1])
        method_labels = {
            'cash': 'Tunai',
            'card': 'Kartu',
            'ewallet': 'E-Wallet'
        }
        insights.append({
            "type": "payment_preference",
            "title": "Preferred Payment Method",
            "description": f"{method_labels.get(top_method[0], top_method[0])} is used in {top_method[1]} transactions",
            "value": top_method[0],
            "confidence": 0.85
        })
    
    # Revenue trend
    if len(completed_transactions) >= 2:
        # Simple trend: compare first half vs second half
        mid = len(completed_transactions) // 2
        first_half_rev = sum(float(t['total_amount']) for t in completed_transactions[:mid])
        second_half_rev = sum(float(t['total_amount']) for t in completed_transactions[mid:])
        
        if second_half_rev > first_half_rev * 1.1:
            trend = "increasing"
            description = "Revenue is trending upward"
        elif second_half_rev < first_half_rev * 0.9:
            trend = "decreasing"
            description = "Revenue is trending downward"
        else:
            trend = "stable"
            description = "Revenue is stable"
        
        insights.append({
            "type": "revenue_trend",
            "title": "Revenue Trend",
            "description": description,
            "value": trend,
            "confidence": 0.75
        })
    
    # Generate natural language summary using LLM
    period_desc = "all time"
    if date_from and date_to:
        period_desc = f"from {date_from} to {date_to}"
    elif date_from:
        period_desc = f"since {date_from}"
    elif date_to:
        period_desc = f"until {date_to}"
    
    # Prepare data for LLM
    context = f"""
    Transaction Summary for Merchant {merchant_id} ({period_desc}):
    - Total Transactions: {total_transactions}
    - Completed: {len(completed_transactions)}
    - Total Revenue: Rp{total_revenue:,.2f}
    - Average Transaction: Rp{average_transaction:,.2f}
    - Payment Methods: {json.dumps(payment_methods)}
    
    Insights:
    {json.dumps(insights, indent=2)}
    """
    
    prompt = f"""Based on the following transaction data, generate a concise, friendly summary in Indonesian (Bahasa Indonesia) 
    for a merchant. Keep it brief (2-3 sentences) and highlight the most important points.
    
    {context}
    
    Summary:"""
    
    try:
        summary_text = await generate_text(prompt, max_tokens=200)
    except Exception as e:
        # Fallback summary if LLM fails
        summary_text = f"Anda memiliki {total_transactions} transaksi dengan total pendapatan Rp{total_revenue:,.2f}. Rata-rata nilai transaksi adalah Rp{average_transaction:,.2f}."
    
    return {
        "summary": summary_text,
        "total_transactions": total_transactions,
        "total_revenue": total_revenue,
        "average_transaction": average_transaction,
        "insights": insights,
        "period": period_desc
    }


async def analyze_transaction_query(
    db: Session,
    merchant_id: str,
    query: str
) -> Dict[str, Any]:
    """Analyze natural language query about transactions"""
    
    # Determine query intent and time period
    query_lower = query.lower()
    
    # Extract time period
    date_from = None
    date_to = None
    
    today = datetime.now().date()
    
    if "hari ini" in query_lower or "today" in query_lower:
        date_from = today.isoformat()
        date_to = today.isoformat()
    elif "kemarin" in query_lower or "yesterday" in query_lower:
        yesterday = today - timedelta(days=1)
        date_from = yesterday.isoformat()
        date_to = yesterday.isoformat()
    elif "minggu ini" in query_lower or "this week" in query_lower:
        week_start = today - timedelta(days=today.weekday())
        date_from = week_start.isoformat()
        date_to = today.isoformat()
    elif "bulan ini" in query_lower or "this month" in query_lower:
        date_from = today.replace(day=1).isoformat()
        date_to = today.isoformat()
    
    # Generate summary with detected time period
    return await generate_transaction_summary(
        db=db,
        merchant_id=merchant_id,
        date_from=date_from,
        date_to=date_to
    )
