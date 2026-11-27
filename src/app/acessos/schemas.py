from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AcessoValidar(BaseModel):
    protocolo: str

class AcessoResposta(BaseModel):
    liberado: bool
    motivo: str
    nome: str | None = None

class AcessoOut(BaseModel):
    id: int
    protocolo: str
    liberado: bool
    motivo: str
    data_hora: datetime
    cadastro_id: int | None

    model_config = ConfigDict(from_attributes=True)