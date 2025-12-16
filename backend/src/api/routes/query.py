from fastapi import APIRouter, HTTPException, Header, status
from typing import Optional, List
import uuid
from pydantic import BaseModel
from src.config.settings import settings
from src.config.logging import get_logger
from src.services.retrieval import search_chunks
from src.services.generation import generate_response
from src.services.database import db_service
from src.models.response import UserQuery, Response, Citation


router = APIRouter()
logger = get_logger(__name__)


class QueryRequest(BaseModel):
    book_id: str
    query: str
    session_token: Optional[str] = None
    top_k: Optional[int] = settings.TOP_K
    relevance_threshold: Optional[float] = settings.RELEVANCE_THRESHOLD
    selected_text: Optional[str] = None


class QueryResponse(BaseModel):
    response: str
    citations: List[Citation]
    session_token: str
    query_id: str
    relevance_score: float


@router.post("/query", summary="Query the RAG system for a book", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    x_api_key: str = Header(None)
):
    """
    Submit a natural language query about the content of a specific book 
    and receive an AI-generated response with citations.
    """
    try:
        # Validate API key
        if x_api_key != settings.API_KEY:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        # Validate that the book exists
        book = await db_service.get_book_content(request.book_id)
        if not book:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )
        
        # Validate query is not empty
        if not request.query.strip():
            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty"
            )
        
        # Create a new chat session if one doesn't exist
        if not request.session_token:
            session_data = {
                "book_id": request.book_id,
                "session_token": str(uuid.uuid4()),
                "is_active": True
            }
            session = await db_service.create_chat_session(session_data)
            request.session_token = session.session_token
        else:
            # For now, we'll just use the provided session token
            # In a real implementation, you would validate and retrieve the session
            pass
        
        # Create user query record
        query_data = {
            "session_id": request.session_token,
            "query_text": request.query,
            "query_type": "SELECTED_TEXT" if request.selected_text else "FULL_BOOK",
            "selected_text": request.selected_text
        }
        user_query = await db_service.create_user_query(query_data)
        
        # Search for relevant chunks in the vector database
        from src.services.embedding import embed_query
        query_embedding = await embed_query(request.query)
        
        relevant_chunks = search_chunks(
            query_embedding=query_embedding,
            book_id=request.book_id,
            top_k=request.top_k,
            threshold=request.relevance_threshold
        )
        
        # Generate response using the RAG pipeline
        response = await generate_response(
            query=request.query,
            context_chunks=relevant_chunks,
            query_id=user_query.id,
            selected_text=request.selected_text
        )
        
        # Save the response to the database
        response_data = {
            "query_id": user_query.id,
            "response_text": response.response_text,
            "sources": response.sources,
            "relevance_score": response.relevance_score,
            "model_used": response.model_used,
            "token_usage": response.token_usage,
            "citations": [c.dict() for c in response.citations]
        }
        await db_service.create_response(response_data)
        
        # Format the response according to the API contract
        api_response = QueryResponse(
            response=response.response_text,
            citations=response.citations,
            session_token=request.session_token,
            query_id=user_query.id,
            relevance_score=response.relevance_score
        )
        
        return api_response
        
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        logger.error(f"Error in query endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during query processing: {str(e)}"
        )


# Create the query-selected endpoint
@router.post("/query-selected", summary="Query restricted to user-selected text", response_model=QueryResponse)
async def query_selected_endpoint(
    request: QueryRequest,  # We can reuse the same model since it has optional selected_text
    x_api_key: str = Header(None)
):
    """
    Submit a query that is restricted to only the user-selected text, without broader retrieval.
    """
    try:
        # Validate API key
        if x_api_key != settings.API_KEY:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        # Validate that the book exists
        book = await db_service.get_book_content(request.book_id)
        if not book:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )
        
        # Validate query and selected text
        if not request.query.strip():
            raise HTTPException(
                status_code=400,
                detail="Query cannot be empty"
            )
        
        if not request.selected_text or not request.selected_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Selected text cannot be empty for this endpoint"
            )
        
        # Create a new chat session if one doesn't exist
        if not request.session_token:
            session_data = {
                "book_id": request.book_id,
                "session_token": str(uuid.uuid4()),
                "is_active": True
            }
            session = await db_service.create_chat_session(session_data)
            request.session_token = session.session_token
        else:
            # For now, we'll just use the provided session token
            # In a real implementation, you would validate and retrieve the session
            pass
        
        # Create user query record
        query_data = {
            "session_id": request.session_token,
            "query_text": request.query,
            "query_type": "SELECTED_TEXT",
            "selected_text": request.selected_text
        }
        user_query = await db_service.create_user_query(query_data)
        
        # For query-selected, we can create a context from the selected text
        # In a real implementation, you might want to find related chunks
        context_chunks = [{
            'content': request.selected_text,
            'chunk_id': 'selected_text_chunk',
            'page_number': 0,  # Placeholder
            'section_title': 'User Selected Text',  # Placeholder
        }]
        
        # Generate response using the selected text as context
        response = await generate_response(
            query=request.query,
            context_chunks=context_chunks,
            query_id=user_query.id,
            selected_text=request.selected_text
        )
        
        # Save the response to the database
        response_data = {
            "query_id": user_query.id,
            "response_text": response.response_text,
            "sources": response.sources,
            "relevance_score": response.relevance_score,
            "model_used": response.model_used,
            "token_usage": response.token_usage,
            "citations": [c.dict() for c in response.citations]
        }
        await db_service.create_response(response_data)
        
        # Format the response according to the API contract
        api_response = QueryResponse(
            response=response.response_text,
            citations=response.citations,
            session_token=request.session_token,
            query_id=user_query.id,
            relevance_score=response.relevance_score
        )
        
        return api_response
        
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        logger.error(f"Error in query-selected endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during query-selected processing: {str(e)}"
        )