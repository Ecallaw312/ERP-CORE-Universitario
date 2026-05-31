"""
Testes de gerenciamento de usuários e módulos.
Cobre: listar, atualizar status, regras de acesso por perfil.
"""


# ── /users ────────────────────────────────────────────────────────────────────

def test_listar_usuarios_admin(client, headers_admin):
    resp = client.get("/users", headers=headers_admin)
    assert resp.status_code == 200
    assert "usuarios" in resp.json()


def test_listar_usuarios_sem_token(client):
    resp = client.get("/users")
    assert resp.status_code == 401


def test_listar_usuarios_perfil_user_negado(client, headers_user):
    """Usuário comum não pode listar usuários."""
    resp = client.get("/users", headers=headers_user)
    assert resp.status_code == 403


def test_listar_usuarios_retorna_lista(client, headers_admin):
    """Admin criado pela fixture deve aparecer na listagem."""
    resp = client.get("/users", headers=headers_admin)
    assert resp.status_code == 200
    usuarios = resp.json()["usuarios"]
    assert isinstance(usuarios, list)
    assert len(usuarios) >= 1


# ── /users/{id}/status ────────────────────────────────────────────────────────

def test_atualizar_status_usuario(client, usuario_admin, headers_admin):
    """Admin deve conseguir desativar/reativar um usuário."""
    user_id = usuario_admin["user"]["id"]
    resp = client.patch(f"/users/{user_id}/status", headers=headers_admin)
    assert resp.status_code == 200
    assert "message" in resp.json()


def test_atualizar_status_usuario_inexistente(client, headers_admin):
    resp = client.patch("/users/99999/status", headers=headers_admin)
    assert resp.status_code == 404


def test_atualizar_status_perfil_user_negado(client, usuario_admin, headers_user):
    """Usuário comum não pode alterar status."""
    user_id = usuario_admin["user"]["id"]
    resp = client.patch(f"/users/{user_id}/status", headers=headers_user)
    assert resp.status_code == 403


def test_toggle_status_ativa_desativa(client, usuario_admin, headers_admin):
    """Dois PATCHs consecutivos devem alternar o status."""
    user_id = usuario_admin["user"]["id"]
    r1 = client.patch(f"/users/{user_id}/status", headers=headers_admin)
    r2 = client.patch(f"/users/{user_id}/status", headers=headers_admin)
    assert r1.status_code == 200
    assert r2.status_code == 200
    # As mensagens devem ser diferentes (desativado / ativado)
    assert r1.json()["message"] != r2.json()["message"]


# ── /modulos ──────────────────────────────────────────────────────────────────

MODULO_PAYLOAD = {
    "nome": "Financeiro",
    "url": "http://localhost",
    "porta": 8001
}


def test_criar_modulo_admin(client, headers_admin):
    resp = client.post("/modulos/create", json=MODULO_PAYLOAD, headers=headers_admin)
    assert resp.status_code == 200
    assert "criado com sucesso" in resp.json()["message"]


def test_criar_modulo_duplicado(client, headers_admin):
    client.post("/modulos/create", json=MODULO_PAYLOAD, headers=headers_admin)
    resp = client.post("/modulos/create", json=MODULO_PAYLOAD, headers=headers_admin)
    assert resp.status_code == 400


def test_criar_modulo_perfil_user_negado(client, headers_user):
    resp = client.post("/modulos/create", json=MODULO_PAYLOAD, headers=headers_user)
    assert resp.status_code == 403


def test_criar_modulo_sem_token(client):
    resp = client.post("/modulos/create", json=MODULO_PAYLOAD)
    assert resp.status_code == 401


def test_listar_modulos_admin(client, headers_admin):
    client.post("/modulos/create", json=MODULO_PAYLOAD, headers=headers_admin)
    resp = client.get("/modulos/list", headers=headers_admin)
    assert resp.status_code == 200
    assert "modules" in resp.json()
    assert len(resp.json()["modules"]) == 1


def test_listar_modulos_perfil_user_negado(client, headers_user):
    resp = client.get("/modulos/list", headers=headers_user)
    assert resp.status_code == 403
