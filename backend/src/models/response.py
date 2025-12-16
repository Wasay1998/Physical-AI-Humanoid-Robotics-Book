from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class QueryType(str, Enum):
    FULL_BOOK = "FULL_BOOK"
    SELECTED_TEXT = "SELECTED_TEXT"


class UserQueryBase(BaseModel):
    session_id: str  # UUID as string
    query_text: str = Field(..., min_length=1, description="The original query text from the user")
    selected_text: Optional[str] = Field(None, description="Text selected by the user (for selected-text queries)")
    query_type: QueryType = Field(..., description="Type of query (FULL_BOOK, SELECTED_TEXT)")


class UserQueryCreate(UserQueryBase):
    pass


class UserQueryUpdate(BaseModel):
    query_text: Optional[str] = None
    selected_text: Optional[str] = None


class UserQuery(UserQueryBase):
    id: str  # UUID as string
    query_embedding: Optional[str] = Field(None, description="Vector representation of the query")
    query_timestamp: datetime
    response_id: Optional[str] = Field(None, description="Reference to the corresponding response")

    class Config:
        from_attributes = True


class Citation(BaseModel):
    chunk_id: str = Field(..., description="ID of the content chunk used")
    page_number: int = Field(..., description="Page number where the information appears in the original book")
    section_title: str = Field(..., description="Title of the section where the information appears")
    text_preview: str = Field(..., description="Brief preview of the cited text")


class ResponseBase(BaseModel):
    query_id: str  # UUID as string
    response_text: str = Field(..., min_length=1, description="The generated response text")


class ResponseCreate(ResponseBase):
    pass


class ResponseUpdate(BaseModel):
    relevance_score: Optional[float] = None


class Response(ResponseBase):
    id: str  # UUID as string
    generated_at: datetime
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="List of source chunks used to generate the response")
    relevance_score: float = Field(ge=0.0, le=1.0, description="Relevance score (0.0 to 1.0)")
    model_used: str = Field(..., description="Name of the model used (e.g., command-r-plus)")
    token_usage: Optional[Dict[str, Any]] = Field(None, description="Information about token usage")
    citations: List[Citation] = Field(default_factory=list, description="List of citations with page numbers and section titles")

    class Config:
        from_attributes = True


class QueryContextBase(BaseModel):
    query_id: str  # UUID as string
    relevance_threshold: float = Field(ge=0.0, le=1.0, default=0.7, description="Threshold used for filtering relevant chunks")
    top_k: int = Field(gt=0, default=6, description="Number of top results retrieved")


class QueryContextCreate(QueryContextBase):
    pass


class QueryContextUpdate(BaseModel):
    relevance_threshold: Optional[float] = None
    top_k: Optional[int] = None


class QueryContext(QueryContextBase):
    id: str  # UUID as string
    chunks_retrieved: List[str] = Field(default_factory=list, description="List of chunk IDs retrieved for the query")
    context_text: str = Field(..., description="Combined text of all relevant chunks")
    context_embedding: Optional[str] = Field(None, description="Vector representation of the context")
    preprocessing_notes: Optional[str] = Field(None, description="Notes about how the context was prepared")

    class Config:
        from_attributes = True