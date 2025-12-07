"""
Reports Router
PDF report generation endpoints
"""
from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.report_service import report_service
from io import BytesIO

router = APIRouter()

@router.post("/generate")
async def generate_report(
    merchant_id: str,
    report_type: str = "summary",
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Generate PDF report"""
    
    if report_type == "sales":
        pdf_bytes = report_service.generate_sales_report(db, merchant_id, days)
        filename = f"laporan_penjualan_{days}hari.pdf"
    elif report_type == "inventory":
        pdf_bytes = report_service.generate_inventory_report(db, merchant_id)
        filename = "laporan_inventori.pdf"
    else:  # summary
        pdf_bytes = report_service.generate_summary_report(db, merchant_id)
        filename = "ringkasan_bisnis.pdf"
    
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
