from sqlalchemy.orm import Session

from app.planos import models, schemas

def criar_plano(db: Session, plano: schemas.PlanoCreate):
    novo = models.Plano(**plano.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def listar_planos(db: Session):
    return db.query(models.Plano).all()

def buscar_plano(db: Session, plano_id: int):
    return db.query(models.Plano).filter(models.Plano.id == plano_id).first()

def atualizar_plano(db: Session, plano_id: int, dados: schemas.PlanoUpdate):
    plano = buscar_plano(db, plano_id)
    if plano is None:
        return None
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(plano, campo, valor)
    db.commit()
    db.refresh(plano)
    return plano

def deletar_plano(db: Session, plano_id: int):
    plano = buscar_plano(db, plano_id)
    if plano is None:
        return False
    db.delete(plano)
    db.commit()
    return True

def plano_em_uso(db: Session, plano_id: int):
    from app.cadastros import models as cadastros_models
    return db.query(cadastros_models.Cadastro).filter(cadastros_models.Cadastro.plano_id == plano_id).first() is not None

def buscar_plano_por_nome(db: Session, nome: str):
    return db.query(models.Plano).filter(models.Plano.nome == nome).first()
