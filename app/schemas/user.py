# from pydantic import BaseModel
# from typing import Optional, Literal

# class User(BaseModel):
#     nome: str
#     email: str
#     senha: str
#     perfil: Literal["admin", "user"] = "user"
#     class Config:
#         from_attributes = True



from pydantic import BaseModel, Field
from typing import Literal

class User(BaseModel):
    nome: str = Field(
        ...,
        example="João Silva",
        description="Nome completo do usuário"
    )

    email: str = Field(
        ...,
        example="joao@email.com",
        description="E-mail utilizado para login"
    )

    senha: str = Field(
        ...,
        example="123456",
        description="Senha do usuário"
    )

    perfil: Literal["admin", "user"] = Field(
        default="user",
        example="user",
        description="Perfil de acesso do usuário"
    )

    class Config:
        from_attributes = True