from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["users"])

@router.get("/")        # Somente Admin
def list_users():
    return {"message": "List of users"}   

@router.get("/users/{id}/status")      # Ativar ou desativar usuário
def user_status(id: int):
    return {"message": f"User {id} status updated successfully"}