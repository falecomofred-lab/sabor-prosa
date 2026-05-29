from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..services.ai_service import AIService

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])
ai_service = AIService()

class ChatRequest(BaseModel): mensagem: str
class ChatResponse(BaseModel): resposta: str; usou_tools: bool = False

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        result = await ai_service.chat_with_tools(request.mensagem, db)
        return ChatResponse(resposta=result["texto"], usou_tools=result["usou_tools"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")
