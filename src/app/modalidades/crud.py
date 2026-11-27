from sqlalchemy.orm import Session

from app.modalidades import models, schemas

def criar_modalidade(db: Session, modalidade: schemas.ModalidadeCreate):
    nova = models.Modalidade(**modalidade.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

def listar_modalidades(db: Session):
    return db.query(models.Modalidade).all()

def buscar_modalidade(db: Session, modalidade_id: int):
    return db.query(models.Modalidade).filter(models.Modalidade.id == modalidade_id).first()

def atualizar_modalidade(db: Session, modalidade_id: int, dados: schemas.ModalidadeUpdate):
    modalidade = buscar_modalidade(db, modalidade_id)
    if modalidade is None:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(modalidade, campo, valor)
    db.commit()
    db.refresh(modalidade)
    return modalidade

def deletar_modalidade(db: Session, modalidade_id: int):
    modalidade = buscar_modalidade(db, modalidade_id)
    if modalidade is None:
        return False
    db.delete(modalidade)
    db.commit()
    return True

def buscar_modalidades_por_ids(db: Session, ids: list[int]):
    if not ids:
        return []
    return db.query(models.Modalidade).filter(models.Modalidade.id.in_(ids)).all()

def modalidade_em_uso(db: Session, modalidade_id: int):
    from app.cadastros import models as cadastros_models
    return (
        db.query(cadastros_models.Cadastro)
        .filter(cadastros_models.Cadastro.modalidades.any(models.Modalidade.id == modalidade_id))
        .first()
        is not None
    )

def buscar_modalidade_por_nome(db: Session, nome: str):
    return db.query(models.Modalidade).filter(models.Modalidade.nome == nome).first()
