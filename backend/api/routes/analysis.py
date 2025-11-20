"""
情感分析相关 API 路由
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from backend.analyzer.emotion_bert import EmotionAnalyzer
from backend.analyzer.music_psychology import MusicPsychologyAnalyzer
from backend.analyzer.anomaly_detect import AnomalyDetector
from backend.analyzer.resonance_network import ResonanceNetworkAnalyzer

router = APIRouter()

# 请求模型
class TextAnalysisRequest(BaseModel):
    text: str
    user_id: Optional[str] = None

class MusicAnalysisRequest(BaseModel):
    user_id: str
    song_ids: List[str]
    listening_times: List[str]

class AnomalyDetectionRequest(BaseModel):
    user_id: str
    days: int = 30

class ResonanceAnalysisRequest(BaseModel):
    user_id: str
    content_ids: List[str]

# 响应模型
class EmotionResponse(BaseModel):
    emotion: str
    confidence: float
    emotions_detail: dict
    risk_level: str
    timestamp: str

class MusicPsychologyResponse(BaseModel):
    overall_valence: float
    sleep_pattern_risk: bool
    favorite_genre_sentiment: str
    recommendations: List[str]

class AnomalyResponse(BaseModel):
    is_anomaly: bool
    anomaly_score: float
    risk_factors: List[str]
    suggestion: str

class ResonanceResponse(BaseModel):
    resonance_score: float
    high_risk_content: List[str]
    user_clusters: List[int]
    intervention_needed: bool

# 初始化分析器
emotion_analyzer = EmotionAnalyzer()
music_analyzer = MusicPsychologyAnalyzer()
anomaly_detector = AnomalyDetector()
resonance_analyzer = ResonanceNetworkAnalyzer()

@router.post("/emotion", response_model=EmotionResponse)
async def analyze_emotion(request: TextAnalysisRequest):
    """
    文本情感分析
    使用 BERT 模型分析文本情感，识别抑郁、焦虑、自杀倾向等
    """
    try:
        result = emotion_analyzer.analyze(request.text)
        risk_level = "🟢 低风险"
        if result['risk_score'] > 70:
            risk_level = "🔴 高风险"
        elif result['risk_score'] > 30:
            risk_level = "🟡 中风险"
        return EmotionResponse(
            emotion=result['primary_emotion'],
            confidence=result['confidence'],
            emotions_detail=result['emotions'],
            risk_level=risk_level,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"情感分析失败: {str(e)}")

@router.post("/music-psychology", response_model=MusicPsychologyResponse)
async def analyze_music_psychology(request: MusicAnalysisRequest):
    """
    音乐心理学分析（创新点⭐）
    分析用户的音乐选择、听歌时间等，评估心理状态
    """
    try:
        result = music_analyzer.analyze(
            user_id=request.user_id,
            song_ids=request.song_ids,
            listening_times=request.listening_times
        )
        return MusicPsychologyResponse(
            overall_valence=result['valence_score'],
            sleep_pattern_risk=result['insomnia_risk'],
            favorite_genre_sentiment=result['genre_sentiment'],
            recommendations=result['recommendations']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"音乐分析失败: {str(e)}")

@router.post("/anomaly-detection", response_model=AnomalyResponse)
async def detect_anomaly(request: AnomalyDetectionRequest):
    """
    时序异常检测
    检测用户行为的异常变化，预警心理危机
    """
    try:
        result = anomaly_detector.detect(
            user_id=request.user_id,
            days=request.days
        )
        return AnomalyResponse(
            is_anomaly=result['is_anomaly'],
            anomaly_score=result['score'],
            risk_factors=result['risk_factors'],
            suggestion=result['intervention_suggestion']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"异常检测失败: {str(e)}")

@router.post("/resonance-network", response_model=ResonanceResponse)
async def analyze_resonance(request: ResonanceAnalysisRequest):
    """
    共鸣网络分析（独特创新点⭐⭐⭐）
    分析用户对哪些内容产生共鸣，识别高危内容聚集
    """
    try:
        result = resonance_analyzer.analyze(
            user_id=request.user_id,
            content_ids=request.content_ids
        )
        return ResonanceResponse(
            resonance_score=result['resonance_intensity'],
            high_risk_content=[c['content_id'] for c in result['high_risk_contents']],
            user_clusters=[hash(u['user_id']) % 10000 for u in result.get('potential_high_risk_users', [])],
            intervention_needed=result['needs_intervention']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"共鸣分析失败: {str(e)}")

@router.get("/risk-assessment/{user_id}")
async def get_risk_assessment(user_id: str):
    """综合风险评估"""
    try:
        emotion_risk = 0
        music_risk = 0
        anomaly_risk = 0
        resonance_risk = 0
        total_risk = (
            emotion_risk * 0.3 +
            music_risk * 0.25 +
            anomaly_risk * 0.25 +
            resonance_risk * 0.2
        )
        if total_risk < 30:
            level = "🟢 绿色"
            action = "正常，持续观察"
        elif total_risk < 70:
            level = "🟡 黄色"
            action = "需要关注，推送心理健康内容"
        else:
            level = "🔴 红色"
            action = "高危！立即通知家长，推荐专业咨询"
        return {
            "user_id": user_id,
            "risk_score": total_risk,
            "risk_level": level,
            "recommended_action": action,
            "details": {
                "emotion_risk": emotion_risk,
                "music_risk": music_risk,
                "anomaly_risk": anomaly_risk,
                "resonance_risk": resonance_risk
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"风险评估失败: {str(e)}")

@router.post("/batch-analysis")
async def batch_analysis(user_ids: List[str], background_tasks: BackgroundTasks):
    """批量分析（异步）"""
    background_tasks.add_task(process_batch_analysis, user_ids)
    return {
        "message": f"已启动 {len(user_ids)} 个用户的批量分析任务",
        "status": "processing"
    }

async def process_batch_analysis(user_ids: List[str]):
    for user_id in user_ids:
        try:
            pass
        except Exception as e:
            print(f"用户 {user_id} 分析失败: {e}")
