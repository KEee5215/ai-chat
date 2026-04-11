"""聊天服务"""

import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from typing import List, Optional

from app.models.chat_session import ChatSession, Message
from app.models.user import User
from app.schemas.chat import ChatSessionCreate, MessageCreate
from app.services.agent_service import AgentService
from app.core.exceptions import NotFoundError


class ChatService:
    """聊天服务类"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.agent_service = AgentService()

    async def get_sessions(self, user_id: str) -> List[ChatSession]:
        """获取用户的所有会话"""
        result = await self.db.execute(
            select(ChatSession)
            .where(ChatSession.user_id == uuid.UUID(user_id))
            .order_by(ChatSession.created_at.desc())
        )
        return list(result.scalars().all())

    async def create_session(self, user_id: str, title: Optional[str] = None) -> ChatSession:
        """创建新会话"""
        session_title = title or "新对话"
        session = ChatSession(user_id=uuid.UUID(user_id), title=session_title)

        self.db.add(session)
        await self.db.commit()
        await self.db.refresh(session)
        return session

    async def get_session(self, session_id: str, user_id: str) -> ChatSession:
        """获取指定会话"""
        result = await self.db.execute(
            select(ChatSession)
            .where(ChatSession.id == uuid.UUID(session_id), ChatSession.user_id == uuid.UUID(user_id))
        )
        return result.scalar_one_or_none()

    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        tokens_used: int = 0
    ) -> Message:
        """添加消息到会话"""
        message = Message(
            session_id=uuid.UUID(session_id),
            role=role,
            content=content,
            tokens_used=tokens_used,
        )

        self.db.add(message)
        await self.db.flush()  # 获取 ID

        # 更新会话的 updated_at
        result = await self.db.execute(
            select(ChatSession).where(ChatSession.id == uuid.UUID(session_id))
        )
        session = result.scalar_one_or_none()
        if session:
            session.updated_at = datetime.now(timezone.utc)

        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_messages(self, session_id: str) -> List[Message]:
        """获取会话的所有消息"""
        result = await self.db.execute(
            select(Message)
            .where(Message.session_id == uuid.UUID(session_id))
            .order_by(Message.created_at.asc())
        )
        return list(result.scalars().all())

    async def chat(
        self,
        session_id: str,
        user_message: str,
        user_id: str
    ) -> tuple[Message, Message]:
        """
        处理用户消息并保存对话结果

        Returns:
            (用户消息对象，AI 回复消息对象)
        """
        # 获取会话和用户
        session = await self.get_session(session_id, user_id)
        if not session:
            raise NotFoundError(detail="Session not found")

        # 添加用户消息
        user_msg = await self.add_message(
            session_id=session_id,
            role="user",
            content=user_message,
            tokens_used=0
        )

        # 获取历史消息
        messages = await self.get_messages(session_id)

        # 准备 Agent 输入
        message_dicts = [
            {
                "role": msg.role,
                "content": msg.content,
            }
            for msg in messages
        ]

        # 调用 Agent
        ai_response, tokens_used, tool_calls = await self.agent_service.chat(message_dicts)

        # 保存 AI 回复
        ai_msg = await self.add_message(
            session_id=session_id,
            role="assistant",
            content=ai_response,
            tokens_used=tokens_used
        )

        # 更新会话标题（如果是第一条消息）
        if len(messages) == 1 and session.title == "新对话":
            # 重新查询 session 以确保它仍然 attached 到当前事务
            result = await self.db.execute(
                select(ChatSession).where(ChatSession.id == uuid.UUID(session_id))
            )
            current_session = result.scalar_one_or_none()
            if current_session:
                current_session.title = user_message[:50]
                await self.db.commit()

        return user_msg, ai_msg
