# refresh_token

Este projeto é um experimento de estudo para aprender a implementar autenticação JWT com refresh tokens usando Django REST Framework.

O foco principal é demonstrar um fluxo básico de autenticação segura em APIs, incluindo:
- cadastro de usuário
- login com geração de access token e refresh token
- renovação do access token usando o refresh token
- alteração de senha com invalidação de tokens antigos
- proteção de rotas com autenticação JWT

## Tecnologias utilizadas

- Python 3.14
- Django 6.0
- Django REST Framework
- djangorestframework-simplejwt
- PostgreSQL
- Docker / Docker Compose (opcional)

## Endpoints principais

Todos os endpoints estão expostos sob o prefixo `/account/`.

- `POST /account/register/`
  - Cria um novo usuário.
  - Dados esperados: `email`, `password`, `confirm_password`.

- `POST /account/login/`
  - Autentica o usuário e retorna `access_token` e `refresh_token`.
  - Dados esperados: `email` e `password`.

- `POST /account/refresh_token/`
  - Recebe um `refresh_token` válido e retorna um novo `access_token`.
  - Dados esperados: `refresh_token`.

- `POST /account/change_password/`
  - Altera a senha do usuário logado e invalida tokens antigos.
  - Requer autenticação JWT no header `Authorization: Bearer <access_token>`.
  - Dados esperados: `current_password`, `new_password`, `confirm_new_password`.

- `GET /account/test_authentication/`
  - Verifica se o usuário está autenticado.
  - Requer JWT válido no header `Authorization: Bearer <access_token>`.

## Como funciona

A aplicação usa `rest_framework_simplejwt` para gerenciar tokens JWT e `token_blacklist` para invalidar refresh tokens quando a senha é alterada.

Configurações importantes em `refresh_tokens/settings.py`:
- `ACCESS_TOKEN_LIFETIME`: 15 minutos
- `REFRESH_TOKEN_LIFETIME`: 7 dias
- `AUTH_USER_MODEL = 'accounts.Account'`
- `DEFAULT_AUTHENTICATION_CLASSES`: JWTAuthentication

## Estrutura do projeto

- `accounts/models.py`: modelo de usuário customizado.
- `accounts/serializers.py`: validação de dados, login, refresh e troca de senha.
- `accounts/views.py`: implementação das views da API.
- `accounts/services.py`: lógica de geração e revogação de tokens.
- `accounts/urls.py`: rotas da app `accounts`.
- `refresh_tokens/settings.py`: configurações do Django, banco de dados e JWT.

## Variáveis de ambiente

O projeto carrega variáveis de ambiente via `python-dotenv`. Crie um arquivo `.env` na raiz com as seguintes chaves:

- `SECRET_KEY`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

> Dica: mantenha `SECRET_KEY` seguro e nunca comite o `.env` no repositório.

## Como executar

### Localmente

1. Ative o ambiente virtual:
   ```bash
   python -m venv myvenv
   source myvenv/bin/activate
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Crie o arquivo `.env` com as configurações do PostgreSQL e `SECRET_KEY`.

4. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

5. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

6. Acesse a API em:
   ```text
   http://127.0.0.1:8000/
   ```

### Com Docker

Se preferir, use Docker Compose para subir o projeto:

```bash
docker compose up --build
```

## Testes e uso

Não há uma suíte de testes automatizados incluída no projeto, mas você pode testar os endpoints com ferramentas como Postman, Insomnia ou `curl`.

Exemplo de uso com `curl`:

```bash
curl -X POST http://127.0.0.1:8000/account/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"usuario","email":"user@example.com","password":"senha123","password_confirm":"senha123"}'
```

## Observação

Este projeto é uma prova de conceito para aprendizado e não deve ser usado como base de produção sem ajustes de segurança adicionais.
