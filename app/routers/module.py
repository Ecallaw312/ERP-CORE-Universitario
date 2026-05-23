from fastapi import APIRouter

router = APIRouter(prefix="/modules", tags=["Modules"])

@router.post("/")
def create_module():
    return {"message": "Module created successfully"}


@router.get("/")
def list_modules():
    return {"message": "List of modules"}