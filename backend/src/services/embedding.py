"""
Embedding service using Cohere to generate vector representations of text.
"""
import cohere
from typing import List, Union
from src.config.settings import settings
from src.config.logging import get_logger
from src.services.cache import cache_service, generate_embedding_cache_key


logger = get_logger(__name__)

# Initialize Cohere client
co = cohere.Client(api_key=settings.COHERE_API_KEY)


async def generate_embeddings(texts: Union[str, List[str]]) -> List[List[float]]:
    """
    Generate embeddings for one or more texts using Cohere's embed-v3 model.
    Uses caching to avoid regenerating embeddings for the same text.

    Args:
        texts: A single text string or a list of text strings to embed

    Returns:
        A list of embeddings (each embedding is a list of floats)
    """
    try:
        # Ensure texts is a list
        if isinstance(texts, str):
            texts = [texts]

        # Check cache for each text
        results = []
        texts_to_generate = []
        text_indices = []  # Track which original positions these texts correspond to

        for i, text in enumerate(texts):
            cache_key = generate_embedding_cache_key(text, "embed-english-v3.0")
            cached_result = await cache_service.get(cache_key)

            if cached_result is not None:
                # Use cached result
                results.extend(cached_result)  # Add cached embeddings to results
            else:
                # Need to generate this embedding
                texts_to_generate.append(text)
                text_indices.append(i)

        # Generate embeddings for texts not in cache
        if texts_to_generate:
            response = co.embed(
                texts=texts_to_generate,
                model="embed-english-v3.0",  # Using embed-v3 as specified in requirements
                input_type="search_document"  # Using search_document type for content chunks
            )

            # Cache the new embeddings and add to results
            for j, (text, embedding) in enumerate(zip(texts_to_generate, response.embeddings)):
                cache_key = generate_embedding_cache_key(text, "embed-english-v3.0")
                # Cache as a single-item list since embed can handle batch requests
                await cache_service.set(cache_key, [embedding])

                # Add to results at the correct position
                results.append(embedding)

        logger.info(f"Generated embeddings for {len(texts)} text(s)")
        return results

    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise


async def embed_query(text: str) -> List[float]:
    """
    Generate an embedding for a query text using Cohere's embed-v3 model.
    Uses 'search_query' input type which is appropriate for queries.
    Uses caching to avoid regenerating embeddings for the same query.

    Args:
        text: The query text to embed

    Returns:
        An embedding (list of floats)
    """
    try:
        cache_key = generate_embedding_cache_key(text, "embed-english-v3.0-query")
        cached_result = await cache_service.get(cache_key)

        if cached_result is not None:
            logger.info(f"Retrieved cached embedding for query: {text[:50]}...")
            return cached_result

        # Generate embedding for query using appropriate input type
        response = co.embed(
            texts=[text],
            model="embed-english-v3.0",
            input_type="search_query"  # Using search_query type for queries
        )

        embedding = response.embeddings[0]  # Return the first (and only) embedding

        # Cache the result
        await cache_service.set(cache_key, embedding)

        logger.info(f"Generated embedding for query: {text[:50]}...")
        return embedding

    except Exception as e:
        logger.error(f"Error generating query embedding: {str(e)}")
        raise