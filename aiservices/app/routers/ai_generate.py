from fastapi import APIRouter
from app.services.llm_client import generate_text

router = APIRouter()

@router.post("/generate-description")
async def gen_desc(body: dict):
    product_name = body["name"]
    context = body.get("context", "")

    prompt = f"""
    Buat deskripsi produk yang menarik untuk:
    {product_name}

    Konteks bisnis:
    {context}
    """

    output = await generate_text(prompt)
    return {"description": output}
