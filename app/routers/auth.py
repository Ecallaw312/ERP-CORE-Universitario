from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencia import get_db, verificar_token
from sqlalchemy.orm import Session
from app.core.security import hash_senha, verificar_senha, criar_token, criar_refresh_token
from app.models.user import User_db
from app.schemas.user import User
from app.schemas.login import Login
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(usuario: User, session: Session = Depends(get_db)):
    usuario_resposta = session.query(User_db).filter(User_db.email == usuario.email).first()
    if usuario_resposta:
        raise HTTPException(status_code=400, detail="Credenciais inválidas ou já utilizadas.")
    else:
        senhacriptografada = hash_senha(usuario.senha)
        novo_usuario = User_db(email=usuario.email,
                             nome=usuario.nome, 
                             senha=senhacriptografada,
                             perfil=usuario.perfil
                             )
        session.add(novo_usuario)
        session.commit()
        return {"message": f"Usuário registrado com sucesso: {usuario.email}"}

@router.post("/login")
async def login(login: Login, session: Session = Depends(get_db)):
    usuario_resposta = session.query(User_db).filter(User_db.email == login.email).first()
    if not usuario_resposta:
        raise HTTPException(status_code=403, detail="Credenciais inválidas")
    if not verificar_senha(login.senha, usuario_resposta.senha):
        raise HTTPException(status_code=403, detail="Credenciais inválidas")
    
    access_token = criar_token({"sub": str(usuario_resposta.id), "perfil": usuario_resposta.perfil})
    refresh_token = criar_refresh_token({"sub": str(usuario_resposta.id), "perfil": usuario_resposta.perfil})
    return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer",
    "user": {
        "id": usuario_resposta.id,
        "nome": usuario_resposta.nome,
        "email": usuario_resposta.email,
        "perfil": usuario_resposta.perfil
    }}

@router.post("/login_formulario")
async def login(login_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db)):
    usuario_resposta = session.query(User_db).filter(User_db.email == login_formulario.username).first()
    if not usuario_resposta:
        raise HTTPException(status_code=403, detail="Credenciais inválidas")
    if not verificar_senha(login_formulario.password, usuario_resposta.senha):
        raise HTTPException(status_code=403, detail="Credenciais inválidas")
    
    access_token = criar_token({"sub": str(usuario_resposta.id), "perfil": usuario_resposta.perfil})
    return {
    "access_token": access_token,
    "token_type": "bearer",
    }


@router.post("/refresh")
async def refresh_token(usuario: User_db = Depends(verificar_token)):
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")
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

@router.post("/verify")
async def verify_token(usuario: User_db = Depends(verificar_token)):
    return {
        "menssagem": "Token válido",
        "user": {
            "nome": usuario.nome, 
            "perfil": usuario.perfil
        }
    }