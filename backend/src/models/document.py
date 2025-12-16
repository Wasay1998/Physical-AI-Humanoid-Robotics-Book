from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid


class BookStatus(str, Enum):
    PENDING = "PENDING"
    INGESTING = "INGESTING"
    INDEXED = "INDEXED"
    FAILED = "FAILED"


class BookContentBase(BaseModel):
    title: str = Field(..., description="Title of the book")
    author: str = Field(..., description="Author of the book")
    isbn: Optional[str] = Field(None, description="ISBN identifier")
    content_format: str = Field(..., description="Format of the book (PDF, ePub, TXT, etc.)")


class BookContentCreate(BookContentBase):
    pass


class BookContentUpdate(BaseModel):
    status: Optional[BookStatus] = None
    total_chunks: Optional[int] = None


class BookContent(BookContentBase):
    id: str  # UUID as string
    upload_date: datetime
    status: BookStatus
    total_chunks: int
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True


class ContentChunkBase(BaseModel):
    book_id: str  # UUID as string
    content: str = Field(..., description="The actual text content of the chunk", max_length=512*4)  # Approximate 512 tokens
    page_number: Optional[int] = Field(None, description="Original page number in the source document")
    section_title: Optional[str] = Field(None, description="Title of the section this chunk belongs to")
    position: int = Field(..., ge=0, description="Position in the original text (character offset)")
    token_count: int = Field(..., ge=0, description="Number of tokens in the chunk")


class ContentChunkCreate(ContentChunkBase):
    pass


class ContentChunkUpdate(BaseModel):
    page_number: Optional[int] = None
    section_title: Optional[str] = None


class ContentChunk(ContentChunkBase):
    id: str  # UUID as string
    chunk_id: str  # Sequential identifier within the book (e.g., "chunk_001")
    vector_id: str  # Identifier in the vector database (Qdrant)
    hash: str  # Hash of content for deduplication purposes

    class Config:
        from_attributes = True