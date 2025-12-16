from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import Optional
import uuid
import tempfile
import os
from src.config.settings import settings
from src.config.logging import get_logger
from src.services.ingestion import ingest_book


router = APIRouter()
logger = get_logger(__name__)


@router.post("/ingest", summary="Ingest a book for RAG processing")
async def ingest_endpoint(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: str = Form(...),
    chunk_size: Optional[int] = Form(settings.CHUNK_SIZE_TOKENS),
    overlap_size: Optional[int] = Form(settings.OVERLAP_SIZE_TOKENS)
):
    """
    Upload and process a book file to enable querying via the RAG system.
    """
    try:
        # Validate file format
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in [".pdf", ".epub", ".txt"]:
            raise HTTPException(
                status_code=415,
                detail="File format not supported. Supported formats: PDF, ePub, TXT"
            )
        
        # Create a temporary file to save the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            # Write the uploaded file content to the temporary file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Perform the ingestion
            result = await ingest_book(
                file_path=temp_file_path,
                title=title,
                author=author,
                content_format=file_extension[1:],  # Remove the dot from extension
                chunk_size=chunk_size,
                overlap_size=overlap_size
            )
            
            return result
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        logger.error(f"Error in ingest endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during book ingestion: {str(e)}"
        )