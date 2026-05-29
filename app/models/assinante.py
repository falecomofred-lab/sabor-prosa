from sqlalchemy import Column, Integer, String, Date, ForeignKey
from ..database import Base
from datetime import date

class Assinante(Base):
    __tablename__ = "assinantes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    kit_id = Column(Integer, ForeignKey("kits.id"), nullable=False)
    data_inicio = Column(Date, nullable=False, default=date.today)
    dia_cobranca = Column(Integer, default=1)
    status = Column(String(20), default="ativo")
    proxima_entrega = Column(Date, nullable=True)
