from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.produto import Produto, CategoriaProduto
from ..schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse

router = APIRouter(prefix="/api/produtos", tags=["Produtos"])

@router.get("/", response_model=List[ProdutoResponse])
async def listar_produtos(categoria: Optional[CategoriaProduto] = None, busca: Optional[str] = Query(None, min_length=2), estoque_baixo: bool = False, db: Session = Depends(get_db)):
    query = db.query(Produto)
    if categoria: query = query.filter(Produto.categoria == categoria)
    if busca: query = query.filter(Produto.nome.ilike(f"%{busca}%") | Produto.codigo_barras.ilike(f"%{busca}%"))
    if estoque_baixo: query = query.filter(Produto.estoque_atual <= Produto.estoque_minimo)
    return query.order_by(Produto.nome).all()

@router.get("/{produto_id}", response_model=ProdutoResponse)
async def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto: raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/", response_model=ProdutoResponse, status_code=201)
async def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    db_produto = Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.put("/{produto_id}", response_model=ProdutoResponse)
async def atualizar_produto(produto_id: int, produto: ProdutoUpdate, db: Session = Depends(get_db)):
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not db_produto: raise HTTPException(status_code=404, detail="Produto não encontrado")
    for key, value in produto.model_dump(exclude_unset=True).items():
        setattr(db_produto, key, value)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@router.delete("/{produto_id}", status_code=204)
async def excluir_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not db_produto: raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(db_produto)
    db.commit()

@router.post("/{produto_id}/duplicar")
async def duplicar_produto(produto_id: int, db: Session = Depends(get_db)):
    original = db.query(Produto).filter(Produto.id == produto_id).first()
    if not original: raise HTTPException(status_code=404, detail="Produto não encontrado")
    novo = Produto(nome=f"[CÓPIA] {original.nome}", categoria=original.categoria, preco_custo=original.preco_custo, preco_venda=original.preco_venda, estoque_atual=0, estoque_minimo=original.estoque_minimo, descricao_curta=original.descricao_curta, historia=original.historia, codigo_barras="", foto_url="")
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo
