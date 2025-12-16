from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from src.config.settings import settings
from src.config.logging import get_logger
from src.api.routes import ingest, query, health


logger = get_logger(__name__)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Create FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for interacting with the Cohere-powered RAG chatbot system for interactive books",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://physical-ai-humanoid-robotics-book-nine-lake.vercel.app"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include API routes
app.include_router(ingest.router, prefix=settings.API_V1_STR, tags=["ingestion"])
app.include_router(query.router, prefix=settings.API_V1_STR, tags=["query"])
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["health"])


@app.get("/")
def read_root():
    return {"message": "RAG Chatbot API for Interactive Books", "status": "running"}


logger.info(f"{settings.APP_NAME} initialized successfully")