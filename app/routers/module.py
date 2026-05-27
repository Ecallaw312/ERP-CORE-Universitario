from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencia import get_db
from app.schemas.module import ModuleSchema
from app.models.module import Module

router = APIRouter(prefix="/modules", tags=["Modules"])

@router.post("/create")
def create_module(moduleschemas: ModuleSchema, session: Session = Depends(get_db)):
    module = session.query(Module).filter(Module.nome == moduleschemas.nome, 
                                          Module.url == moduleschemas.url,
                                          Module.porta == moduleschemas.porta).first()
    if module:
        raise HTTPException(status_code=400, detail="Module já existe")
    else:
        module = Module(nome=moduleschemas.nome, url=moduleschemas.url, porta=moduleschemas.porta)
        session.add(module)
        session.commit()
        return {"message": "Module criado com sucesso"}


@router.get("/list")
def list_modules(session: Session = Depends(get_db)):
    modules = session.query(Module).all()
    return {"modules": modules}