from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..database import Base

kit_itens = Table("kit_itens", Base.metadata,
    Column("kit_id", Integer, ForeignKey("kits.id", ondelete="CASCADE"), primary_key=True),
    Column("produto_id", Integer, ForeignKey("produtos.id"), primary_key=True),
    Column("quantidade", Integer, nullable=False, default=1),
)

class Kit(Base):
    __tablename__ = "kits"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(200), nullable=False)
    descricao = Column(String(500), default="")
    preco_venda = Column(Float, nullable=False)
    margem_percentual = Column(Float, default=0.0)
    itens = relationship("Produto", secondary=kit_itens, lazy="joined")
