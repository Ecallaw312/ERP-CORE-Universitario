# Contrato de Autenticação — ERP Core

Este documento descreve como o **Frontend** e os **módulos** devem se autenticar e consumir a API do CORE.

Base URL: `http://localhost:8000`

---

## Fluxo Geral

```
1. Frontend chama POST /auth/login com email + senha
2. CORE retorna access_token (JWT) + dados do usuário
3. Frontend armazena o token e envia em todas as requisições protegidas:
   Authorization: Bearer <access_token>
4. Quando o token expira (401), Frontend chama POST /auth/refresh
5. CORE retorna novo access_token
```

---

## Endpoints

### `POST /auth/register`

Cria um novo usuário no sistema. Uso interno / administrativo.

**Request body:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "senha123",
  "perfil": "user"
}
```

| Campo  | Tipo   | Obrigatório | Valores aceitos     |
|--------|--------|-------------|---------------------|
| nome   | string | ✅          | qualquer string     |
| email  | string | ✅          | e-mail único        |
| senha  | string | ✅          | qualquer string     |
| perfil | string | ❌          | `"admin"` \| `"user"` (padrão: `"user"`) |

**Response 200:**
```json
{ "message": "Usuário registrado com sucesso: joao@email.com" }
```

**Erros:**
- `400` — e-mail já cadastrado

---

### `POST /auth/login`

Autentica o usuário e retorna os tokens.

**Request body:**
```json
{
  "email": "joao@email.com",
  "senha": "senha123"
}
```

**Response 200:**
```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@email.com",
    "perfil": "user"
  }
}
```

> ⚠️ **Os nomes dos campos são fixos.** O frontend depende de `access_token`, `token_type`, `user.id`, `user.nome`, `user.email` e `user.perfil` exatamente assim.

**Erros:**
- `403` — e-mail não encontrado ou senha incorreta

---

### `POST /auth/verify`

Valida se o token atual ainda é válido. Útil para o frontend checar sessão ao carregar a aplicação.

**Header obrigatório:**
```
Authorization: Bearer <access_token>
```

**Response 200:**
```json
{
  "mensagem": "Token válido",
  "user": {
    "nome": "João Silva",
    "perfil": "user"
  }
}
```

**Erros:**
- `401` — token inválido ou expirado

---

### `POST /auth/refresh`

Gera um novo `access_token` a partir do token atual ainda válido.

**Header obrigatório:**
```
Authorization: Bearer <access_token>
```

**Response 200:**
```json
{
  "access_token": "<novo_jwt>",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "nome": "João Silva",
    "email": "joao@email.com",
    "perfil": "user"
  }
}
```

**Erros:**
- `401` — token inválido ou expirado

---

## Como os módulos devem usar o token

Os módulos do ERP (Financeiro, RH, Estoque, Compras) **não fazem login** — quem faz login é o usuário via Frontend.

O Frontend envia o `access_token` recebido do CORE em cada requisição para os módulos:

```
Authorization: Bearer <access_token>
```

Se um módulo precisar validar o token, deve chamar:

```
POST http://localhost:8000/auth/verify
Authorization: Bearer <access_token>
```

---

## Códigos de erro padrão

| Código | Significado                        |
|--------|------------------------------------|
| 400    | Dados inválidos ou duplicados      |
| 401    | Sessão expirada / token inválido   |
| 403    | Acesso negado (perfil insuficiente)|
| 404    | Recurso não encontrado             |
| 500    | Erro interno do servidor           |

---

## Perfis de acesso

| Perfil  | Pode fazer login | Acessa /users | Acessa /modulos | Acessa rotas do sistema |
|---------|-----------------|---------------|-----------------|------------------------|
| `admin` | ✅              | ✅            | ✅              | ✅                     |
| `user`  | ✅              | ❌            | ❌              | ✅ (rotas públicas)    |

---

## Expiração dos tokens

Configurado via `.env`:

| Variável                    | Padrão recomendado |
|-----------------------------|--------------------|
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 60 minutos       |
| `REFRESH_TOKEN_EXPIRE_DAYS`   | 7 dias           |
