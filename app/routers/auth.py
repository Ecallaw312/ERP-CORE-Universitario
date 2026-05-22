from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register():
    return {"message": "User registered successfully"}



@router.post("/login")
def login():
    return {"message": "User logged in successfully"}




@router.get("/verify")
def verify():
    return {"message": "User verified successfully"}



@router.get("/private")
def private():
    return {"message": "This is a private route"}



@router.post("/refresh")
def refresh():
    return {"message": "Token refreshed successfully"}
