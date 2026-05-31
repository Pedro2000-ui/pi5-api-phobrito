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