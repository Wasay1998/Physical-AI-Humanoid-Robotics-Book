import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    # Cohere settings
    COHERE_API_KEY: str = os.getenv("COHERE_API_KEY")
    
    # Qdrant settings
    QDRANT_URL: str = os.getenv("QDRANT_URL")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY")
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    
    # Application settings
    APP_NAME: str = os.getenv("APP_NAME", "RAG Chatbot API")
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "RAG Chatbot for Interactive Books")
    
    # Security
    API_KEY: str = os.getenv("API_KEY", "your-default-api-key")
    API_KEY_HEADER_NAME: str = os.getenv("API_KEY_HEADER_NAME", "X-API-Key")
    
    # Chunking parameters
    CHUNK_SIZE_TOKENS: int = int(os.getenv("CHUNK_SIZE_TOKENS", "512"))
    OVERLAP_SIZE_TOKENS: int = int(os.getenv("OVERLAP_SIZE_TOKENS", "150"))
    
    # RAG parameters
    TOP_K: int = int(os.getenv("TOP_K", "6"))
    RELEVANCE_THRESHOLD: float = float(os.getenv("RELEVANCE_THRESHOLD", "0.7"))
    MAX_CONCURRENT_REQUESTS: int = int(os.getenv("MAX_CONCURRENT_REQUESTS", "100"))
    
    # Validation
    def validate_settings(self):
        """Validate that required environment variables are set"""
        required_vars = [
            "COHERE_API_KEY",
            "QDRANT_URL", 
            "QDRANT_API_KEY",
            "DATABASE_URL"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(self, var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")


# Create a global settings instance
settings = Settings()