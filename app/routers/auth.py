from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencia import get_db
from sqlalchemy.orm import Session
from app.core.security import bcrypt_context
from app.models.user import User
from app.schemas.user import UserSchema


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(usuario_schemas: UserSchema, session: Session = Depends(get_db)):
    usuario = session.query(User).filter(User.email == usuario_schemas.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email do usuário já cadastrado")
    else:
        senhacriptografada = bcrypt_context.hash(usuario_schemas.senha)
        novo_usuario = User(email=usuario_schemas.email,
                             nome=usuario_schemas.nome, 
                             senha=senhacriptografada,
                             perfil=usuario_schemas.perfil
                             )
        session.add(novo_usuario)
        session.commit()
        return {"message": f"Usuário registrado com sucesso: {usuario_schemas.email}"}



@router.post("/login")
def login():
    return {"message": "Usuário logado com sucesso"}


@router.post("/refresh")
def refresh():
    return {"message": "Token refreshed successfully"}

@router.get("/verify")
def verify():
    return {"message": "Usuário verificado com sucesso"}

# @router.get("/private")
# def private():
#     return {"message": "This is a private route"}