from sqlalchemy import Column, Integer, String, Date, Text
from ..database import Base

class Evento(Base):
    __tablename__ = "eventos"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(200), nullable=False, index=True)
    data = Column(Date, nullable=True)
    local = Column(String(300), default="")
    descricao = Column(Text, default="")
    tipo = Column(String(50), default="")
