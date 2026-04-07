from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatSessionBase(BaseModel):
    title: Optional[str] = None


class ChatSessionCreate(ChatSessionBase):
    pass


class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    pass


class MessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    tokens_used: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionWithMessages(ChatSessionBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True


class ChatSessionResponse(ChatSessionWithMessages):
    pass


class ChatSessionListResponse(BaseModel):
    sessions: List[ChatSessionBase]


class ChatCompletionResponse(BaseModel):
    message: str
    tokens_used: int
    session_id: str
    tool_calls: Optional[List[dict]] = None
