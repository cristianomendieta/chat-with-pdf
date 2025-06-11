# Chat with PDF

Um aplicativo para conversar com documentos PDF usando IA, construído com FastAPI e Streamlit.

## 🚀 Funcionalidades

- Interface web interativa para upload de PDFs
- Chat em tempo real com documentos
- API RESTful para integração
- Containerização com Docker

## 🛠️ Tecnologias

- **Backend**: FastAPI, Python 3.11
- **Frontend**: Streamlit
- **Containerização**: Docker & Docker Compose
- **Gerenciamento de dependências**: UV

## 📦 Instalação e Execução

### Pré-requisitos

- Docker
- Docker Compose

### Execução Rápida

```bash
# Executar o script de inicialização
./start.sh
```

### Execução Manual

```bash
# Construir e executar os containers
docker-compose up --build

# Executar em background
docker-compose up -d --build
```

## 🌐 Acessos

- **Frontend (Streamlit)**: http://localhost:8501
- **Backend (FastAPI)**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

## 🏗️ Estrutura do Projeto

```
chat-with-pdf/
├── app/                    # Backend FastAPI
│   ├── main.py            # Ponto de entrada da API
│   ├── framework/         # Framework e rotas
│   └── dockerfile         # Dockerfile do backend
├── ui/                    # Frontend Streamlit
│   ├── chat.py           # Interface do usuário
│   └── dockerfile        # Dockerfile do frontend
├── docker-compose.yml    # Configuração dos serviços
├── pyproject.toml        # Dependências do projeto
└── start.sh             # Script de inicialização
```

## 🔧 Desenvolvimento

Para desenvolvimento local:

```bash
# Instalar dependências
uv sync

# Executar backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Executar frontend (em outro terminal)
streamlit run ui/chat.py --server.port 8501
```

## 📝 API Endpoints

- `GET /`: Status da aplicação
- `GET /health`: Verificação de saúde
- `POST /api/v1/chat`: Endpoint de chat
- `GET /api/v1/status`: Status do assistente

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request