from openai import AsyncOpenAI
from app.config import settings
from typing import Optional, List, Dict

client = AsyncOpenAI(api_key=settings.openai_api_key)

async def get_embedding(text: str):
    """Generate embedding for text"""
    res = await client.embeddings.create(
        model=settings.embedding_model,
        input=text
    )
    return res.data[0].embedding

async def generate_text(
    prompt: str,
    max_tokens: int = None,
    system_prompt: Optional[str] = None,
    conversation_history: Optional[List[Dict]] = None
):
    """
    Generate text from prompt using LLM
    
    Args:
        prompt: User message/prompt
        max_tokens: Maximum tokens to generate
        system_prompt: Optional system message for context
        conversation_history: Optional list of previous messages
    """
    messages = []
    
    # Add system prompt if provided
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)
    
    # Add current user message
    messages.append({"role": "user", "content": prompt})
    
    res = await client.chat.completions.create(
        model=settings.llm_model,
        messages=messages,
        max_tokens=max_tokens or settings.max_tokens,
        temperature=settings.temperature
    )
    return res.choices[0].message.content

