"""Pydantic 数据模型（可选使用）"""
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
from datetime import datetime

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    monitoring_enabled: bool = False

class EmotionAnalysisRequest(BaseModel):
    text: str
    user_id: Optional[str] = None

class EmotionResponse(BaseModel):
    text: str
    primary_emotion: str
    confidence: float
    emotions: Dict[str, float]
    risk_score: float
    risk_level: str
    keywords: List[str]
    timestamp: datetime
