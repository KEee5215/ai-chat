"""创建数据库脚本 - 连接到 default 数据库来创建新数据库"""

import asyncio
import asyncpg


async def create_database():
    """创建数据库（如果不存在）"""
    # 连接到 postgres 默认数据库
    conn = await asyncpg.connect(
        host="localhost",
        port=5432,
        user="postgres",
        password="postgres"
    )

    try:
        # 检查数据库是否存在
        result = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = 'ai_chat_db'"
        )

        if result:
            print("数据库 'ai_chat_db' 已存在")
        else:
            # 创建数据库
            await conn.execute("CREATE DATABASE ai_chat_db;")
            print("数据库 'ai_chat_db' 创建成功！")

    except Exception as e:
        print(f"错误：{e}")
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(create_database())
