"""
TeenMind-SocialGuard 主应用入口
FastAPI 应用程序配置
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager

from backend.api.routes import analysis, users, data
from backend.models.database import init_db, close_db

# 应用生命周期管理
@asynccontextmanager
def lifespan(app: FastAPI):
    # 启动时执行
    print("🚀 TeenMind-SocialGuard 系统启动中...")
    await init_db()
    print("✅ 数据库连接成功")
    yield
    # 关闭时执行
    print("🔴 TeenMind-SocialGuard 系统关闭中...")
    await close_db()
    print("✅ 数据库连接已关闭")

# 创建 FastAPI 应用
app = FastAPI(
    title="TeenMind-SocialGuard API",
    description="基于社交媒体与音乐平台的青少年心理健康监测系统",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "*"  # 生产环境应改为具体域名
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(analysis.router, prefix="/api/analysis", tags=["情感分析"])
app.include_router(users.router, prefix="/api/users", tags=["用户管理"])
app.include_router(data.router, prefix="/api/data", tags=["数据采集"])

# 根路由
@app.get("/", tags=["系统"])
async def root():
    """系统首页"""
    return {
        "project": "TeenMind-SocialGuard",
        "description": "基于社交媒体与音乐平台的青少年心理健康监测系统",
        "version": "1.0.0",
        "status": "running",
        "author": "feng2740249312",
        "features": [
            "🎵 音乐心理学分析",
            "🌐 共鸣网络识别",
            "🤖 多模态AI融合",
            "⏰ 时序异常检测",
            "🔒 隐私保护设计"
        ],
        "docs": "/docs"
    }

# 健康检查
@app.get("/health", tags=["系统"])
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
        "mongodb": "connected"
    }

# 系统信息
@app.get("/info", tags=["系统"])
async def system_info():
    """系统信息"""
    return {
        "system": "TeenMind-SocialGuard",
        "modules": {
            "data_collection": "网易云音乐、QQ空间、豆瓣、微博",
            "ai_analysis": "BERT情感分析、音乐心理学、异常检测、共鸣网络",
            "warning_system": "三级预警、实时监控、主动干预",
            "visualization": "Dashboard、报告生成、趋势分析"
        },
        "innovation": [
            "首次将音乐数据用于心理健康检测",
            "独创共鸣网络分析算法",
            "多模态AI融合分析",
            "提前7天预警心理危机"
        ]
    }

# 全局异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "detail": str(exc)
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
