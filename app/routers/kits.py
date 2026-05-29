from fastapi import APIRouter, Form
from ..database import SessionLocal
from ..models import Kit, kit_itens
from fastapi.responses import RedirectResponse
import json

router = APIRouter(prefix="/api/kits", tags=["Kits"])

@router.post("/form")
async def salvar_kit(id: int = Form(None), nome: str = Form(...), descricao: str = Form(""), preco_venda: float = Form(...), itens_json: str = Form("[]")):
    db = SessionLocal()
    itens = json.loads(itens_json)
    custo_total = sum(item["custo"] * item["qtd"] for item in itens)
    margem = round(((preco_venda - custo_total) / custo_total * 100), 2) if custo_total > 0 else 0
    if id:
        kit = db.query(Kit).filter(Kit.id == id).first()
        kit.nome = nome
        kit.descricao = descricao
        kit.preco_venda = preco_venda
        kit.margem_percentual = margem
        db.execute(kit_itens.delete().where(kit_itens.c.kit_id == id))
    else:
        kit = Kit(nome=nome, descricao=descricao, preco_venda=preco_venda, margem_percentual=margem)
        db.add(kit)
        db.flush()
    for item in itens:
        db.execute(kit_itens.insert().values(kit_id=kit.id, produto_id=item["id"], quantidade=item["qtd"]))
    db.commit()
    db.close()
    return RedirectResponse(url="/kits", status_code=303)