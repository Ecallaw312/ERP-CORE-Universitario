from pydantic import BaseModel
from typing import Optional, Literal

class UserSchema(BaseModel):
    name: str
    email: str
    senha: str
    perfil: Literal["admin", "user"] = "user"
    class Config:
        from_attributes = True