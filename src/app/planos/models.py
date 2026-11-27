from sqlalchemy import Column, Integer, String, Numeric
from app.database import Base

class Plano(Base):
    __tablename__ = "planos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(80), nullable=False, unique=True)
    descricao = Column(String(255))
    preco = Column(Numeric(8,2), nullable=False)
    duracao_dias = Column(Integer, default=30, nullable=False)
