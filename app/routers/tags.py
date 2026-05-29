from fastapi import APIRouter
from ..database import SessionLocal
from ..models import Cliente
from datetime import datetime

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])

@router.post("/atualizar-tags")
async def atualizar_tags():
    db = SessionLocal()
    clientes = db.query(Cliente).all()
    agora = datetime.utcnow()
    for c in clientes:
        tags = []
        if c.total_compras > 1000: tags.append("VIP")
        if c.qtd_compras == 0: tags.append("Novo")
        if c.ultima_compra and (agora - c.ultima_compra).days > 30: tags.append("Inativo 30d")
        c.observacoes = ", ".join(tags) if tags else ""
    db.commit(); db.close()
    return {"status": "Tags atualizadas", "clientes_processados": len(clientes)}
