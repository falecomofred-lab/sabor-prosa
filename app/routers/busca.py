from fastapi import APIRouter, Query
from ..database import SessionLocal
from ..models import Produto, Fornecedor, Cliente, Evento

router = APIRouter(prefix="/api/busca", tags=["Busca"])

@router.get("")
async def buscar_tudo(termo: str = Query(..., min_length=1)):
    db = SessionLocal()
    termo_like = "%" + termo + "%"
    produtos = db.query(Produto).filter(Produto.nome.ilike(termo_like) | Produto.codigo_barras.ilike(termo_like) | Produto.categoria.ilike(termo_like)).limit(20).all()
    fornecedores = db.query(Fornecedor).filter(Fornecedor.nome.ilike(termo_like) | Fornecedor.cnpj.ilike(termo_like)).limit(10).all()
    clientes = db.query(Cliente).filter(Cliente.nome.ilike(termo_like) | Cliente.telefone.ilike(termo_like)).limit(10).all()
    eventos = db.query(Evento).filter(Evento.nome.ilike(termo_like) | Evento.local.ilike(termo_like)).limit(10).all()
    db.close()
    return {
        "produtos": [{"id": p.id, "nome": p.nome, "categoria": p.categoria, "codigo_barras": p.codigo_barras, "preco_venda": p.preco_venda, "estoque_atual": p.estoque_atual, "margem_percentual": p.margem_percentual, "foto_url": p.foto_url} for p in produtos],
        "fornecedores": [{"id": f.id, "nome": f.nome, "cnpj": f.cnpj, "cidade": f.cidade, "uf": f.uf, "telefone": f.telefone} for f in fornecedores],
        "clientes": [{"id": c.id, "nome": c.nome, "telefone": c.telefone, "total_compras": c.total_compras} for c in clientes],
        "eventos": [{"id": e.id, "nome": e.nome, "data": str(e.data) if e.data else None, "local": e.local, "tipo": e.tipo} for e in eventos]
    }
