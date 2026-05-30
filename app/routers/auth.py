from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencia import get_db, verificar_token
from sqlalchemy.orm import Session
from app.core.security import hash_senha, verificar_senha, criar_token, criar_refresh_token
from app.models.user import User
from app.schemas.user import UserSchema
from app.schemas.login import LoginSchema
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(usuario_schemas: UserSchema, session: Session = Depends(get_db)):
    usuario = session.query(User).filter(User.email == usuario_schemas.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Credenciais inválidas ou já utilizadas.")
    else:
        senhacriptografada = hash_senha(usuario_schemas.senha)
        novo_usuario = User(email=usuario_schemas.email,
                             nome=usuario_schemas.nome, 
                             senha=senhacriptografada,
                             perfil=usuario_schemas.perfil
                             )
        session.add(novo_usuario)
        session.commit()
        return {"message": f"Usuário registrado com sucesso: {usuario_schemas.email}"}



@router.post("/login")
def login(login_schemas: LoginSchema, session: Session = Depends(get_db)):
    usuario = session.query(User).filter(User.email == login_schemas.email).first()
    if not usuario:
        raise HTTPException(status_code=403, detail="Credenciais inválidas")
    if not verificar_senha(login_schemas.senha, usuario.senha):
        raise HTTPException(status_code=403, detail="Credenciais inválidas")
    
    access_token = criar_token({"sub": str(usuario.id), "perfil": usuario.perfil})
    refresh_token = criar_refresh_token({"sub": str(usuario.id), "perfil": usuario.perfil})
    return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer",
    "user": {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil
    }}

@router.post("/login_formulario")
def login(login_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    usuario = session.query(User).filter(User.email == login_formulario.username).first()
    if not usuario:
        raise HTTPException(status_code=403, detail="Credenciais inválidas")
    if not verificar_senha(login_formulario.password, usuario.senha):
        raise HTTPException(status_code=403, detail="Credenciais inválidas")
    
    access_token = criar_token({"sub": str(usuario.id), "perfil": usuario.perfil})
    return {
    "access_token": access_token,
    "token_type": "bearer",
    }


@router.get("/refresh")
def refresh_token(usuario: User = Depends(verificar_token)):
    
    access_token = criar_token({"sub": str(usuario.id), "perfil": usuario.perfil})

    return {
    "access_token": access_token,
    # "refresh_token": refresh_token,
    "token_type": "bearer",
    "user": {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil
    }}

