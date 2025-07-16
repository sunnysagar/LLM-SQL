"""
    This route:

Accepts a user query (POST /chat)

Searches similar docs using FAISS

Sends the context + query to the selected LLM

Returns the response to the client
"""


from fastapi import APIRouter
from pydantic import BaseModel
from app.services.faiss_service import search
from app.services.llm_factory import get_llm_response

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    provider: str = "openai"  # Default if not provided


@router.post("/chat")
async def chat(req: ChatRequest):
    # Step 1: Search context using FAISS
    context_list = search(req.query)
    context = "\n".join(context_list)

    # Step 2: Create a complete prompt
    prompt = f"""Context:
{context}

Question:
{req.query}
"""

    # Step 3: Call LLM
    answer = await get_llm_response(prompt, provider=req.provider)

    # Step 4: Return response
    return {"response": answer}
