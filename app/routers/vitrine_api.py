from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from ..database import SessionLocal
from ..models import Produto

router = APIRouter(prefix="/api/vitrine", tags=["Vitrine"])

@router.post("/pedido")
async def registrar_pedido(data: dict):
    """Registra pedido da vitrine e abate estoque."""
    db = SessionLocal()
    itens = data.get("itens", [])
    cliente_nome = data.get("cliente", "Cliente")
    cliente_telefone = data.get("telefone", "")
    
    total = 0.0
    produtos_vendidos = []
    
    for item in itens:
        produto = db.query(Produto).filter(Produto.id == item["id"]).first()
        if produto and produto.estoque_atual >= item["qtd"]:
            produto.estoque_atual -= item["qtd"]
            total += produto.preco_venda * item["qtd"]
            produtos_vendidos.append({
                "nome": produto.nome,
                "qtd": item["qtd"],
                "preco": produto.preco_venda
            })
    
    db.commit()
    db.close()
    
    return JSONResponse({
        "sucesso": True,
        "cliente": cliente_nome,
        "total": round(total, 2),
        "produtos": produtos_vendidos,
        "mensagem": f"Pedido de {cliente_nome} registrado! Total: R$ {total:.2f}"
    })
