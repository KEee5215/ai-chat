from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import hashlib
import secrets

from app.database.session import Base


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    key_hash = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    last_used_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系（延迟加载）
    user = relationship("User", back_populates="api_keys")


def generate_api_key(prefix: str = "sk_") -> tuple[str, str]:
    """
    生成新的 API Key
    返回：(原始 key, 哈希值)
    """
    raw_key = f"{prefix}{secrets.token_urlsafe(32)}"
    hash_value = hash_api_key(raw_key)
    return raw_key, hash_value


def hash_api_key(raw_key: str) -> str:
    """对 API Key 进行哈希"""
    return hashlib.sha256(raw_key.encode()).hexdigest()


def verify_api_key(raw_key: str, stored_hash: str) -> bool:
    """验证 API Key"""
    return secrets.compare_digest(hash_api_key(raw_key), stored_hash)
