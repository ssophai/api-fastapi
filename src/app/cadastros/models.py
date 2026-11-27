from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, Boolean, Date
from sqlalchemy.orm import relationship
from app.database import Base

cadastro_modalidade = Table(
    "cadastro_modalidade",
    Base.metadata,
    Column("cadastro_id", ForeignKey("cadastros.id"), primary_key=True),
    Column("modalidade_id", ForeignKey("modalidades.id"), primary_key=True),
)

class Cadastro(Base):
    __tablename__ = "cadastros"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(120))
    objetivo = Column(String(255))
    observacoes = Column(String(500))
    protocolo = Column(String(20), unique=True, nullable=False)
    criado_em = Column(DateTime, default=datetime.now)
    ativo = Column(Boolean, default=False, nullable=False)
    data_validade = Column(Date)

    plano_id = Column(Integer, ForeignKey("planos.id"), nullable=False)
    plano = relationship("Plano")
    modalidades = relationship("Modalidade", secondary=cadastro_modalidade)
