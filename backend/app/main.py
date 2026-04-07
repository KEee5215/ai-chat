"""FastAPI 应用入口"""

import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from app.config.settings import get_settings
from app.api.v1.router import v1_router
from app.database.init_db import init_database

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    print(f"Starting {settings.APP_NAME}...")
    print(f"Model: {settings.DASHSCOPE_MODEL}")

    # 初始化数据库
    # await init_database()

    yield
    # 关闭时执行
    print("Shutting down...")


# 创建 FastAPI 应用
app = FastAPI(
    title=settings.APP_NAME,
    description="AI Chat Platform with LangChain and Alibaba Cloud DashScope",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS 配置
allow_origins = settings.ALLOW_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(v1_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": settings.APP_NAME}


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to AI Chat Platform",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
