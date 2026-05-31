from pydantic import BaseModel, ConfigDict, Field
 
class Modulo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
 
    nome: str = Field(..., json_schema_extra={"example": "Financeiro"})
    url: str = Field(..., json_schema_extra={"example": "http://localhost:8001"})
    porta: int = Field(..., json_schema_extra={"example": 8001})
 