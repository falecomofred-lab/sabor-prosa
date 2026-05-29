from sqlalchemy import Column, Integer, String, Text
from ..database import Base

class Fornecedor(Base):
    __tablename__ = "fornecedores"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(200), nullable=False, index=True)
    cnpj = Column(String(18), unique=True, index=True)
    contato = Column(String(200), default="")
    telefone = Column(String(20), default="")
    email = Column(String(200), default="")
    cep = Column(String(10), default="")
    logradouro = Column(String(200), default="")
    bairro = Column(String(100), default="")
    cidade = Column(String(100), default="")
    uf = Column(String(2), default="")
    observacoes = Column(Text, default="")
