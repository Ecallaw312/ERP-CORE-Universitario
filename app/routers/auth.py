from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencia import get_db
from app.models.user import User
from app.core.security import bcrypt_context


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(email: str, nome: str, senha: str, session = Depends(get_db)):
    usuario = session.query(User).filter(User.email == email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email do usuário já cadastrado")
    else:
        senhacriptografada = bcrypt_context.hash(senha)
        novo_usuario = User(email=email, nome=nome, senha=senhacriptografada)
        session.add(novo_usuario)
        session.commit()
        return {"message": f"Usuário registrado com sucesso: {email}"}



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