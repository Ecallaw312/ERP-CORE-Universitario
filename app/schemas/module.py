from pydantic import BaseModel

class ModuleSchema(BaseModel):
    nome: str
    url: str
    porta: int
    class Config:
        from_attributes = True