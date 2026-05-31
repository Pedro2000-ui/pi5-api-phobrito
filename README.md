# Configuração do Ambiente

```bash
python -m venv .venv
```

Cria o ambiente virtual Python na pasta `.venv`.

---

## Ativar o Ambiente Virtual

### Windows (Git Bash)

```bash
source .venv/Scripts/activate
```

### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Ativa o ambiente virtual para que as dependências sejam instaladas apenas no projeto atual.

---

## Instalar Dependências

```bash
pip install fastapi "uvicorn[standard]" pydantic
```

Instala as bibliotecas necessárias para a aplicação.

### FastAPI
Framework para criação de APIs REST em Python de forma rápida, moderna e com documentação automática.

### Uvicorn
Servidor ASGI responsável por executar a aplicação FastAPI e processar as requisições HTTP.

### Pydantic
Biblioteca utilizada para validação, conversão e serialização de dados com base em tipagem Python.

---

## Gerar o Arquivo de Dependências

```bash
pip freeze > requirements.txt
```

Gera o arquivo `requirements.txt` contendo todas as dependências instaladas e suas versões.

---

## Executar a Aplicação

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8069 --reload
```

Inicia a aplicação utilizando o Uvicorn.

### Parâmetros

- `app.main`: módulo Python onde a aplicação está localizada.
- `app`: instância do FastAPI.
- `--host 0.0.0.0`: permite acesso à aplicação por outras máquinas da rede.
- `--port 8069`: define a porta utilizada pela aplicação.
- `--reload`: reinicia automaticamente o servidor ao detectar alterações no código.

---

# Executando o Projeto Localmente

Após instalar as dependências e ativar o ambiente virtual, execute o comando abaixo:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8069 --reload
```

A aplicação ficará disponível em:

```text
http://localhost:8069
```

Caso a documentação automática esteja habilitada, ela poderá ser acessada em:

### Swagger UI

```text
http://localhost:8069/docs
```

### ReDoc

```text
http://localhost:8069/redoc
```

---

# Utilizando a API em Produção

A API está disponível em produção através do Railway:

```text
https://pi5-api-phobrito-production.up.railway.app/
```

## URL Base

```text
https://pi5-api-phobrito-production.up.railway.app/
```

Todas as requisições devem utilizar essa URL como base.

### Exemplo

Endpoint local:

```text
http://localhost:8069/endpoint
```

Endpoint em produção:

```text
https://pi5-api-phobrito-production.up.railway.app/endpoint
```

## Documentação da API

### Swagger UI

```text
https://pi5-api-phobrito-production.up.railway.app/docs
```

### ReDoc

```text
https://pi5-api-phobrito-production.up.railway.app/redoc
```