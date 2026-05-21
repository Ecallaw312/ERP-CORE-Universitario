from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column( "id", Integer, primary_key=True, autoincrement=True)
    nome = Column( "nome", String)
    email = Column( "email", String, unique=True, index=True)
    senha_hash = Column( "senha_hash", String)
    perfil = Column( "perfil", String)  # admin ou user
    ativo = Column( "ativo", Boolean, default=True)
    criado_em = Column( "criado_em", DateTime, default=datetime.utcnow)

    def __init__(self, nome, email, senha_hash, perfil="user"):
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash
        self.perfil = perfil
        
        