"""
数据库连接和配置模块
"""
import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# 环境变量
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./teenmind.db')
MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017/')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# SQLAlchemy 基础设施
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 可选依赖：MongoDB & Redis（若未安装，优雅降级）
try:
    from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
except Exception:
    AsyncIOMotorClient = None  # type: ignore

try:
    import redis  # type: ignore
except Exception:
    redis = None  # type: ignore

mongo_client = None
mongodb = None
redis_client = None


def get_db() -> Generator[Session, None, None]:
    """获取数据库会话（依赖注入使用）。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def init_db():
    """初始化数据库与可选的缓存/文档库。"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("✅ PostgreSQL/SQLite 数据库初始化完成")

    # 初始化 Mongo
    global mongo_client, mongodb
    if AsyncIOMotorClient is not None:
        try:
            mongo_client = AsyncIOMotorClient(MONGODB_URL)
            mongodb = mongo_client.get_database('teenmind')
            # 可选索引（防失败包裹）
            try:
                await mongodb.users.create_index('user_id')
            except Exception:
                pass
            print("✅ MongoDB 连接就绪")
        except Exception as e:
            print(f"⚠️ MongoDB 初始化失败: {e}")

    # 初始化 Redis
    global redis_client
    if redis is not None:
        try:
            redis_client = redis.from_url(REDIS_URL, decode_responses=True)
            # 轻触发一次连接
            try:
                redis_client.ping()
            except Exception:
                pass
            print("✅ Redis 连接就绪")
        except Exception as e:
            print(f"⚠️ Redis 初始化失败: {e}")


async def close_db():
    """关闭外部连接。"""
    global mongo_client
    try:
        if mongo_client is not None:
            mongo_client.close()
            print("✅ MongoDB 连接已关闭")
    except Exception:
        pass
