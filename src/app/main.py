
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.planos import models as planos_models
from app.modalidades import models as modalidades_models
from app.cadastros import models as cadastros_models
from app.planos.router import router as planos_router
from app.modalidades.router import router as modalidades_router
from app.cadastros.router import router as cadastros_router
from app.acessos import models as acessos_models
from app.acessos.router import router as acessos_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(planos_router)
app.include_router(modalidades_router)
app.include_router(cadastros_router)
app.include_router(acessos_router)


@app.get("/")
def inicio():
    return {"mensagem": "socorro!"}