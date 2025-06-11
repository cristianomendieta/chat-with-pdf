from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

api = APIRouter()

class ChatRequest(BaseModel):
    message: str
    
class ChatResponse(BaseModel):
    response: str
    sources: List[str] = []

@api.post("/chat", response_model=ChatResponse)
async def chat_with_pdf(request: ChatRequest):
    """
    Chat endpoint for interacting with PDF content
    """
    # Placeholder response - here you would integrate with your PDF processing logic
    return ChatResponse(
        response=f"You asked: '{request.message}'. This is a placeholder response. PDF processing will be implemented here.",
        sources=["example.pdf"]
    )

@api.get("/status")
async def get_status():
    """
    Get the status of the assistant service
    """
    return {"status": "ready", "message": "Assistant is ready to chat with PDFs"}
