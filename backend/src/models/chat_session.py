from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class ChatSessionBase(BaseModel):
    book_id: str  # UUID as string
    session_token: Optional[str] = Field(None, description="Unique token for session identification")
    user_id: Optional[str] = Field(None, description="Optional reference to authenticated user")


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(BaseModel):
    is_active: Optional[bool] = None
    last_activity: Optional[datetime] = None


class ChatSession(ChatSessionBase):
    id: str  # UUID as string
    created_at: datetime
    last_activity: datetime
    is_active: bool
    metadata: Optional[dict] = None

    class Config:
        from_attributes = True