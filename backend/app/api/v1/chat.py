"""聊天相关路由"""

import json
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.dialects.postgresql import UUID

from app.api.deps import CurrentUser, DbSession
from app.schemas.chat import (
    ChatSessionCreate,
    ChatSessionResponse,
    MessageCreate,
    MessageResponse,
    ChatCompletionResponse,
)
from app.services.chat_service import ChatService
from app.core.exceptions import NotFoundError

router = APIRouter(prefix="/chats", tags=["聊天"])


@router.get("/sessions", response_model=list[dict])
async def list_sessions(
    current_user: CurrentUser,
    db: DbSession
):
    """获取用户的所有会话列表"""
    from app.services.chat_service import ChatService

    chat_service = ChatService(db)
    sessions = await chat_service.get_sessions(str(current_user.id))

    return [
        {
            "id": str(session.id),
            "title": session.title,
            "created_at": session.created_at,
            "updated_at": session.updated_at,
        }
        for session in sessions
    ]


@router.post("/sessions", response_model=ChatSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: ChatSessionCreate,
    current_user: CurrentUser,
    db: DbSession
):
    """创建新会话"""
    chat_service = ChatService(db)
    session = await chat_service.create_session(
        user_id=str(current_user.id),
        title=session_data.title
    )

    # 加载消息
    messages = await chat_service.get_messages(str(session.id))
    
    # 将 ORM 消息对象转换为 Pydantic schema
    message_responses = [
        MessageResponse(
            id=str(msg.id),
            session_id=str(msg.session_id),
            role=msg.role,
            content=msg.content,
            tokens_used=msg.tokens_used,
            created_at=msg.created_at,
        )
        for msg in messages
    ]
    
    return ChatSessionResponse(
        id=str(session.id),
        user_id=str(session.user_id),
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        messages=message_responses,
    )


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_session(
    session_id: str,
    current_user: CurrentUser,
    db: DbSession
):
    """获取指定会话的详情和消息"""
    chat_service = ChatService(db)
    session = await chat_service.get_session(session_id, str(current_user.id))

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    messages = await chat_service.get_messages(session_id)
    
    # 将 ORM 消息对象转换为 Pydantic schema
    message_responses = [
        MessageResponse(
            id=str(msg.id),
            session_id=str(msg.session_id),
            role=msg.role,
            content=msg.content,
            tokens_used=msg.tokens_used,
            created_at=msg.created_at,
        )
        for msg in messages
    ]

    return ChatSessionResponse(
        id=str(session.id),
        user_id=str(session.user_id),
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        messages=message_responses,
    )


@router.post("/sessions/{session_id}/messages")
async def send_message(
    session_id: str,
    message_data: MessageCreate,
    current_user: CurrentUser,
    db: DbSession
):
    """发送消息并获取 AI 回复"""
    chat_service = ChatService(db)

    try:
        # 处理对话
        user_msg, ai_msg = await chat_service.chat(
            session_id=session_id,
            user_message=message_data.content,
            user_id=str(current_user.id)
        )

        return ChatCompletionResponse(
            message=ai_msg.content,
            tokens_used=ai_msg.tokens_used,
            session_id=str(session_id),
        )

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e.detail))


@router.post("/sessions/{session_id}/messages/stream")
async def stream_message(
    session_id: str,
    message_data: MessageCreate,
    current_user: CurrentUser,
    db: DbSession
):
    """流式发送消息"""
    chat_service = ChatService(db)

    async def generate():
        try:
            # 添加用户消息
            user_msg = await chat_service.add_message(
                session_id=session_id,
                role="user",
                content=message_data.content,
                tokens_used=0
            )

            # 获取历史消息
            messages = await chat_service.get_messages(session_id)
            message_dicts = [{"role": msg.role, "content": msg.content} for msg in messages]

            # 流式获取 AI 回复
            async for chunk in chat_service.agent_service.stream_chat(message_dicts):
                yield f"data: {json.dumps({'content': chunk})}\n\n"

            # 保存 AI 回复（这里简化处理）
            full_response = ""
            # 注意：实际应用中需要重新获取完整的响应

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
