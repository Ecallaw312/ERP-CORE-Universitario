# 📦 ERP CORE - Sistema ERP Distribuído

## 📌 Sobre o Projeto

Este projeto foi desenvolvido para a disciplina de Sistemas Distribuídos com o objetivo de criar o núcleo principal (CORE) de um sistema ERP distribuído.

O CORE é responsável por:

* autenticação de usuários
* autorização e controle de acesso
* gerenciamento de módulos
* monitoramento dos serviços conectados
* centralização da segurança da aplicação

O sistema foi desenvolvido utilizando FastAPI e arquitetura baseada em microsserviços.

---

# 🚀 Tecnologias Utilizadas

* Python 3.11+
* FastAPI
* SQLAlchemy
* SQLite
* JWT Authentication
* OAuth2
* Swagger/OpenAPI
* Passlib (bcrypt)
* Pytest
* Uvicorn
* Alembic


---

# 🏗️ Arquitetura do Projeto

O sistema segue uma arquitetura distribuída baseada em microsserviços.

O CORE funciona como serviço principal do ERP, sendo responsável pela autenticação e comunicação entre os módulos do sistema.

Os módulos podem se registrar no CORE e serem monitorados automaticamente através do sistema de Health Check.

---

# 📁 Estrutura do Projeto

```bash
app/
├── core/
│   ├── admin.py
│   ├── auth.py
│   ├── database.py
│   ├── deps.py
│   └── security.py
│
├── models/
│   ├── user.py
│   ├── module.py
│   └── refresh_token.py
│
├── schemas/
│   ├── user.py
│   ├── auth.py
│   └── module.py
│
├── routers/
│   ├── auth.py
│   ├── users.py
│   ├── module.py
│   └── health.py
│
└── main.py

tests/
├── test_admin.py
├── test_auth.py
├── test_health.py
└── test_module.py
```

---

# 🔐 Funcionalidades Implementadas

## 👤 Usuários

* Cadastro de usuários
* Login com JWT
* Controle de acesso por perfil
* Ativação e desativação de usuários
* Rotas protegidas

## 🔑 Autenticação

* OAuth2 Password Flow
* JWT Access Token
* Refresh Token
* Verificação de sessão
* Proteção de endpoints

## 🧩 Módulos

* Registro de módulos
* Listagem de módulos
* Integração entre serviços

## 🩺 Health Check

* Monitoramento dos módulos cadastrados
* Verificação automática de status
* Serviços online/offline
* Health Check agregado do sistema

## 🛡️ Segurança

* Senhas criptografadas com bcrypt
* Autenticação JWT
* Controle de permissões
* Rotas protegidas com Depends

---

# 📖 Documentação da API

Após iniciar o servidor, a documentação pode ser acessada em:

```txt
http://127.0.0.1:8000/docs
```

A documentação foi gerada automaticamente utilizando Swagger UI.

---

# ⚙️ Como Executar o Projeto

## 1️⃣ Clonar o repositório

```bash
git clone https://github.com/g4brielmendes/erp-core.git
```

---

## 2️⃣ Entrar na pasta do projeto

```bash
cd ERP-Core
```

---

## 3️⃣ Criar ambiente virtual

```bash
python -m venv venv
```

### Ativar ambiente virtual

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 4️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

---

## 5️⃣ Configurar variáveis de ambiente

Criar um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=erp_core_super_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

REFRESH_TOKEN_EXPIRE_DAYS=7
```
### 🗄️ Configuração do Banco de Dados

O projeto suporta **dois bancos de dados**:

- **SQLite** → usado para testes e desenvolvimento local  
- **PostgreSQL** → recomendado para produção

No arquivo `.env`, adicione:
Para testes e desenvolvimentos:
```env
DATABASE_URL=sqlite:///./core.db
```
Para Produção:
```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/erp_core
```
### ⚙️ Executando Migrações
### SQLite (testes):
  
Windows PowerShell:
```env
$env:DATABASE_URL = "sqlite:///./core.db"
alembic upgrade head
```
CMD:
```env
set DATABASE_URL=sqlite:///./core.db
alembic upgrade head
```
### PostgreSQL (produção)
```env
$env:DATABASE_URL = "postgresql://usuario:senha@localhost:5432/erp_core"
alembic upgrade head
```
---

## 6️⃣ Executar aplicação

```bash
uvicorn app.main:app --reload
```

---

## 7️⃣ Executar Seed

Para criar usuários e módulos automaticamente:

```bash
python seed.py
```

Usuários padrão:

```txt
Admin:
admin@erp.com
12345

Usuário:
user@erp.com
12345
```

---

# 🔐 Autenticação

A API utiliza autenticação JWT com OAuth2.

Para autenticar:

1. Acesse `/docs`
2. Utilize o endpoint `/auth/login`
3. Clique em Authorize
4. Informe usuário e senha

---

# 📌 Principais Endpoints

## Auth

* `POST /auth/register`
* `POST /auth/login`
* `GET /auth/verify`
* `POST /auth/refresh`

## Usuários

* `GET /users`
* `PATCH /users/{id}/status`

## Módulos

* `POST /modules`
* `GET /modules`

## Sistema

* `GET /health`

---

# 🩺 Exemplo de Health Check

```json
{
  "status": "ok",
  "services": {
    "core": "online",
    "financeiro": "offline"
  }
}
```

---

# 🧪 Testes Automatizados

Os testes foram desenvolvidos utilizando Pytest e FastAPI TestClient.

## Executar testes

```bash
python -m pytest
```

## Executar cobertura de testes

```bash
python -m pytest --cov=app
```

---

# 📊 Cobertura Atual

```txt
87% de cobertura de testes
```

---

# 🌐 CORS

O sistema está configurado para permitir integração com frontend local:

```txt
http://localhost:3000
```

---

# 🔄 Fluxo Básico do Sistema

1. Usuário realiza login
2. CORE gera token JWT
3. Usuário acessa rotas protegidas
4. Módulos se registram no CORE
5. CORE monitora disponibilidade dos serviços
6. Sistema retorna status online/offline dos módulos

---

# 👨‍💻 Integrantes
* Wallace Souza
* Wallison Souza
* Gabriel Mendes
* Felipe Magalhães
* Pedro Neto
---

# 📌 Observações

Este projeto possui fins acadêmicos e foi desenvolvido para estudo de arquitetura distribuída, autenticação JWT e integração entre microsserviços utilizando FastAPI.

---

# 📄 Licença

Projeto de uso acadêmico.
