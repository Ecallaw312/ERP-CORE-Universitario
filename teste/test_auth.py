"""
Testes do módulo de autenticação.
Cobre: register, login, verify, refresh, regras de negócio.
"""


# ── /auth/register ────────────────────────────────────────────────────────────

def test_register_sucesso(client):
    resp = client.post("/auth/register", json={
        "nome": "João Silva",
        "email": "joao@teste.com",
        "senha": "senha123",
        "perfil": "user"
    })
    assert resp.status_code == 200
    assert "registrado com sucesso" in resp.json()["message"]


def test_register_email_duplicado(client):
    payload = {"nome": "A", "email": "dup@teste.com", "senha": "123", "perfil": "user"}
    client.post("/auth/register", json=payload)
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 400


def test_register_perfil_padrao_user(client):
    """Sem informar perfil, deve assumir 'user'."""
    resp = client.post("/auth/register", json={
        "nome": "Sem Perfil",
        "email": "semperfil@teste.com",
        "senha": "123"
    })
    assert resp.status_code == 200


# ── /auth/login ───────────────────────────────────────────────────────────────

def test_login_sucesso(client):
    client.post("/auth/register", json={
        "nome": "Login User",
        "email": "login@teste.com",
        "senha": "senha123",
        "perfil": "user"
    })
    resp = client.post("/auth/login", json={
        "email": "login@teste.com",
        "senha": "senha123"
    })
    assert resp.status_code == 200
    data = resp.json()
    # Campos obrigatórios para o frontend
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert "id" in data["user"]
    assert "nome" in data["user"]
    assert "email" in data["user"]
    assert "perfil" in data["user"]


def test_login_email_inexistente(client):
    resp = client.post("/auth/login", json={
        "email": "naoexiste@teste.com",
        "senha": "qualquer"
    })
    assert resp.status_code == 403


def test_login_senha_errada(client):
    client.post("/auth/register", json={
        "nome": "X",
        "email": "x@teste.com",
        "senha": "correta",
        "perfil": "user"
    })
    resp = client.post("/auth/login", json={
        "email": "x@teste.com",
        "senha": "errada"
    })
    assert resp.status_code == 403


# ── /auth/verify ──────────────────────────────────────────────────────────────

def test_verify_token_valido(client, headers_user):
    resp = client.post("/auth/verify", headers=headers_user)
    assert resp.status_code == 200
    assert "user" in resp.json()


def test_verify_token_invalido(client):
    resp = client.post("/auth/verify", headers={"Authorization": "Bearer token_invalido"})
    assert resp.status_code == 401


def test_verify_sem_token(client):
    resp = client.post("/auth/verify")
    assert resp.status_code == 401


# ── /auth/refresh ─────────────────────────────────────────────────────────────

def test_refresh_token_valido(client, headers_user):
    resp = client.post("/auth/refresh", headers=headers_user)
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalido(client):
    resp = client.post("/auth/refresh", headers={"Authorization": "Bearer lixo"})
    assert resp.status_code == 401
