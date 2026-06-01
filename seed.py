"""
Seed — popula o banco com usuários e módulos iniciais.
Execute após rodar as migrações: python seed.py
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./core.db")

# Ajusta o driver para PostgreSQL
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

from app.core.security import hash_senha
from app.models.user import User_db
from app.models.module import Modulo_db


def seed():
    session = SessionLocal()

    try:
        # ── Usuários ──────────────────────────────────────────────────────────
        usuarios = [
            {"nome": "Administrador", "email": "admin@erp.com", "senha": "12345", "perfil": "admin"},
            {"nome": "Usuário Padrão", "email": "user@erp.com",  "senha": "12345", "perfil": "user"},
        ]

        for dados in usuarios:
            existe = session.query(User_db).filter(User_db.email == dados["email"]).first()
            if not existe:
                novo = User_db(
                    nome=dados["nome"],
                    email=dados["email"],
                    senha=hash_senha(dados["senha"]),
                    perfil=dados["perfil"],
                )
                session.add(novo)
                print(f"  [+] Usuário criado: {dados['email']} ({dados['perfil']})")
            else:
                print(f"  [=] Usuário já existe: {dados['email']}")

        # ── Módulos ───────────────────────────────────────────────────────────
        modulos = [
            {"nome": "Financeiro", "url": "http://localhost", "porta": 8001},
            {"nome": "Estoque",    "url": "http://localhost", "porta": 8002},
            {"nome": "RH",         "url": "http://localhost", "porta": 8003},
        ]

        for dados in modulos:
            existe = session.query(Modulo_db).filter(Modulo_db.nome == dados["nome"]).first()
            if not existe:
                novo = Modulo_db(
                    nome=dados["nome"],
                    url=dados["url"],
                    porta=dados["porta"],
                )
                session.add(novo)
                print(f"  [+] Módulo criado: {dados['nome']} (porta {dados['porta']})")
            else:
                print(f"  [=] Módulo já existe: {dados['nome']}")

        session.commit()
        print("\n✅ Seed concluído com sucesso!")

    except Exception as e:
        session.rollback()
        print(f"\n❌ Erro durante o seed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    print("🌱 Iniciando seed...\n")
    seed()
