# Chat with PDF

A Retrieval Augmented Generation (RAG) application that enables users to ask questions about PDF documents using natural language processing and hybrid search capabilities.

## 🚀 Features

- **PDF Upload**: Upload multiple PDF documents for indexing
- **Hybrid Search**: Combines semantic (dense) and lexical (sparse) search for better accuracy
- **Session Management**: Filter answers by uploaded files in the current session
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
    "search_strategy": "hybrid",
    "max_documents": 5,
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

### Request Examples

#### Question Request - Technical Content
```json
{
  "question": "Qual é a diferença entre potência ativa, aparente e reativa, e como elas se relacionam com o fator de potência?",
  "search_strategy": "hybrid",
  "max_documents": 5,
}
```

#### Question Request - Maintenance Procedures
```json
{
  "question": "Qual é o procedimento recomendado quando o redutor ou motorredutor da WEG-CESTARI não for utilizado por um período superior a 6 meses?",
  "search_strategy": "hybrid",
  "max_documents": 5,
}
```

#### Question Request - General Information
```json
{
  "question": "Por que o motor de indução é considerado o mais utilizado entre os motores elétricos, segundo o guia da WEG?",
  "search_strategy": "hybrid",
  "max_documents": 5,
}
```

### Response Examples

#### Response - Technical Explanation
```json
{
  "answer": "A potência ativa (P) é a parcela da potência aparente que realiza trabalho útil, medida em Watts (W). A potência reativa (Q) não realiza trabalho, mas é necessária para manter os campos magnéticos em capacitores e indutores, medida em Volt-Ampere reativo (VAr). A potência aparente (S) é a combinação vetorial das potências ativa e reativa, medida em Volt-Ampere (VA), e o fator de potência (cos ϕ) é a razão entre a potência ativa e a aparente, indicando a eficiência do uso da energia.",
  "references": [
    "P\n\nS  = (VA)\nCos ϕ\n\nEvidentemente, para as cargas resistivas, cos ϕ = 1 e a\npotência ativa se confunde com a potência aparente.\nA unidade de medida para potência aparente é o VoltAmpère (VA) ou seu múltiplo, o quilo-Volt-Ampère (kVA).\n\nPotência ativa (P)\nÉ a parcela da potência aparente que realiza trabalho, ou\nseja, que é transformada em energia.\n\nP =  3 . U . I . cos √ ϕ (W)  ou  P = S . cos ϕ (W)\n\nPotência reativa (Q)\nÉ a parcela da potência aparente que \"não\" realiza trabalho.\nApenas é transferida e armazenada nos elementos passivos\n(capacitores e indutores) do circuito.\n\nQ  =   3 . U. I sen √ ϕ (VAr)  ou  Q = S . sen ϕ (VAr)",
    "Figura 1.4 - Fator de potência\n\nImportância do fator de potência\nA energia reativa limita a capacidade de transporte de energia\nútil (ativa) nas linhas de transmissão, subtransmissão e\ndistribuição, em outras palavras, quanto maior o fator de\npotência, maior a disponibilidade de potência ativa no sistema\ne maior é o aproveitamento do sistema elétrico brasileiro.\nO fator de potência de referência das cargas, determinado\npela portaria do DNAEE número 85, é de 0,92."
  ]
}
```

#### Response - Maintenance Procedure
```json
{
  "answer": "Quando o redutor ou motorredutor WEG-CESTARI não for utilizado por mais de 6 meses (até 9 meses), deve-se preencher todo o interior com lubrificante adequado até a parte superior, garantindo que engrenagens e rolamentos fiquem imersos em óleo. O eixo de entrada deve ser girado pelo menos duas voltas completas a cada 2 meses. Além disso, proteger os retentores externamente com graxa para evitar ressecamento, removendo-a antes da operação.",
  "references": [
    "Os redutores/motorredutores da WEG-CESTARI deverão ser armazenados na posição de trabalho\nespecificada e fornecida, em superfície plana sobre estrados ou em prateleiras apropriadas (não em\ncontato direto com o piso) e não disposto em local com trepidação e oscilações.\n2.1 Período sem funcionamento\nOs redutores/motorredutores WEG-CESTARI saem de fábrica e devem ser postos em operação\ndentro do período máximo de 6 meses.\nPara períodos de 6 meses até 9 meses sem operação, é recomendado preencher todo interior do\nredutor com lubrificantes apropriados",
    "imersos em óleo. O eixo de entrada do redutor deverá ser girado no mínimo duas voltas completas e\neste procedimento deverá ser repetido, no mínimo, 1 vez a cada 2 meses.\nNOTAS: Antes da operação, o lubrificante do redutor/motorredutor deverá ser drenado até o nível\nadequado para operação"
  ]
}
```

#### Response - General Information
```json
{
  "answer": "O motor de indução é o mais utilizado entre os motores elétricos porque combina baixo custo, facilidade de transporte, limpeza, simplicidade de comando, construção simples e grande versatilidade para se adaptar a diversos tipos de cargas, além de apresentar melhores rendimentos.",
  "references": [
    "Motor elétrico é a máquina destinada a transformar energia\nelétrica em energia mecânica. O motor de indução é o mais\nusado de todos os tipos de motores, pois, combina as\nvanta g ens da utilização de energia elétrica - baixo custo,\nfacilidade de transporte, limpeza, simplicidade de\ncomando - com sua construção simples e grande\nversatilidade de adaptação às car g as dos mais\ndiversos tipos e melhores rendimentos."
  ]
}
```

### Data Models Schema

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
    "question": str,                    # User's question
    "search_strategy": str,             # "dense", "sparse", or "hybrid" (default)
    "max_documents": int,               # Maximum number of documents to retrieve (default: 5)
    "file_filters": List[str]           # Optional list of filenames to filter results
}
```

#### QuestionResult
```python
{
    "answer": str,                      # AI-generated response
    "references": List[str]             # List of source document excerpts
}
```