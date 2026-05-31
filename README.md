# 📦 ERP CORE — Sistema ERP Distribuído

Disciplina de Sistemas Distribuídos — UNILAGO 2026

O **CORE** é o serviço central de um ERP distribuído baseado em microsserviços. Ele é responsável por autenticar usuários, controlar permissões, gerenciar módulos e monitorar a disponibilidade dos serviços conectados.

---

## 🚀 Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Framework | FastAPI + Uvicorn |
| Banco de dados | SQLAlchemy + SQLite (dev) / PostgreSQL (produção) |
| Migrações | Alembic |
| Autenticação | JWT (python-jose) + OAuth2 |
| Segurança | Passlib + bcrypt |
| Testes | Pytest + pytest-cov + httpx (TestClient) |
| Validação | Pydantic v2 |

---

## 📁 Estrutura do Projeto

```
app/
├── core/
│   ├── database.py       # Engine e Base SQLAlchemy
│   ├── dependencia.py    # get_db e verificar_token
│   └── security.py       # JWT, bcrypt, OAuth2
│
├── models/
│   ├── user.py
│   ├── module.py
│   └── refresh_token.py
│
├── schemas/
│   ├── user.py
│   ├── login.py
│   └── module.py
│
├── routers/
│   ├── auth.py           # /auth/*
│   ├── users.py          # /users/*
│   ├── module.py         # /modulos/*
│   └── health.py         # /health
│
└── main.py

teste/
├── conftest.py           # Banco em memória, fixtures
├── test_auth.py
├── test_admin.py
└── test_health.py

alembic/                  # Migrações de banco
seed.py                   # Dados iniciais
AUTH_CONTRACT.md          # Contrato de autenticação para frontend e módulos
```

---

## ⚙️ Como Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/Ecallaw312/ERP-CORE-Universitario.git
cd erp-core
```

### 2. Criar e ativar ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz:

```env
SECRET_KEY=erp_core_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
DATABASE_URL=sqlite:///./core.db
```

Para produção, substitua `DATABASE_URL` por:
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/erp_core
```

### 5. Executar migrações

**Windows PowerShell:**
```powershell
$env:DATABASE_URL = "sqlite:///./core.db"
alembic upgrade head
```

**Windows CMD:**
```cmd
set DATABASE_URL=sqlite:///./core.db
alembic upgrade head
```

**Linux/Mac:**
```bash
DATABASE_URL=sqlite:///./core.db alembic upgrade head
```

### 6. Popular banco com dados iniciais (opcional)

```bash
python seed.py
```

Usuários criados:

| Perfil     | Email | Senha  |
|------------|-------|-------|
| admin | admin@erp.com | 12345 |
| user  | user@erp.com  | 12345 |

Módulos criados:

| Nome       | Porta |
|------------|-------|
| Financeiro | 8001  |
| Estoque    | 8002  |
| RH         | 8003  |

### 7. Iniciar o servidor

```bash
uvicorn app.main:app --reload
```

Acesse a documentação interativa em: `http://127.0.0.1:8000/docs`

---

## 📌 Endpoints

### Auth
| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| POST | `/auth/register` | Cadastrar usuário | ❌ |
| POST | `/auth/login` | Login (retorna JWT) | ❌ |
| POST | `/auth/verify` | Verificar token | ✅ |
| POST | `/auth/refresh` | Renovar access token | ✅ |

### Usuários
| Método | Rota | Descrição | Perfil |
|--------|------|-----------|--------|
| GET | `/users` | Listar usuários | admin |
| PATCH | `/users/{id}/status` | Ativar/desativar usuário | admin |

### Módulos
| Método | Rota | Descrição | Perfil |
|--------|------|-----------|--------|
| POST | `/modulos/create` | Registrar módulo | admin |
| GET | `/modulos/list` | Listar módulos | admin |

### Sistema
| Método | Rota | Descrição | Auth |
|--------|------|-----------|------|
| GET | `/health` | Status dos serviços | ❌ |

---

## 🩺 Health Check

O endpoint `/health` verifica automaticamente a disponibilidade de todos os módulos cadastrados:

```json
{
  "status": "ok",
  "services": {
    "core": "online",
    "financeiro": "online",
    "estoque": "offline"
  }
}
```

`status` retorna `"ok"` quando todos os serviços estão online, ou `"degraded"` quando algum está inacessível.

---

## 🧪 Testes

```bash
# Executar todos os testes
python -m pytest

# Com relatório de cobertura
python -m pytest --cov=app --cov-report=term-missing
```

**Cobertura atual: 93%**

Os testes usam banco SQLite em memória — nenhuma configuração adicional necessária.

---

## 🌐 CORS

Configurado para aceitar requisições do frontend em:
```
http://localhost:3000
```

---

## 🔐 Contrato de Autenticação

Consulte o arquivo [`AUTH_CONTRACT.md`](./AUTH_CONTRACT.md) para a documentação completa de como o frontend e os outros módulos devem se integrar com o CORE.

---

## 👨‍💻 Integrantes

- Wallace Souza
- Wallison Souza
- Gabriel Mendes
- Felipe Magalhães
- Pedro Neto

---
