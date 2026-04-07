"""API Key 服务"""

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.models.api_key import ApiKey, generate_api_key, hash_api_key
from app.schemas.api_key import ApiKeyCreate, ApiKeyResponse
from app.core.exceptions import NotFoundError


class ApiKeyService:
    """API Key 服务类"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_keys(self, user_id: str) -> List[ApiKey]:
        """获取用户的所有 API Keys"""
        result = await self.db.execute(
            select(ApiKey).where(ApiKey.user_id == uuid.UUID(user_id))
            .order_by(ApiKey.created_at.desc())
        )
        return list(result.scalars().all())

    async def create_key(self, user_id: str, name: str) -> tuple[str, ApiKey]:
        """
        创建新的 API Key

        Returns:
            (原始 key, 保存后的记录) - 注意：只有第一次返回时能看到完整 key
        """
        # 生成新的 API key
        raw_key, key_hash = generate_api_key()

        api_key = ApiKey(
            user_id=uuid.UUID(user_id),
            name=name,
            key_hash=key_hash,
        )

        self.db.add(api_key)
        await self.db.commit()
        await self.db.refresh(api_key)

        return raw_key, api_key

    async def get_key_by_id(self, key_id: str, user_id: str) -> Optional[ApiKey]:
        """根据 ID 获取 API Key"""
        result = await self.db.execute(
            select(ApiKey)
            .where(ApiKey.id == uuid.UUID(key_id), ApiKey.user_id == uuid.UUID(user_id))
        )
        return result.scalar_one_or_none()

    async def delete_key(self, key_id: str, user_id: str) -> bool:
        """删除 API Key"""
        result = await self.db.execute(
            select(ApiKey)
            .where(ApiKey.id == uuid.UUID(key_id), ApiKey.user_id == uuid.UUID(user_id))
        )
        api_key = result.scalar_one_or_none()

        if not api_key:
            return False

        await self.db.delete(api_key)
        await self.db.commit()
        return True

    async def update_last_used(self, key_id: str) -> None:
        """更新最后使用时间"""
        from datetime import datetime, timezone

        result = await self.db.execute(
            select(ApiKey).where(ApiKey.id == uuid.UUID(key_id))
        )
        api_key = result.scalar_one_or_none()

        if api_key:
            api_key.last_used_at = datetime.now(timezone.utc)
            await self.db.commit()
