from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.cadastros import crud, schemas
from app.planos import crud as planos_crud
from app.modalidades import crud as modalidades_crud

router = APIRouter(prefix="/cadastros", tags=["Cadastros"])

@router.post("/", response_model=schemas.CadastroOut)
def criar(dados: schemas.CadastroCreate, db: Session = Depends(get_db)):
    if planos_crud.buscar_plano(db, dados.plano_id) is None:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    ids = list(set(dados.modalidades_ids))
    modalidades = modalidades_crud.buscar_modalidades_por_ids(db, ids)
    if len(modalidades) != len(ids):
        raise HTTPException(status_code=400, detail="Modalidade inválida")

    return crud.criar_cadastro(db, dados, modalidades)

@router.get("/", response_model=list[schemas.CadastroOut])
def listar(db: Session = Depends(get_db)):
    return crud.listar_cadastros(db)

@router.get("/protocolo/{protocolo}", response_model=schemas.CadastroOut)
def buscar_por_protocolo(protocolo: str, db: Session = Depends(get_db)):
    cadastro = crud.buscar_cadastro_por_protocolo(db, protocolo)
    if cadastro is None:
        raise HTTPException(status_code=404, detail="Cadastro não encontrado")
    return cadastro

@router.get("/{cadastro_id}", response_model=schemas.CadastroOut)
def buscar(cadastro_id: int, db: Session = Depends(get_db)):
    cadastro = crud.buscar_cadastro(db, cadastro_id)
    if cadastro is None:
        raise HTTPException(status_code=404, detail="Cadastro não encontrado")
    return cadastro

@router.delete("/{cadastro_id}", status_code=204)
def deletar(cadastro_id: int, db: Session = Depends(get_db)):
    if not crud.deletar_cadastro(db, cadastro_id):
        raise HTTPException(status_code=404, detail="Cadastro não encontrado")

@router.patch("/{cadastro_id}/ativacao", response_model=schemas.CadastroOut)
def ativar(cadastro_id: int, dados: schemas.CadastroAtivacao, db: Session = Depends(get_db)):
    cadastro = crud.ativar_cadastro(db, cadastro_id, dados)
    if cadastro is None:
        raise HTTPException(status_code=404, detail="Cadastro não encontrado")
    return cadastro