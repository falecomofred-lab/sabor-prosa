from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from ..models.produto import CategoriaProduto

class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=200)
    categoria: CategoriaProduto
    codigo_barras: Optional[str] = Field(None, max_length=50)
    preco_custo: float = Field(..., ge=0)
    preco_venda: float = Field(..., ge=0)
    estoque_atual: int = Field(0, ge=0)
    estoque_minimo: int = Field(5, ge=0)
    validade: Optional[date] = None
    descricao_curta: str = ""
    historia: str = ""
    foto_url: str = ""

class ProdutoCreate(ProdutoBase): pass

class ProdutoUpdate(BaseModel):
    nome: Optional[str] = None
    categoria: Optional[CategoriaProduto] = None
    codigo_barras: Optional[str] = None
    preco_custo: Optional[float] = None
    preco_venda: Optional[float] = None
    estoque_atual: Optional[int] = None
    estoque_minimo: Optional[int] = None
    validade: Optional[date] = None
    descricao_curta: Optional[str] = None
    historia: Optional[str] = None
    foto_url: Optional[str] = None

class ProdutoResponse(ProdutoBase):
    id: int
    margem_percentual: float
    precisa_repor: bool
    class Config: from_attributes = True
