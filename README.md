# Chat with PDF

A Retrieval Augmented Generation (RAG) application that enables users to ask questions about PDF documents using natural language processing and hybrid search capabilities.

## 🚀 Features

- **PDF Upload**: Upload multiple PDF documents for indexing
- **Hybrid Search**: Combines semantic (dense) and lexical (sparse) search for better accuracy
- **Web Interface**: Intuitive Streamlit interface for user interaction
- **REST API**: FastAPI backend for integration with external systems
- **Clean Architecture**: Implementation based on Domain-Driven Design (DDD) principles
- **Containerization**: Fully dockerized application
- **Asynchronous Processing**: Concurrent document processing capabilities
- **Multi-LLM Support**: Compatible with OpenAI and Groq models

## 🏗️ Architecture

The project follows a clean architecture with clear separation of concerns:

```
app/
├── config/           # Dependency injection configuration
├── controllers/      # API controllers
├── domain/          # Business rules and interfaces
│   ├── entities/    # Domain entities
│   ├── interfaces/  # Contracts/interfaces
│   ├── models/      # Data models
│   └── services/    # Domain services
├── framework/       # Framework-specific code (FastAPI)
│   └── apis/        # API routes
└── infra/          # Infrastructure layer
    ├── encoders/    # Text encoders
    ├── gateways/    # External gateways (Pinecone)
    ├── llm/         # LLM integrations
    ├── repositories/# Data repositories
    └── services/    # Infrastructure services
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **Python 3.11+** - Programming language
- **LangChain** - Framework for LLM applications
- **Pinecone** - Vector database
- **OCRmyPDF** and **Tesseract** - OCR tools
- **PyMuPDF** - PDF document processing
- **Kink** - Dependency injection container
- **Uvicorn** - ASGI server

### Frontend
- **Streamlit** - Interactive web interface

### LLM Integration
- **OpenAI** - GPT models for response generation
- **Groq** - Fast LLM inference(used as model fallback)

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **UV** - Python dependency manager

## 📋 Prerequisites

- Docker and Docker Compose
- API Keys:
  - Pinecone API Key
  - At least one LLM provider API Key (OpenAI or Groq)

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <repository-url>
cd chat-with-pdf
```

### 2. Set up environment variables
Create a `.env` file in the project root:

```env
# Pinecone Configuration
PINECONE_API_KEY=your_pinecone_api_key_here

# LLM Configuration (choose one or more)
OPENAI_API_KEY=your_openai_api_key_here
# or
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run with Docker Compose
```bash
docker-compose up --build
```

### 4. Access the application
- **Web Interface (Streamlit)**: http://localhost:8501
- **API Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🐛 Debugging

For local development and debugging:

1. **Start the application**:
   ```bash
   docker-compose up --build
   ```

2. **Enable debugging in your IDE**:
   - Docker Compose is configured for remote debugging on port 5678
   - In VSCode, use the debugger configuration to attach to the running container
   - Set breakpoints in your code and debug as usual

3. **Debug configuration**:
   The application supports remote debugging through the containerized environment, allowing you to debug the running application without leaving the Docker context.

## 📚 Usage

### Web Interface (Streamlit)

1. Navigate to http://localhost:8501
2. Upload one or more PDF files
3. Wait for processing and indexing to complete
4. Ask questions in the chat interface
5. Receive answers based on document content

### REST API

#### Upload Documents
```bash
curl -X POST "http://localhost:8000/api/v1/documents" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@document.pdf"
```

#### Ask Questions
```bash
curl -X POST "http://localhost:8000/api/v1/question" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the main content of the document?",
  }'
```

### Running tests
```bash
# Run test notebooks
jupyter notebook notebooks/
```

### Debugging
Docker Compose is configured for remote debugging on port 5678.

## 📁 Data Models

### Request/Response Models

#### DocumentProcessResult
```python
{
    "message": "Documents processed successfully",
    "documents_indexed": 3,
    "total_chunks": 150
}
```

#### QuestionRequest
```python
{
    "question": "Your question here",
}
```

#### QuestionResult
```python
{
    "answer": "AI-generated response",
    "references": ["source1.pdf", "source2.pdf"]
}
```