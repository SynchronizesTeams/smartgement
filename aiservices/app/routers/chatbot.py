from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import (
    ChatMessage, ChatResponse,
    AutomationPreview, AutomationExecuteRequest, AutomationResult,
    UndoRequest
)
from app.services import chatbot_service, automation_service

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    """Send a message to the chatbot"""
    return await chatbot_service.process_chat_message(db, message)


@router.post("/automation/preview", response_model=AutomationPreview)
async def preview_automation(
    request: AutomationExecuteRequest,
    db: Session = Depends(get_db)
):
    """Preview what an automation command will do"""
    result = await automation_service.preview_automation(
        db, request.merchant_id, request.command
    )
    
    if not result["success"]:
        return AutomationPreview(
            operation_type="unknown",
            description=result.get("error", "Unknown error"),
            affected_products=[],
            affected_count=0,
            estimated_impact="",
            requires_confirmation=False
        )
    
    from app.schemas.product import ProductResponse
    return AutomationPreview(
        operation_type=result["operation_type"],
        description=result["description"],
        affected_products=[ProductResponse.model_validate(p) for p in result["affected_products"]],
        affected_count=result["affected_count"],
        estimated_impact=result["estimated_impact"],
        requires_confirmation=result["requires_confirmation"]
    )


@router.post("/automation/execute", response_model=AutomationResult)
async def execute_automation(
    request: AutomationExecuteRequest,
    db: Session = Depends(get_db)
):
    """Execute an automation command"""
    result = await automation_service.execute_automation(
        db, request.merchant_id, request.command, request.confirmed
    )
    
    if not result["success"]:
        return AutomationResult(
            success=False,
            operation_type="unknown",
            affected_count=0,
            affected_product_ids=[],
            message=result.get("error", "Unknown error"),
            can_undo=False
        )
    
    return AutomationResult(
        success=True,
        operation_type=result["operation_type"],
        affected_count=result["affected_count"],
        affected_product_ids=result["affected_product_ids"],
        message=result["message"],
        can_undo=result["can_undo"],
        operation_id=result.get("operation_id")
    )


@router.post("/automation/undo")
async def undo_automation(request: UndoRequest, db: Session = Depends(get_db)):
    """Undo a previous automation operation"""
    return await automation_service.undo_last_operation(
        db, request.merchant_id, request.operation_id
    )


@router.get("/automation/history")
def get_automation_history(
    merchant_id: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get automation operation history"""
    return automation_service.get_automation_history(db, merchant_id, limit)
