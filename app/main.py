from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.di_container import di_container
from app.framework.apis.base_api import router

# Initialize dependency injection container
di_container()

app = FastAPI(
    title="Chat with PDF API",
    description="API for chatting with PDF documents using RAG and hybrid search",
    version="0.1.0",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint to verify API status."""
    return {"status": "healthy"}


# Include API routes
app.include_router(router, prefix="/api/v1")
