from fastapi import APIRouter
from ..database import SessionLocal
from ..models import Produto

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
