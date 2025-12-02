from fastapi import APIRouter
from app.services.llm_client import generate_text

router = APIRouter()

@router.post("/generate-description")
async def gen_desc(body: dict):
    product_name = body["name"]
    context = body.get("context", "")

    prompt = f"""
    Create a compelling product description for:
    {product_name}

    Business context:
    {context}
    """

    output = await generate_text(prompt)
    return {"description": output}
