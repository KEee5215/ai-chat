# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AI Chat Platform backend using FastAPI + LangChain + PostgreSQL. The application provides a chat API with AI agent capabilities (calculator, search tools) powered by Alibaba Cloud DashScope API (qwen3.5-122b-a10b).

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run production server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run tests
pytest
pytest-asyncio
```

## Architecture

**Layered Architecture Pattern:**

```
app/
├── api/v1/        # FastAPI routers (auth, chat, api_keys)
├── agents/        # LangChain tools and prompts
├── services/      # Business logic layer
├── models/        # SQLAlchemy ORM models
├── schemas/       # Pydantic schemas for validation
├── core/          # Security, exceptions, settings
└── database/      # DB connection and session management
```

**Key Patterns:**
- Dependency injection via `app/api/deps.py` (`CurrentUser`, `DbSession`)
- Async database sessions with SQLAlchemy 2.0 (`AsyncSession`)
- JWT authentication via OAuth2PasswordBearer
- API versioning under `/api/v1`

**Service Layer:**
- `ChatService` - Manages chat sessions and messages
- `UserService` - User registration/authentication
- `AgentService` - LangChain agent orchestration
- `ApiKeyService` - User API key management

**Configuration:**
- Environment variables via `python-dotenv` (`.env` file)
- Settings managed in `app/config/settings.py` using `pydantic-settings`

## API Endpoints

- `/api/v1/auth/*` - User registration, login, me
- `/api/v1/chats/*` - Session management, messaging, streaming
- `/api/v1/api-keys/*` - API key CRUD
- `/health` - Health check
