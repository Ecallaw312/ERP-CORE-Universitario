"""
Testes do endpoint de health check.
Cobre: resposta básica, estrutura do JSON, módulos sem cadastro.
"""


def test_health_retorna_200(client):
    resp = client.get("/health")
    assert resp.status_code == 200


def test_health_estrutura_resposta(client):
    resp = client.get("/health")
    data = resp.json()
    assert "status" in data
    assert "services" in data
    assert "core" in data["services"]
    assert data["services"]["core"] == "online"


def test_health_sem_modulos_status_ok(client):
    """Sem módulos cadastrados, core está online → status deve ser 'ok'."""
    resp = client.get("/health")
    assert resp.json()["status"] == "ok"


def test_health_com_modulo_offline(client, headers_admin):
    """Módulo cadastrado mas inacessível → status deve ser 'degraded'."""
    client.post("/modulos/create", json={
        "nome": "Fantasma",
        "url": "http://localhost",
        "porta": 19999  # porta que não existe
    }, headers=headers_admin)

    resp = client.get("/health")
    data = resp.json()
    assert data["status"] == "degraded"
    assert data["services"].get("Fantasma") == "offline"
