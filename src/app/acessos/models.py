from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base

class Acesso(Base):
    __tablename__ = "acessos"

    id = Column(Integer, primary_key=True, index=True)
    protocolo = Column(String(20), nullable=False)
    liberado = Column(Boolean, nullable=False)
    motivo = Column(String(120), nullable=False)
    data_hora = Column(DateTime, default=datetime.now)
    cadastro_id = Column(Integer, ForeignKey("cadastros.id"))