"""测试数据库连接脚本"""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.config.settings import get_settings

settings = get_settings()

print(f"数据库 URL: {settings.DATABASE_URL}")


async def test_connection():
    """测试数据库连接"""
    print("\n正在尝试连接数据库...")

    # 创建一个新引擎用于测试
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,  # 显示 SQL 日志
        pool_pre_ping=True,
    )

    try:
        async with engine.connect() as conn:
            print("\n数据库连接成功！")
            result = await conn.execute("SELECT version();")
            version = result.scalar()
            print(f"PostgreSQL 版本：{version}")
            return True
    except Exception as e:
        print(f"\n数据库连接失败：{e}")
        print("\n可能的原因：")
        print("1. PostgreSQL 服务未启动")
        print("2. 数据库名称 'ai_chat_db' 不存在")
        print("3. 用户名或密码错误")
        print("4. 端口 5432 被占用或防火墙阻止")
        return False
    finally:
        await engine.dispose()


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    if not success:
        print("\n请确保:")
        print("1. PostgreSQL 服务正在运行")
        print("2. 数据库 'ai_chat_db' 已创建")
        print("3. 用户 'postgres' 密码为 'postgres'")
        print("\n创建数据库命令（PostgreSQL）:")
        print("  CREATE DATABASE ai_chat_db;")
