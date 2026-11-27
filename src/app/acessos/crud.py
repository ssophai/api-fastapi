from datetime import date
from sqlalchemy.orm import Session

from app.acessos import models
from app.cadastros import crud as cadastros_crud

def validar_acesso(db: Session, protocolo: str):
    protocolo = protocolo.strip().upper()
    cadastro = cadastros_crud.buscar_cadastro_por_protocolo(db, protocolo)

    if cadastro is None:
        liberado, motivo = False, "Protocolo não encontrado"
    elif not cadastro.ativo:
        liberado, motivo = False, "Cadastro inativo"
    elif cadastro.data_validade is None or cadastro.data_validade < date.today():
        liberado, motivo = False, "Plano vencido"
    else:
        liberado, motivo = True, "Acesso liberado"

    registro = models.Acesso(
        protocolo=protocolo,
        liberado=liberado,
        motivo=motivo,
        cadastro_id=cadastro.id if cadastro else None,
    )
    db.add(registro)
    db.commit()
    return liberado, motivo, (cadastro.nome if cadastro else None)

def listar_acessos(db: Session):
    return db.query(models.Acesso).order_by(models.Acesso.id.desc()).all()