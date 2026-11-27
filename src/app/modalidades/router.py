from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.modalidades import crud, schemas

router = APIRouter(prefix="/modalidades", tags=["Modalidades"])

@router.post("/", response_model=schemas.ModalidadeOut)
def criar(modalidade: schemas.ModalidadeCreate, db: Session = Depends(get_db)):
    if crud.buscar_modalidade_por_nome(db, modalidade.nome):
        raise HTTPException(status_code=409, detail="Já existe uma modalidade com esse nome")
    return crud.criar_modalidade(db, modalidade)

@router.get("/", response_model=list[schemas.ModalidadeOut])
def listar(db: Session = Depends(get_db)):
    return crud.listar_modalidades(db)

@router.get("/{modalidade_id}", response_model=schemas.ModalidadeOut)
def buscar(modalidade_id: int, db: Session = Depends(get_db)):
    modalidade = crud.buscar_modalidade(db, modalidade_id)
    if modalidade is None:
        raise HTTPException(status_code=404, detail="Modalidade não encontrada")
    return modalidade

@router.patch("/{modalidade_id}", response_model=schemas.ModalidadeOut)
def atualizar(modalidade_id: int, dados: schemas.ModalidadeUpdate, db: Session = Depends(get_db)):
    if dados.nome is not None:
        existente = crud.buscar_modalidade_por_nome(db, dados.nome)
        if existente and existente.id != modalidade_id:
            raise HTTPException(status_code=409, detail="Já existe uma modalidade com esse nome")
    modalidade = crud.atualizar_modalidade(db, modalidade_id, dados)
    if modalidade is None:
        raise HTTPException(status_code=404, detail="Modalidade não encontrada")
    return modalidade

@router.delete("/{modalidade_id}", status_code=204)
def deletar(modalidade_id: int, db: Session = Depends(get_db)):
    if crud.buscar_modalidade(db, modalidade_id) is None:
        raise HTTPException(status_code=404, detail="Modalidade não encontrada")
    if crud.modalidade_em_uso(db, modalidade_id):
        raise HTTPException(status_code=409, detail="Modalidade em uso por cadastros e não pode ser apagada")
    crud.deletar_modalidade(db, modalidade_id)
