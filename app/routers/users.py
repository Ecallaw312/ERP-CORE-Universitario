from fastapi import APIRouter

router = APIRouter(tags=["users"])
# Somente Admin
@router.get("/users")        
def list_users():
    return {"message": "List of users"}   
# Somente Admin
@router.get("/users/{id}/status")      # Ativar ou desativar usuário
def user_status(id: int):
    return {"message": f"User {id} status updated successfully"}