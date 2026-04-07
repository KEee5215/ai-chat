"""Agent 服务 - LangChain Agent 核心"""

from typing import List, Optional, Dict, Any
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    BaseMessage,
)
from app.services.llm_service import LLMService
from app.agents.tools import TOOLS
from app.config.settings import get_settings


def convert_to_langchain_message(msg: Dict[str, Any]) -> BaseMessage:
    """将字典消息转换为 LangChain 消息对象"""
    role = msg.get("role", "user")
    content = msg.get("content", "")

    if role == "user":
        return HumanMessage(content=content)
    elif role == "assistant":
        return AIMessage(content=content)
    elif role == "system":
        return SystemMessage(content=content)
    else:
        return HumanMessage(content=content)


class AgentService:
    """LangChain Agent 服务"""

    def __init__(self):
        self.llm_service = LLMService()
        self.settings = get_settings()

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        use_tools: bool = True,
        max_iterations: int = 10
    ) -> tuple[str, int, Optional[List[Dict]]]:
        """
        Agent 对话

        Args:
            messages: 历史消息列表（字典格式）
            use_tools: 是否使用工具
            max_iterations: 最大迭代次数

        Returns:
            (回复内容，token 数量，工具调用列表)
        """
        # 转换消息格式
        langchain_messages = [convert_to_langchain_message(m) for m in messages]

        # 添加系统提示词
        from app.agents.prompts import SYSTEM_PROMPT
        system_msg = SystemMessage(content=SYSTEM_PROMPT)
        langchain_messages = [system_msg] + langchain_messages

        # 获取工具
        tools = TOOLS if use_tools else None

        # 调用 LLM（带工具或不带工具）
        if tools:
            response, tool_calls = await self.llm_service.call_with_tools(
                langchain_messages,
                tools=tools,
                max_iterations=max_iterations
            )
        else:
            response = await self.llm_service.invoke(langchain_messages)
            tool_calls = None

        # 计算 token 数
        tokens_used = self.llm_service.count_tokens(langchain_messages)

        return response, tokens_used, tool_calls

    async def stream_chat(
        self,
        messages: List[Dict[str, Any]]
    ):
        """
        流式对话

        Args:
            messages: 历史消息列表

        Yields:
            流式回复片段
        """
        langchain_messages = [convert_to_langchain_message(m) for m in messages]
        system_msg = SystemMessage(content="You are a helpful AI assistant.")
        langchain_messages = [system_msg] + langchain_messages

        async for chunk in self.llm_service.stream_invoke(langchain_messages):
            yield chunk
