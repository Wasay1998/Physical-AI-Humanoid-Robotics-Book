from fastapi import Depends, HTTPException, status
from typing import AsyncGenerator
from src.config.settings import settings
from src.services.database import db_service


# Dependency to get the database service
async def get_db_service():
    """
    Dependency to provide the database service instance.
    In a more complex implementation, this might handle connection pooling,
    transactions, etc.
    """
    # In this implementation, we're using a singleton pattern for the db_service
    # In a more advanced implementation, you might set up actual database connections here
    return db_service


# API key dependency
def get_api_key(api_key_header: str = Depends(lambda: settings.API_KEY)):
    """
    Dependency to validate the API key.
    """
    # In a real implementation, this would check the provided key against the expected key
    # For now, we'll just return the expected key
    return api_key_header