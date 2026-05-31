from pydantic import BaseModel, Field

class Modulo(BaseModel):
    nome: str = Field(
        ...,
        example="Financeiro"
    )

    url: str = Field(
        ...,
        example="http://localhost:8001"
    )

    porta: int = Field(
        ...,
        example=8001
    )

    class Config:
        from_attributes = True