from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from ..database import Base
from datetime import datetime

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(200), nullable=False, index=True)
    telefone = Column(String(20), unique=True, index=True)
    email = Column(String(200), default="")
    cpf = Column(String(14), default="")
    data_nascimento = Column(Date, nullable=True)
    endereco = Column(String(300), default="")
    total_compras = Column(Float, default=0.0)
    qtd_compras = Column(Integer, default=0)
    ultima_compra = Column(DateTime, default=datetime.utcnow)
    observacoes = Column(String(500), default="")
