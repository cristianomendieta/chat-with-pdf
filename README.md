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
- **Multi-LLM Support**: Compatible with OpenAI, Google Gemini, and Groq models

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
- **PyMuPDF** - PDF document processing
- **Kink** - Dependency injection container
- **Uvicorn** - ASGI server

### Frontend
- **Streamlit** - Interactive web interface

### LLM Integration
- **OpenAI** - GPT models for response generation
- **Google Gemini** - Alternative AI models
- **Groq** - Fast LLM inference

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **UV** - Python dependency manager

## 📋 Prerequisites

- Docker and Docker Compose
- API Keys:
  - Pinecone API Key
  - At least one LLM provider API Key (OpenAI, Groq, or Google Gemini)

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
PINECONE_DENSE_INDEX_NAME=dense-chat-with-pdf
PINECONE_SPARSE_INDEX_NAME=sparse-chat-with-pdf

# LLM Configuration (choose one or more)
OPENAI_API_KEY=your_openai_api_key_here
# or
GROQ_API_KEY=your_groq_api_key_here
# or
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Run with Docker Compose
```bash
docker-compose up --build
```

### 4. Access the application
- **Web Interface (Streamlit)**: http://localhost:8501
- **API Backend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

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
    "search_strategy": "hybrid",
    "max_documents": 5
  }'
```

#### Check Service Status
```bash
curl -X GET "http://localhost:8000/api/v1/question/status"
```

## 🔧 Advanced Configuration

### Search Strategies
- **`hybrid`** (default): Combines semantic and lexical search
- **`dense`**: Semantic search only
- **`sparse`**: Lexical search only

### Search Parameters
- **`max_documents`**: Maximum number of documents for context (default: 5)
- **`search_strategy`**: Search strategy to use

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
    "search_strategy": "hybrid",  # optional
    "max_documents": 5           # optional
}
```

#### QuestionResult
```python
{
    "answer": "AI-generated response",
    "references": ["source1.pdf", "source2.pdf"]
}
```

## � Components

### Controllers
- **DocumentController**: Handles PDF upload and processing operations
- **QuestionController**: Manages question answering operations

### Services
- **DocumentProcessingService**: Processes and indexes PDF documents
- **QuestionAnsweringService**: Handles question answering with hybrid search

### Domain Models
- **DocumentProcessResult**: Document processing statistics
- **QuestionRequest**: Question request with search parameters
- **QuestionResult**: Answer with source references