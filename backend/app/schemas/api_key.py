from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ApiKeyBase(BaseModel):
    name: str


class ApiKeyCreate(ApiKeyBase):
    pass


class ApiKeyResponse(BaseModel):
    id: str
    name: str
    key_preview: str  # 只显示前几个字符
    last_used_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ApiKeyListResponse(BaseModel):
    keys: list[ApiKeyResponse]
