import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base
from app.core.dependencia import get_db

# SQLite em memória com conexão compartilhada — necessário para que
# create_all e as queries do app enxerguem as mesmas tabelas.
DATABASE_URL_TEST = "sqlite:///:memory:"

engine_test = create_engine(
    DATABASE_URL_TEST,
    connect_args={"check_same_thread": False},
)

# Mantém UMA conexão única durante os testes para o banco em memória não sumir
_conn = engine_test.connect()

TestingSessionLocal = sessionmaker(
    bind=_conn, autoflush=False, autocommit=False
)


def override_get_db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """Cria as tabelas antes de cada teste e limpa depois."""
    Base.metadata.create_all(bind=_conn)
    yield
    Base.metadata.drop_all(bind=_conn)


@pytest.fixture(scope="function")
def client(setup_db):
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ── Fixtures de conveniência ──────────────────────────────────────────────────

@pytest.fixture
def usuario_admin(client):
    """Cria e retorna dados de login do admin."""
    client.post("/auth/register", json={
        "nome": "Admin Teste",
        "email": "admin@teste.com",
        "senha": "senha123",
        "perfil": "admin"
    })
    resp = client.post("/auth/login", json={
        "email": "admin@teste.com",
        "senha": "senha123"
    })
    return resp.json()


@pytest.fixture
def usuario_comum(client):
    """Cria e retorna dados de login do usuário comum."""
    client.post("/auth/register", json={
        "nome": "User Teste",
        "email": "user@teste.com",
        "senha": "senha123",
        "perfil": "user"
    })
    resp = client.post("/auth/login", json={
        "email": "user@teste.com",
        "senha": "senha123"
    })
    return resp.json()


@pytest.fixture
def headers_admin(usuario_admin):
    return {"Authorization": f"Bearer {usuario_admin['access_token']}"}


@pytest.fixture
def headers_user(usuario_comum):
    return {"Authorization": f"Bearer {usuario_comum['access_token']}"}
