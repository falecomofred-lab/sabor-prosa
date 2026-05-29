from sqlalchemy import Column, Integer, String, Float, Date, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from ..database import Base
import enum

class CategoriaProduto(str, enum.Enum):
    QUEIJOS = "Queijos"
    VINHOS = "Vinhos"
    GELEIAS = "Geleias"
    CAFES = "Cafés"
    OUTROS = "Outros"

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(200), nullable=False, index=True)
    categoria = Column(SQLEnum(CategoriaProduto), nullable=False)
    codigo_barras = Column(String(50), unique=True, index=True)
    preco_custo = Column(Float, nullable=False, default=0.0)
    preco_venda = Column(Float, nullable=False, default=0.0)
    estoque_atual = Column(Integer, nullable=False, default=0)
    estoque_minimo = Column(Integer, nullable=False, default=5)
    validade = Column(Date, nullable=True)
    descricao_curta = Column(Text, default="")
    historia = Column(Text, default="")
    foto_url = Column(String(500), default="")
    lotes = relationship("Lote", back_populates="produto", cascade="all, delete-orphan")
    
    @property
    def margem_percentual(self) -> float:
        if self.preco_custo > 0: return round((self.preco_venda - self.preco_custo) / self.preco_custo * 100, 2)
        return 0.0
    
    @property
    def precisa_repor(self) -> bool:
        return self.estoque_atual <= self.estoque_minimo
