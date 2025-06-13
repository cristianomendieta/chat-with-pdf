from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.framework.apis.base_api import router

app = FastAPI(
    title="Chat with PDF API",
    description="API for chatting with PDF documents",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(router, prefix="/api/v1")

