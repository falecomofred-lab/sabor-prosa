from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..services.ai_service import ClaudeteIA

router = APIRouter(prefix="/api/chat", tags=["Chatbot"])
claudete = ClaudeteIA()

class ChatRequest(BaseModel):
    mensagem: str

class ChatResponse(BaseModel):
    resposta: str
    usou_ferramentas: bool = False

@router.post("/", response_model=ChatResponse)
async def conversar(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        resultado = await claudete.conversar(request.mensagem, db)
        return ChatResponse(
            resposta=resultado["resposta"],
            usou_ferramentas=resultado["usou_ferramentas"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro: {str(e)}")
