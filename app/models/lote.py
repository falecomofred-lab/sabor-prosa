from sqlalchemy import Column, Integer, Float, Date, ForeignKey, String
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import date

class Lote(Base):
    __tablename__ = "lotes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False)
    codigo_lote = Column(String(50), nullable=False)
    quantidade_inicial = Column(Integer, nullable=False)
    quantidade_atual = Column(Integer, nullable=False)
    data_fabricacao = Column(Date, nullable=False)
    data_validade = Column(Date, nullable=False, index=True)
    preco_custo = Column(Float, nullable=False)
    produto = relationship("Produto", back_populates="lotes")
    
    @property
    def dias_ate_vencimento(self) -> int:
        return (self.data_validade - date.today()).days
