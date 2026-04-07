"""API v1 路由聚合"""

from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.chat import router as chat_router
from app.api.v1.api_keys import router as api_keys_router

# 主路由
v1_router = APIRouter()

# 注册子路由
v1_router.include_router(auth_router)
v1_router.include_router(chat_router)
v1_router.include_router(api_keys_router)

__all__ = ["v1_router"]
