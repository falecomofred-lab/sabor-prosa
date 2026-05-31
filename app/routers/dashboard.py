from fastapi import APIRouter
from fastapi.responses import JSONResponse
from ..database import SessionLocal
from ..models import Produto, Cliente, Evento
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/caixa-comparativo")
async def caixa_comparativo():
    return {"hoje": 1250.00, "semana_passada": 980.00, "percentual": 27.5, "tendencia": "alta"}

@router.get("/alertas-estoque")
async def alertas_estoque():
    db = SessionLocal()
    produtos = db.query(Produto).filter(Produto.estoque_atual <= Produto.estoque_minimo).all()
    alertas = [{"id": p.id, "nome": p.nome, "estoque_atual": p.estoque_atual, "estoque_minimo": p.estoque_minimo, "whatsapp_link": f"https://wa.me/?text=Olá, preciso de reposição do {p.nome} (estoque: {p.estoque_atual})"} for p in produtos]
    db.close()
    return alertas

@router.get("/prioridades")
async def prioridades():
    db = SessionLocal()
    hoje = datetime.utcnow().date()
    
    alta = []
    criticos = db.query(Produto).filter(Produto.estoque_atual == 0).all()
    for p in criticos:
        alta.append({"texto": f"{p.nome} - Estoque ZERADO!", "link": "/produtos", "acao": "Repor"})
    
    vencendo = db.query(Produto).filter(Produto.validade <= hoje + timedelta(days=3), Produto.validade >= hoje).all()
    for p in vencendo:
        alta.append({"texto": f"{p.nome} vence em breve!", "link": "/produtos", "acao": "Ver"})
    
    media = []
    baixos = db.query(Produto).filter(Produto.estoque_atual <= Produto.estoque_minimo, Produto.estoque_atual > 0).all()
    for p in baixos[:3]:
        media.append({"texto": f"{p.nome} - Estoque baixo ({p.estoque_atual})", "link": "/produtos", "acao": "Repor"})
    
    baixa = [
        {"texto": "Gerar post para Instagram"},
        {"texto": "Verificar agenda de eventos"},
        {"texto": "Atualizar preços da vitrine"},
        {"texto": "Revisar checklist de feiras"},
    ]
    
    db.close()
    return JSONResponse({"alta": alta, "media": media, "baixa": baixa})