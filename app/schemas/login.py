from pydantic import BaseModel, ConfigDict, Field
 
class Login(BaseModel):
    model_config = ConfigDict(from_attributes=True)
 
    email: str = Field(..., json_schema_extra={"example": "admin@email.com"})
    senha: str = Field(..., json_schema_extra={"example": "123456"})