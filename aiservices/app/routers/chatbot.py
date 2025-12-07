from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import (
    ChatMessage, ChatResponse,
    AutomationPreview, AutomationExecuteRequest, AutomationResult,
    UndoRequest
)
from app.services import chatbot_service, automation_service
from app.services.report_service import report_service
from app.services.education_service import education_service
from app.services.transaction_automation import transaction_automation_service
import json
import asyncio

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def chat(message: ChatMessage, db: Session = Depends(get_db)):
    """Send a message to the chatbot"""
    return await chatbot_service.process_chat_message(db, message)


@router.post("/message/stream")
async def chat_stream(message: ChatMessage, db: Session = Depends(get_db)):
    """Stream chatbot response in chunks for better UX"""
    async def generate():
        # Get full response first
        response = await chatbot_service.process_chat_message(db, message)
        
        # Send intent and confidence first
        yield f"data: {{\"type\": \"meta\", \"intent\": \"{response.intent}\", \"confidence\": {response.confidence}}}\n\n"
        
        # Stream response text word by word
        words = response.response.split()
        for i, word in enumerate(words):
            chunk = {
                "type": "text",
                "text": word + " ",
                "done": i == len(words) - 1
            }
            yield f"data: {json.dumps(chunk)}\n\n"
            await asyncio.sleep(0.03)  # 30ms delay for smooth animation
        
        # Send suggested actions
        if response.suggested_actions:
            actions_data = {
                "type": "actions",
                "actions": response.suggested_actions
            }
            yield f"data: {json.dumps(actions_data)}\n\n"
        
        # Final done signal
        yield f"data: {{\"type\": \"done\"}}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


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





@router.get("/chat/history")
def get_chat_history(
    merchant_id: str,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get chat conversation history"""
    from app.models.product import ChatHistory
    
    history = db.query(ChatHistory).filter(
        ChatHistory.merchant_id == merchant_id
    ).order_by(ChatHistory.created_at.desc()).limit(limit).all()
    
    return [
        {
            "id": h.id,
            "user_message": h.user_message,
            "ai_response": h.ai_response,
            "intent": h.intent,
            "created_at": h.created_at.isoformat()
        }
        for h in history
    ]


@router.post("/business-tips")
async def get_business_tips(merchant_id: str, db: Session = Depends(get_db)):
    """Get business education tips based on merchant's business type"""
    return await education_service.get_business_tips(db, merchant_id)


@router.post("/growth-strategy")
async def get_growth_strategy(merchant_id: str, db: Session = Depends(get_db)):
    """Get personalized growth strategy"""
    strategy = await education_service.get_growth_strategy(db, merchant_id)
    return {"strategy": strategy}


@router.post("/automation/transaction")
async def create_transaction_auto(merchant_id: str, description: str, db: Session = Depends(get_db)):
    """Create transaction from natural language description"""
    result = await transaction_automation_service.create_transaction_data(db, merchant_id, description)
    return result


@router.post("/automation/batch-products")
async def batch_add_products(merchant_id: str, description: str, db: Session = Depends(get_db)):
    """Add multiple products from package description"""
    result = await transaction_automation_service.batch_add_products(db, merchant_id, description)
    return result
