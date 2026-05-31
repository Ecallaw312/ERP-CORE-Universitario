from pydantic import BaseModel, Field

class Login(BaseModel):
    email: str = Field(
        ...,
        example="admin@email.com"
    )

    senha: str = Field(
        ...,
        example="123456"
    )

    class Config:
        from_attributes = True