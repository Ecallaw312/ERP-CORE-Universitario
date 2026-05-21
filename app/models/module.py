from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database import Base

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column( "nome", String)
    url = Column( "url", String, nullable=True)
    porta = Column( "porta", Integer, nullable=True, unique=True)
    ativo = Column( "ativo", Boolean, default=True)
    criado_em = Column( "criado_em", DateTime, default=datetime.utcnow)