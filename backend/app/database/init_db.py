"""数据库初始化脚本"""

import asyncio
from sqlalchemy.ext.asyncio import AsyncEngine
from app.database.session import engine, Base
from app.models import User, ChatSession, Message, ApiKey


async def init_database():
    """初始化数据库表"""
    print("正在连接数据库...")

    try:
        # 测试连接
        async with engine.connect() as conn:
            print("数据库连接成功！")

        # 创建所有表
        print("正在创建数据表...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        print("数据表创建成功！")
        print("- users")
        print("- chat_sessions")
        print("- messages")
        print("- api_keys")

    except Exception as e:
        print(f"数据库初始化失败：{e}")
        raise


async def drop_all_tables():
    """删除所有表（危险操作！）"""
    print("警告：正在删除所有数据表...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("所有表已删除")


if __name__ == "__main__":
    asyncio.run(init_database())
