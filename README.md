# PI5 backend (bot carille)

API desenvolvida em Python com FastAPI para execução do BOT Carille.

A aplicação recebe o estado atual do jogo, processa as informações utilizando a estratégia implementada pelo bot e retorna a ação escolhida para o turno.

## Estratégia do BOT

A documentação da estratégia utilizada pelo BOT Carille está disponível em [docs/estrategia.md](docs/estrategia.md).


Nesse documento estão descritos os critérios de avaliação do tabuleiro, sistema de pontuação, heurísticas e processo de tomada de decisão.

---

## Configuração do Ambiente

### Criar o ambiente virtual

```bash
python -m venv .venv
```

### Ativar o ambiente virtual

#### Windows (Git Bash)

```bash
source .venv/Scripts/activate
```

#### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

#### Linux/macOS

```bash
source .venv/bin/activate
```

---

## Instalação das Dependências

```bash
pip install fastapi "uvicorn[standard]" pydantic
```

### Gerar o arquivo requirements.txt

```bash
pip freeze > requirements.txt
```

---

## Execução Local

Inicie a aplicação com:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8069 --reload
```

A API ficará disponível em:

```text
http://localhost:8069
```

### Documentação

Swagger:

```text
http://localhost:8069/docs
```

ReDoc:

```text
http://localhost:8069/redoc
```

---

## Ambiente de Produção

URL base:

```text
https://pi5-api-phobrito-production.up.railway.app/
```

Exemplo:

Local:

```text
http://localhost:8069/endpoint
```

Produção:

```text
https://pi5-api-phobrito-production.up.railway.app/endpoint
```

### Documentação

Swagger:

```text
https://pi5-api-phobrito-production.up.railway.app/docs
```

ReDoc:

```text
https://pi5-api-phobrito-production.up.railway.app/redoc
```

---

## Estrutura do Projeto

```text
├── app/
│    └── __init__.py
│    └── logic.py
│    └── main.py
│    └── schemas.py
├── docs/
│   └── choose_setup.md
│   └── choose_turn.md
│   └── estrategia.md
├── requirements.txt
└── README.md
```
