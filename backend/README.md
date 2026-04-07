# AI Chat Platform

基于 LangChain + FastAPI + PostgreSQL 的 AI 聊天机器人后端，使用阿里云百炼平台 API（qwen3.5-122b-a10b）。

## 功能特性

- 用户注册/登录（JWT 认证）
- 多会话管理
- 流式对话响应
- Agent 工具调用（计算器、搜索）
- 用户 API Key 管理

## 技术栈

- **Web 框架**: FastAPI
- **AI 框架**: LangChain
- **数据库**: PostgreSQL + SQLAlchemy (Async)
- **LLM**: 阿里云百炼 DashScope API
- **认证**: JWT

## 快速开始

### 1. 环境要求

- Python 3.10+
- PostgreSQL 12+
- 阿里云 DashScope API Key

### 2. 安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 配置环境变量

编辑 `.env` 文件：

```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/ai_chat_db
DASHSCOPE_API_KEY=your_api_key_here
SECRET_KEY=your-secret-key-here
```

### 4. 初始化数据库

```bash
# 创建数据库
createdb ai_chat_db

# 运行迁移（如果使用了 Alembic）
alembic upgrade head
```

### 5. 启动服务

```bash
uvicorn app.main:app --reload
```

访问 http://localhost:8000/docs 查看 API 文档。

## API 端点

### 认证

- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/auth/me` - 获取当前用户

### 聊天

- `GET /api/v1/chats/sessions` - 获取会话列表
- `POST /api/v1/chats/sessions` - 创建新会话
- `GET /api/v1/chats/sessions/{id}` - 获取会话详情
- `POST /api/v1/chats/sessions/{id}/messages` - 发送消息
- `POST /api/v1/chats/sessions/{id}/messages/stream` - 流式对话

### API Key 管理

- `GET /api/v1/api-keys` - 列出 API Keys
- `POST /api/v1/api-keys` - 创建 API Key
- `DELETE /api/v1/api-keys/{id}` - 删除 API Key

## 项目结构

```
backend/
├── app/
│   ├── api/          # API 路由层
│   ├── agents/       # LangChain Agent 核心
│   ├── config/       # 配置文件
│   ├── core/         # 核心工具（安全、异常）
│   ├── database/     # 数据库连接
│   ├── models/       # SQLAlchemy 模型
│   ├── schemas/      # Pydantic Schema
│   └── services/     # 业务逻辑层
├── alembic/          # 数据库迁移
├── tests/            # 测试
├── .env              # 环境变量
└── requirements.txt  # 依赖
```
