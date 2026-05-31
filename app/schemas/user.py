from pydantic import BaseModel, ConfigDict, Field
from typing import Literal
 
class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
 
    nome: str = Field(
        ...,
        json_schema_extra={"example": "João Silva"},
        description="Nome completo do usuário"
    )
    email: str = Field(
        ...,
        json_schema_extra={"example": "joao@email.com"},
        description="E-mail utilizado para login"
    )
    senha: str = Field(
        ...,
        json_schema_extra={"example": "123456"},
        description="Senha do usuário"
    )
    perfil: Literal["admin", "user"] = Field(
        default="user",
        json_schema_extra={"example": "user"},
        description="Perfil de acesso do usuário"
    )