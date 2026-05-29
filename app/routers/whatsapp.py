from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..services.ai_service import AIService
from ..database import SessionLocal
import httpx

router = APIRouter(prefix="/api/whatsapp", tags=["WhatsApp"])

@router.get("/webhook")
async def verificar_webhook(hub_mode: str = None, hub_challenge: str = None, hub_verify_token: str = None):
    if hub_verify_token == "sabor_prosa_token":
        return int(hub_challenge)
    return JSONResponse({"error": "Token inválido"}, status_code=403)

@router.post("/webhook")
async def receber_mensagem(request: Request):
    try:
        data = await request.json()
        mensagem = data['entry'][0]['changes'][0]['value']['messages'][0]
        texto = mensagem['text']['body']
        telefone = mensagem['from']
        db = SessionLocal()
        ai = AIService()
        result = await ai.chat_with_tools(texto, db)
        db.close()
        await enviar_mensagem_whatsapp(telefone, result.get("texto", "Desculpe, não consegui processar sua mensagem."))
        return JSONResponse({"status": "ok"})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

async def enviar_mensagem_whatsapp(telefone: str, mensagem: str):
    try:
        token = "SEU_TOKEN_WHATSAPP"
        phone_id = "SEU_PHONE_ID"
        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://graph.facebook.com/v18.0/{phone_id}/messages",
                headers={"Authorization": f"Bearer {token}"},
                json={"messaging_product": "whatsapp", "to": telefone, "text": {"body": mensagem[:1000]}}
            )
    except Exception as e:
        print(f"Erro ao enviar WhatsApp: {e}")
