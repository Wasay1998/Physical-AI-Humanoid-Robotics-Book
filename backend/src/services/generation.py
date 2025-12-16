"""
Generation service using Cohere to create responses based on retrieved context.
"""
from typing import List, Dict, Any
from datetime import datetime
import cohere
from src.config.settings import settings
from src.config.logging import get_logger
from src.models.response import Response, Citation


logger = get_logger(__name__)

# Initialize Cohere client
co = cohere.Client(api_key=settings.COHERE_API_KEY)


async def generate_response(
    query: str,
    context_chunks: List[Dict[str, Any]],
    query_id: str,
    selected_text: str = None
) -> Response:
    """
    Generate a response using Cohere based on the query and retrieved context.

    Args:
        query: The user's query
        context_chunks: List of relevant content chunks
        query_id: The ID of the original query
        selected_text: Optional selected text for context

    Returns:
        Response object with generated text and citations
    """
    try:
        # Prepare the context for the model
        context = "\n\n".join([chunk['content'] for chunk in context_chunks])

        # Create the prompt for the model with proper RAG instructions
        if selected_text:
            prompt = f"""
            You are an AI assistant that answers questions based only on the provided context.
            Do not generate answers that are not directly supported by the context.
            If the context does not contain information to answer the question, say "I cannot answer based on the provided information."

            Context for answering the question:
            {context}

            User's selected text for additional context:
            {selected_text}

            User's question:
            {query}

            Provide a clear, concise answer based only on the context and selected text.
            Include citations for any information you use.
            """
        else:
            prompt = f"""
            You are an AI assistant that answers questions based only on the provided context.
            Do not generate answers that are not directly supported by the context.
            If the context does not contain information to answer the question, say "I cannot answer based on the provided information."

            Context for answering the question:
            {context}

            User's question:
            {query}

            Provide a clear, concise answer based only on the context.
            Include citations for any information you use.
            """

        # Generate response using Cohere with proper parameters for factuality
        response = co.generate(
            model='command-r-plus',  # Using command-r-plus as specified in requirements
            prompt=prompt,
            max_tokens=500,  # Adjust as needed
            temperature=0.3,  # Lower temperature for more factual responses
            stop_sequences=["\n\n"]  # Stop at double newlines to avoid overly long responses
        )

        # Extract the generated text
        generated_text = response.generations[0].text.strip()

        # Create citations from the context chunks
        citations = []
        for chunk in context_chunks:
            citations.append(
                Citation(
                    chunk_id=chunk.get('chunk_id', ''),
                    page_number=chunk.get('page_number', 0),
                    section_title=chunk.get('section_title', ''),
                    text_preview=chunk.get('content', '')[:100] + "..." if len(chunk.get('content', '')) > 100 else chunk.get('content', '')
                )
            )

        # Calculate relevance score based on the number of citations and context usage
        relevance_score = calculate_relevance_score(query, generated_text, context_chunks)

        return Response(
            query_id=query_id,
            response_text=generated_text,
            generated_at=datetime.utcnow(),
            sources=[{k: v for k, v in chunk.items() if k != 'embedding'} for chunk in context_chunks],  # Exclude embedding from sources
            relevance_score=relevance_score,
            model_used="command-r-plus",
            token_usage={
                "input_tokens": len(prompt.split()),
                "output_tokens": len(generated_text.split())
            },
            citations=citations
        )

    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise


def calculate_relevance_score(query: str, response: str, context_chunks: List[Dict[str, Any]]) -> float:
    """
    Calculate a relevance score based on how well the response matches the query and uses the context.

    Args:
        query: The original query
        response: The generated response
        context_chunks: The context chunks used to generate the response

    Returns:
        A relevance score between 0.0 and 1.0
    """
    # This is a simplified relevance calculation
    # In a real implementation, you might use more sophisticated NLP techniques

    # Calculate basic metrics
    query_words = set(query.lower().split())
    response_words = set(response.lower().split())

    # Simple overlap metric
    overlap = len(query_words.intersection(response_words))
    overlap_score = min(1.0, overlap / max(len(query_words), 1))

    # Use more context chunks as an indicator of better grounding
    context_utilization_score = min(1.0, len(context_chunks) / 10.0)  # Assuming max 10 chunks is ideal

    # Combine scores
    relevance_score = (overlap_score * 0.4) + (context_utilization_score * 0.6)

    # Ensure it's within bounds
    return max(0.0, min(1.0, relevance_score))