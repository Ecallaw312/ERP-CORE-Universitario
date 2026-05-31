from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencia import get_db, verificar_token
from app.schemas.module import Modulo
from app.models.module import Modulo_db
from app.models.user import User_db

router = APIRouter(prefix="/modulos", tags=["Modulos"])

# Somente Admin pode criar e listar os módulos

@router.post("/create")
async def create_module(modulo: Modulo, usuario: User_db = Depends(verificar_token), session: Session = Depends(get_db)):
    if not usuario or usuario.perfil != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado: Somente administrador")
    modulo_resposta = session.query(Modulo_db).filter(Modulo_db.nome == modulo.nome, 
                                                      Modulo_db.url == modulo.url,
                                                      Modulo_db.porta == modulo.porta).first()
    if modulo_resposta:
        raise HTTPException(status_code=400, detail="Modulo já existe")
    else:
        url_tratada = modulo.url.rstrip(":")
        modulo_resposta = Modulo_db(nome=modulo.nome, url=url_tratada, porta=modulo.porta)
        session.add(modulo_resposta)
        session.commit()
        return {"message": "Modulo criado com sucesso"}


@router.get("/list")
async def list_modules(session: Session = Depends(get_db), usuario: User_db = Depends(verificar_token)):
    if not usuario or usuario.perfil != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado: Somente administrador")
    modules = session.query(Modulo_db).all()
    return {"modules": modules}