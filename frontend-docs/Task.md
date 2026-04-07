## 技术栈

前端 (Client): React (Vite) + TailwindCSS (样式) + Lucide React (图标) + fetch (处理流式响应) + redux(路由)。

## 任务

根据 openapi.json中的后端api接口构建前端界面,包括完整的功能

## 页面

- 用户注册登录界面
- 对话主界面
- 管理apikey的界面
- 你觉得缺失的页面
- 404页面

## 接口

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
