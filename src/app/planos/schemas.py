from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class PlanoBase(BaseModel):
    nome: str
    descricao: str | None = None
    preco: Decimal
    duracao_dias: int = Field(default=30, gt=0)

class PlanoCreate(PlanoBase):
    pass

class PlanoOut(PlanoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class PlanoUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    preco: Decimal | None = None
    duracao_dias: int | None = Field(default=None, gt=0)
