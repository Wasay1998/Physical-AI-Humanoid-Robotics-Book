"""
Ingestion service for processing and indexing book content.
"""
import uuid
import hashlib
from typing import List, Dict, Any, Tuple
from pathlib import Path
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None
try:
    from ebooklib import epub
except ImportError:
    epub = None
import asyncio
import tempfile
from src.config.logging import get_logger
from src.config.settings import settings
from src.services.embedding import generate_embeddings
from src.services.retrieval import store_content_chunks
from src.services.database import db_service
from src.models.document import BookContent, ContentChunk


logger = get_logger(__name__)


def calculate_chunk_hash(content: str) -> str:
    """Calculate a hash for content deduplication purposes."""
    return hashlib.sha256(content.encode()).hexdigest()


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 150) -> List[Dict[str, Any]]:
    """
    Split text into overlapping chunks of specified size.

    Args:
        text: The text to chunk
        chunk_size: Maximum size of each chunk in tokens (approximate)
        overlap: Number of tokens to overlap between chunks

    Returns:
        List of chunk dictionaries with content and metadata
    """
    # For a more accurate tokenization, we can use Cohere's token counting
    # but for now, we'll use a simple approach that approximates tokens
    # (typically 1 token ≈ 4 characters or 0.75 words in English)
    import re

    # Split text by sentence boundaries first, to avoid cutting sentences
    sentences = re.split(r'[.!?]+\s+', text)
    chunks = []
    current_chunk = ""
    current_position = 0

    for sentence in sentences:
        # Check if adding this sentence would exceed the chunk size
        if len(current_chunk) + len(sentence) > chunk_size * 4:  # Approximate character count for token limit
            if current_chunk.strip():
                # Save the current chunk
                chunks.append({
                    "content": current_chunk.strip(),
                    "position": current_position,
                    "token_count": len(current_chunk.split()),  # Approximate token count
                    "hash": calculate_chunk_hash(current_chunk.strip())
                })

                # Start a new chunk, possibly with overlap from the previous chunk
                if overlap > 0:
                    # Find overlapping words from the end of the current chunk
                    words = current_chunk.split()
                    overlap_words = words[-int(overlap):] if len(words) > overlap else words
                    current_chunk = " ".join(overlap_words) + " " + sentence
                else:
                    current_chunk = sentence
            else:
                # If the sentence itself is too long, we need to split it
                chunks.extend(split_long_sentence(sentence, chunk_size, overlap))
        else:
            current_chunk += sentence + ". "  # Add back the sentence ending

    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append({
            "content": current_chunk.strip(),
            "position": current_position,
            "token_count": len(current_chunk.split()),  # Approximate token count
            "hash": calculate_chunk_hash(current_chunk.strip())
        })

    return chunks


def split_long_sentence(sentence: str, chunk_size: int, overlap: int) -> List[Dict[str, Any]]:
    """
    Split a long sentence into smaller chunks.

    Args:
        sentence: The long sentence to split
        chunk_size: Maximum size of each chunk in tokens (approximate)
        overlap: Number of tokens to overlap between chunks

    Returns:
        List of chunk dictionaries with content and metadata
    """
    import re

    # Split the sentence into words
    words = sentence.split()
    chunks = []
    current_chunk_words = []
    start_pos = 0

    for word in words:
        current_chunk_words.append(word)

        # If the current chunk exceeds the size limit
        if len(current_chunk_words) >= chunk_size:
            chunk_content = " ".join(current_chunk_words)
            chunks.append({
                "content": chunk_content,
                "position": start_pos,
                "token_count": len(current_chunk_words),
                "hash": calculate_chunk_hash(chunk_content)
            })

            # Start a new chunk with overlap, if specified
            if overlap > 0:
                overlap_start = len(current_chunk_words) - overlap
                current_chunk_words = current_chunk_words[overlap_start:]
                start_pos += len(" ".join(current_chunk_words[:overlap_start]))
            else:
                current_chunk_words = []
                start_pos += len(chunk_content)

    # Add the last chunk if there are remaining words
    if current_chunk_words:
        chunk_content = " ".join(current_chunk_words)
        chunks.append({
            "content": chunk_content,
            "position": start_pos,
            "token_count": len(current_chunk_words),
            "hash": calculate_chunk_hash(chunk_content)
        })

    return chunks


async def process_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text content
    """
    try:
        if PyPDF2 is None:
            raise ImportError("PyPDF2 is required to process PDF files")

        text_content = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text() + "\n"

        logger.info(f"Extracted text from PDF: {file_path}")
        return text_content
    except Exception as e:
        logger.error(f"Error processing PDF file {file_path}: {str(e)}")
        raise


async def process_epub(file_path: str) -> str:
    """
    Extract text content from an EPUB file.

    Args:
        file_path: Path to the EPUB file

    Returns:
        Extracted text content
    """
    try:
        if epub is None:
            raise ImportError("ebooklib is required to process EPUB files")

        book = epub.read_epub(file_path)
        text_content = ""

        for item in book.get_items():
            if item.get_type() == epub.EpubHtml:
                # Decode the content and extract text
                content = item.get_content().decode('utf-8')
                # Simple HTML tag removal (in a real implementation, use BeautifulSoup)
                import re
                clean_text = re.sub(r'<[^>]+>', '', content)
                text_content += clean_text + "\n"

        logger.info(f"Extracted text from EPUB: {file_path}")
        return text_content
    except Exception as e:
        logger.error(f"Error processing EPUB file {file_path}: {str(e)}")
        raise


async def process_text(file_path: str) -> str:
    """
    Extract text content from a plain text file.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        Text content
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
        
        logger.info(f"Extracted text from TXT file: {file_path}")
        return text_content
    except Exception as e:
        logger.error(f"Error processing text file {file_path}: {str(e)}")
        raise


async def process_book_content(
    book_id: str,
    content: str,
    chunk_size: int = 512,
    overlap_size: int = 150
) -> List[Dict[str, Any]]:
    """
    Process book content by chunking and generating embeddings.

    Args:
        book_id: ID of the book being processed
        content: The raw text content of the book
        chunk_size: Maximum size of each chunk in tokens
        overlap_size: Number of tokens to overlap between chunks

    Returns:
        List of chunk data with embeddings
    """
    try:
        # Chunk the content
        chunks = chunk_text(content, chunk_size, overlap_size)

        # Prepare chunks with additional metadata
        chunks_with_metadata = []
        for i, chunk in enumerate(chunks):
            chunk_with_metadata = {
                **chunk,
                "chunk_id": f"chunk_{i:03d}",
                "vector_id": str(uuid.uuid4()),  # Generate a unique ID for the vector
                "book_id": book_id,
                "page_number": None,  # Will need to derive from source if available
                "section_title": None  # Will need to derive from source if available
            }
            chunks_with_metadata.append(chunk_with_metadata)

        # Extract just the content for embedding
        contents = [chunk["content"] for chunk in chunks_with_metadata]

        # Generate embeddings for all chunks
        logger.info(f"Generating embeddings for {len(contents)} chunks...")
        embeddings = await generate_embeddings(contents)

        # Associate embeddings with chunks
        chunks_with_embeddings = []
        for i, chunk in enumerate(chunks_with_metadata):
            chunk_with_embedding = {**chunk, "embedding": embeddings[i]}
            chunks_with_embeddings.append(chunk_with_embedding)

        logger.info(f"Processed and embedded {len(chunks_with_embeddings)} chunks for book {book_id}")
        return chunks_with_embeddings

    except Exception as e:
        logger.error(f"Error processing book content: {str(e)}")
        raise


async def ingest_book(
    file_path: str,
    title: str,
    author: str,
    content_format: str,
    chunk_size: int = settings.CHUNK_SIZE_TOKENS,
    overlap_size: int = settings.OVERLAP_SIZE_TOKENS
) -> Dict[str, Any]:
    """
    Main ingestion function that processes a book file and stores it for RAG.
    
    Args:
        file_path: Path to the book file
        title: Title of the book
        author: Author of the book
        content_format: Format of the content (pdf, epub, txt)
        chunk_size: Size of text chunks
        overlap_size: Overlap size between chunks
        
    Returns:
        Dictionary with ingestion results
    """
    try:
        # Create book record in database
        book_data = {
            "title": title,
            "author": author,
            "content_format": content_format,
            "status": "INGESTING",
            "total_chunks": 0  # Will update after processing
        }
        
        book_record = await db_service.create_book_content(book_data)
        book_id = book_record.id
        logger.info(f"Created book record for '{title}' with ID: {book_id}")
        
        # Process the file based on its format
        if content_format.lower() == "pdf":
            content = await process_pdf(file_path)
        elif content_format.lower() == "epub":
            content = await process_epub(file_path)
        elif content_format.lower() in ["txt", "text"]:
            content = await process_text(file_path)
        else:
            raise ValueError(f"Unsupported content format: {content_format}")
        
        # Process the content (chunk and embed)
        chunks_with_embeddings = await process_book_content(
            book_id, content, chunk_size, overlap_size
        )

        # Store chunks in vector database (Qdrant)
        embeddings_only = [chunk["embedding"] for chunk in chunks_with_embeddings]
        chunks_data_only = [{k: v for k, v in chunk.items() if k != "embedding"}
                           for chunk in chunks_with_embeddings]

        store_content_chunks(chunks_data_only, embeddings_only, book_id)
        logger.info(f"Stored {len(chunks_data_only)} chunks in vector database for book {book_id}")
        
        # Update book record with final status and chunk count
        await db_service.update_book_content(
            book_id, 
            {"status": "INDEXED", "total_chunks": len(chunks_data_only)}
        )
        logger.info(f"Updated book {book_id} status to INDEXED with {len(chunks_data_only)} chunks")
        
        # Return ingestion results
        return {
            "message": "Book ingestion completed successfully",
            "book_id": book_id,
            "status": "INDEXED",
            "total_chunks": len(chunks_data_only)
        }
        
    except Exception as e:
        logger.error(f"Error ingesting book: {str(e)}")
        # Update book status to FAILED
        if 'book_id' in locals():
            await db_service.update_book_content(book_id, {"status": "FAILED"})
        raise