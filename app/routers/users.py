from fastapi import APIRouter
from fastapi import Depends,HTTPException
from app.models.user import User_db
from app.core.dependencia import verificar_token, get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["users"])
# Somente Admin
@router.get("/users")        
async def list_users(usuario: User_db = Depends(verificar_token), session: Session = Depends(get_db)):
    if not usuario or usuario.perfil != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado, somente administradores podem acessar esta rota.")
    
    usuarios = session.query(User_db).all()
    return {"usuarios": [
                {"id": user.id, 
                 "nome": user.nome, 
                 "email": user.email, 
                 "perfil": user.perfil, 
                 "ativo": user.ativo,
                 "data_criacao": user.criado_em.isoformat()} 
                 for user in usuarios]}

# Somente Admin
@router.patch("/users/{id}/status")      # Ativar ou desativar usuário
async def user_status(id: int, usuario: User_db = Depends(verificar_token), session: Session = Depends(get_db)):
    if not usuario or usuario.perfil != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado, somente administradores podem acessar esta rota.")  
    
    user = session.query(User_db).filter(User_db.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    
    user.ativo = not user.ativo
    session.commit()

    status = "ativado" if user.ativo else "desativado"
    return {"message": f"Usuário {user.nome} {status} com sucesso."}