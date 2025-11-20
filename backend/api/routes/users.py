"""
用户管理相关 API 路由
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import hashlib
import jwt
from datetime import timedelta

router = APIRouter()

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "user"

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    monitoring_enabled: Optional[bool] = None
    monitoring_frequency: Optional[int] = None

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    role: str
    created_at: str
    monitoring_enabled: bool

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserRegister):
    try:
        password_hash = hashlib.sha256(user.password.encode()).hexdigest()
        new_user = {
            "id": generate_user_id(),
            "username": user.username,
            "email": user.email,
            "password_hash": password_hash,
            "role": user.role,
            "created_at": datetime.now().isoformat(),
            "monitoring_enabled": False,
            "monitoring_frequency": 60
        }
        return UserResponse(**new_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"注册失败: {str(e)}")

@router.post("/login")
async def login_user(credentials: UserLogin):
    try:
        password_hash = hashlib.sha256(credentials.password.encode()).hexdigest()
        token = generate_jwt_token(credentials.username)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {"username": credentials.username, "role": "user"}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"登录失败: {str(e)}")

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    try:
        user = {
            "id": user_id,
            "username": "demo_user",
            "email": "demo@example.com",
            "role": "user",
            "created_at": datetime.now().isoformat(),
            "monitoring_enabled": True
        }
        return UserResponse(**user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取用户失败: {str(e)}")

@router.put("/{user_id}")
async def update_user(user_id: str, update: UserUpdate):
    try:
        update_data = update.dict(exclude_unset=True)
        return {"message": "用户信息更新成功", "updated_fields": list(update_data.keys())}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新失败: {str(e)}")

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    try:
        return {"message": "用户删除成功", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")

@router.get("/{user_id}/dashboard")
async def get_user_dashboard(user_id: str, days: int = 30):
    try:
        dashboard_data = {
            "user_id": user_id,
            "period": f"最近{days}天",
            "emotion_trend": [
                {"date": "2025-11-01", "score": 65},
                {"date": "2025-11-05", "score": 55},
                {"date": "2025-11-10", "score": 45},
                {"date": "2025-11-15", "score": 38},
                {"date": "2025-11-19", "score": 42}
            ],
            "music_preference": {"sad": 45, "happy": 30, "neutral": 25},
            "activity_heatmap": {
                "00:00-06:00": 15,
                "06:00-12:00": 20,
                "12:00-18:00": 35,
                "18:00-24:00": 45
            },
            "risk_radar": {"emotion": 42, "music": 38, "anomaly": 35, "resonance": 40},
            "social_interaction": {"posts": 45, "comments": 120, "likes_received": 230},
            "overall_risk_score": 38,
            "risk_level": "🟡 中度风险"
        }
        return dashboard_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取仪表盘数据失败: {str(e)}")

def generate_user_id() -> str:
    import uuid
    return str(uuid.uuid4())

def generate_jwt_token(username: str) -> str:
    payload = {"username": username, "exp": datetime.utcnow() + timedelta(days=7)}
    token = jwt.encode(payload, "secret-key", algorithm="HS256")
    return token
