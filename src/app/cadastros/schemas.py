from datetime import datetime, date
from pydantic import BaseModel, ConfigDict, field_validator

from app.planos.schemas import PlanoOut
from app.modalidades.schemas import ModalidadeOut

class CadastroCreate(BaseModel):
    nome: str
    telefone: str
    email: str | None = None
    objetivo: str | None = None
    observacoes: str | None = None
    plano_id: int
    modalidades_ids: list[int] = []

    @field_validator("telefone")
    @classmethod
    def validar_telefone(cls, valor: str):
        digitos = "".join(c for c in valor if c.isdigit())
        if len(digitos) not in (10, 11):
            raise ValueError("Telefone inválido: informe DDD + número (10 ou 11 dígitos)")
        return digitos

class CadastroOut(BaseModel):
    id: int
    protocolo: str
    nome: str
    telefone: str
    email: str | None
    objetivo: str | None
    observacoes: str | None
    criado_em: datetime
    plano: PlanoOut
    modalidades: list[ModalidadeOut]
    ativo: bool
    data_validade: date | None
    model_config = ConfigDict(from_attributes=True)

class CadastroAtivacao(BaseModel):
    ativo: bool
    data_validade: date | None = None