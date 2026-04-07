"""LLM 服务 - 阿里云百炼 API 封装"""

import os
from typing import Generator, Optional, List, Dict, Any
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    BaseMessage,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatOpenAI
from langchain_core.outputs import LLMResult
import json

from app.config.settings import get_settings


class LLMService:
    """阿里云百炼 LLM 服务封装"""

    def __init__(self):
        self.settings = get_settings()
        self.model_name = self.settings.DASHSCOPE_MODEL

        # 初始化 OpenAI 兼容的聊天模型
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=0.7,
            streaming=True,
            base_url=self.settings.DASHSCOPE_BASE_URL,
            api_key=self.settings.DASHSCOPE_API_KEY,
        )

    async def invoke(self, messages: List[BaseMessage]) -> str:
        """
        发送消息并获取回复

        Args:
            messages: 消息列表

        Returns:
            AI 回复内容
        """
        response = await self.llm.ainvoke(messages)
        return response.content

    async def stream_invoke(self, messages: List[BaseMessage]) -> Generator[str, None, None]:
        """
        流式发送消息

        Args:
            messages: 消息列表

        Yields:
            流式回复片段
        """
        async for chunk in self.llm.astream(messages):
            content = chunk.content if hasattr(chunk, 'content') else ""
            yield content

    async def call_with_tools(
        self,
        messages: List[BaseMessage],
        tools: Optional[List] = None,
        max_iterations: int = 10
    ) -> tuple[str, Optional[List[Dict]]]:
        """
        LLM 调用（支持工具）

        Args:
            messages: 消息列表
            tools: 可用的工具列表
            max_iterations: 最大迭代次数

        Returns:
            (最终回复，工具调用列表)
        """
        # 暂时不使用复杂工具调用，直接使用 LLM 的基本调用
        # DashScope API 通过 bind_tools 支持函数调用
        if tools:
            try:
                llm_with_tools = self.llm.bind_tools(tools)
                response = await llm_with_tools.ainvoke(messages)

                # 检查是否有工具调用
                tool_calls = getattr(response, 'tool_calls', [])
                if tool_calls:
                    # 如果有工具调用，简单返回第一个工具的参数
                    first_tool = tool_calls[0]
                    return f"Tool called: {first_tool['name']}", [first_tool]

                return response.content if hasattr(response, 'content') else str(response), []
            except Exception as e:
                # 如果 bind_tools 失败，回退到普通调用
                print(f"Tool binding failed: {e}, falling back to basic call")

        # 普通调用
        response = await self.invoke(messages)
        return response, None

    def count_tokens(self, messages: List[BaseMessage]) -> int:
        """估算 token 数量"""
        text_content = ""
        for msg in messages:
            if isinstance(msg.content, str):
                text_content += msg.content
            elif isinstance(msg.content, list):
                for item in msg.content:
                    if isinstance(item, dict) and item.get("type") == "text":
                        text_content += item.get("text", "")

        # 简单的 token 估算（约每 4 个字符一个 token）
        return len(text_content) // 4
