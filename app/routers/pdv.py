from fastapi import APIRouter, Query
from ..database import SessionLocal
from ..models import Produto

router = APIRouter(prefix="/api/pdv", tags=["PDV"])

@router.get("/favoritos")
async def produtos_favoritos():
    db = SessionLocal()
    produtos = db.query(Produto).filter(Produto.estoque_atual > 0).limit(10).all()
    result = [{"id": p.id, "nome": p.nome, "preco": p.preco_venda, "foto": p.foto_url or "", "estoque": p.estoque_atual} for p in produtos]
    db.close()
    return result

@router.get("/buscar")
async def buscar_produto(codigo: str = Query(...)):
    db = SessionLocal()
    produto = db.query(Produto).filter(Produto.codigo_barras == codigo).first()
    db.close()
    if not produto: return {"erro": "Produto não encontrado"}
    return {"id": produto.id, "nome": produto.nome, "preco": produto.preco_venda, "estoque": produto.estoque_atual, "foto": produto.foto_url or ""}

@router.post("/vender")
async def registrar_venda(data: dict):
    db = SessionLocal()
    itens = data.get("itens", [])
    total = 0.0
    for item in itens:
        produto = db.query(Produto).filter(Produto.id == item["id"]).first()
        if produto and produto.estoque_atual >= item["qtd"]:
            produto.estoque_atual -= item["qtd"]
            total += produto.preco_venda * item["qtd"]
    db.commit()
    db.close()
    return {"total": round(total, 2), "status": "sucesso"}

@router.get("/sugestao")
async def sugestao_cross_selling(produto_id: int = Query(...)):
    db = SessionLocal()
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto: db.close(); return {"sugestao": None}
    complementar = db.query(Produto).filter(Produto.id != produto_id, Produto.categoria != produto.categoria, Produto.estoque_atual > 0).first()
    db.close()
    if complementar: return {"sugestao": f"Ofereça {complementar.nome} (R$ {complementar.preco_venda:.2f}) junto com {produto.nome}!"}
    return {"sugestao": None}
