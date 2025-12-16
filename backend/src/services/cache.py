"""
Caching service for frequently accessed embeddings and other data.
"""
from typing import Optional, Dict, Any
import hashlib
import asyncio
from datetime import datetime, timedelta
from src.config.logging import get_logger


logger = get_logger(__name__)


class CacheService:
    """
    Simple in-memory cache service for frequently accessed data.
    In a production environment, this would likely use Redis or another caching solution.
    """
    
    def __init__(self, default_ttl: int = 3600):  # 1 hour default TTL
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
        self._lock = asyncio.Lock()  # For thread safety in async context
    
    async def get(self, key: str) -> Optional[Any]:
        """
        Get a value from the cache.
        
        Args:
            key: The cache key
            
        Returns:
            The cached value or None if not found or expired
        """
        async with self._lock:
            if key in self._cache:
                entry = self._cache[key]
                # Check if the entry has expired
                if datetime.now() < entry['expires_at']:
                    logger.debug(f"Cache HIT for key: {key}")
                    return entry['value']
                else:
                    # Remove expired entry
                    del self._cache[key]
                    logger.debug(f"Cache EXPIRED for key: {key}")
        
        logger.debug(f"Cache MISS for key: {key}")
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set a value in the cache.
        
        Args:
            key: The cache key
            value: The value to cache
            ttl: Time to live in seconds (uses default if not specified)
        """
        if ttl is None:
            ttl = self.default_ttl
        
        async with self._lock:
            self._cache[key] = {
                'value': value,
                'expires_at': datetime.now() + timedelta(seconds=ttl)
            }
            logger.debug(f"Cache SET for key: {key} with TTL: {ttl}s")
    
    async def delete(self, key: str) -> bool:
        """
        Delete a value from the cache.
        
        Args:
            key: The cache key to delete
            
        Returns:
            True if the key was found and deleted, False otherwise
        """
        async with self._lock:
            if key in self._cache:
                del self._cache[key]
                logger.debug(f"Cache DELETE for key: {key}")
                return True
            return False
    
    async def clear(self) -> None:
        """
        Clear all entries from the cache.
        """
        async with self._lock:
            self._cache.clear()
            logger.debug("Cache CLEARED")
    
    async def has(self, key: str) -> bool:
        """
        Check if a key exists in the cache and is not expired.
        
        Args:
            key: The cache key to check
            
        Returns:
            True if the key exists and is not expired, False otherwise
        """
        value = await self.get(key)
        return value is not None


# Create a singleton instance
cache_service = CacheService()


def generate_embedding_cache_key(text: str, model: str = "embed-english-v3.0") -> str:
    """
    Generate a cache key for an embedding based on the text and model.
    
    Args:
        text: The text that was embedded
        model: The model used for embedding
        
    Returns:
        A unique cache key for this embedding
    """
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    return f"embedding:{model}:{text_hash}"