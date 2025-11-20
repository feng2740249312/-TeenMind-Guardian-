"""
时序异常检测模块（核心功能⭐⭐⭐⭐⭐）
"""
import numpy as np
from typing import List, Dict
from datetime import datetime, timedelta

class AnomalyDetector:
    def __init__(self):
        self.user_baselines = {}

    def detect(self, user_id: str, days: int = 30) -> Dict:
        data = self._fetch_user_data(user_id, days)
        if len(data) < 7:
            return {'user_id': user_id,'is_anomaly': False,'message': '数据不足'}
        baseline = self._build_baseline(user_id, data)
        emotion_anomaly = self._detect_emotion_change(data, baseline)
        behavior_anomaly = self._detect_behavior_change(data, baseline)
        sleep_anomaly = self._detect_sleep_pattern_change(data, baseline)
        social_anomaly = self._detect_social_withdrawal(data, baseline)
        score = self._calculate_anomaly_score(emotion_anomaly, behavior_anomaly, sleep_anomaly, social_anomaly)
        risk_factors = self._identify_risk_factors(emotion_anomaly, behavior_anomaly, sleep_anomaly, social_anomaly)
        intervention = self._generate_intervention_suggestion(score, risk_factors)
        return {
            'user_id': user_id,
            'is_anomaly': score > 60,
            'score': score,
            'risk_level': self._get_risk_level(score),
            'emotion_anomaly': emotion_anomaly,
            'behavior_anomaly': behavior_anomaly,
            'sleep_anomaly': sleep_anomaly,
            'social_anomaly': social_anomaly,
            'risk_factors': risk_factors,
            'intervention_suggestion': intervention,
            'analysis_timestamp': datetime.now().isoformat()
        }

    def _build_baseline(self, user_id: str, data: List[Dict]) -> Dict:
        subset = data[:int(len(data)*0.7)]
        emotion_scores = [d['emotion_score'] for d in subset]
        interaction_counts = [d['interaction_count'] for d in subset]
        baseline = {
            'emotion_mean': np.mean(emotion_scores),
            'emotion_std': np.std(emotion_scores) or 1,
            'interaction_mean': np.mean(interaction_counts),
            'interaction_std': np.std(interaction_counts) or 1
        }
        self.user_baselines[user_id] = baseline
        return baseline

    def _detect_emotion_change(self, data: List[Dict], baseline: Dict) -> Dict:
        recent = data[-7:]
        scores = [d['emotion_score'] for d in recent]
        z_scores = [(s - baseline['emotion_mean'])/baseline['emotion_std'] for s in scores]
        anomaly_days = sum(1 for z in z_scores if z < -2)
        is_anomaly = anomaly_days >= 3
        recent_avg = np.mean(scores)
        change_rate = (recent_avg - baseline['emotion_mean'])/baseline['emotion_mean'] if baseline['emotion_mean'] else 0
        return {'detected': is_anomaly,'z_scores': z_scores,'anomaly_days': anomaly_days,'recent_avg': recent_avg,'baseline_avg': baseline['emotion_mean'],'change_rate': round(change_rate,3)}

    def _detect_behavior_change(self, data: List[Dict], baseline: Dict) -> Dict:
        recent = data[-7:]
        posts = sum(d['post_count'] for d in recent)
        baseline_posts = 10
        post_change = (posts - baseline_posts)/baseline_posts if baseline_posts else 0
        interactions = [d['interaction_count'] for d in recent]
        interaction_avg = np.mean(interactions)
        interaction_change = (interaction_avg - baseline['interaction_mean'])/baseline['interaction_mean'] if baseline['interaction_mean'] else 0
        is_anomaly = post_change < -0.5 or interaction_change < -0.5
        return {'detected': is_anomaly,'post_change_rate': round(post_change,3),'interaction_change_rate': round(interaction_change,3),'recent_posts': posts,'baseline_posts': baseline_posts}

    def _detect_sleep_pattern_change(self, data: List[Dict], baseline: Dict) -> Dict:
        recent = data[-7:]
        late_night = sum(1 for d in recent if d['activity_hour']>=22 or d['activity_hour']<6)
        ratio = late_night/len(recent)
        return {'detected': ratio>0.5,'late_night_count': late_night,'late_night_ratio': round(ratio,3),'insomnia_risk': ratio>0.6}

    def _detect_social_withdrawal(self, data: List[Dict], baseline: Dict) -> Dict:
        recent = data[-7:]
        prev = data[-14:-7] if len(data)>=14 else data[:7]
        recent_interactions = sum(d['interaction_count'] for d in recent)
        prev_interactions = sum(d['interaction_count'] for d in prev)
        change_rate = (recent_interactions - prev_interactions)/prev_interactions if prev_interactions else 0
        return {'detected': change_rate < -0.6,'recent_interactions': recent_interactions,'previous_interactions': prev_interactions,'change_rate': round(change_rate,3)}

    def _calculate_anomaly_score(self, emotion, behavior, sleep, social) -> float:
        score = 0.0
        if emotion['detected']: score += 35 * abs(emotion['change_rate'])
        if behavior['detected']: score += 25
        if sleep['detected']: score += 20 * sleep['late_night_ratio']
        if social['detected']: score += 20 * abs(social['change_rate'])
        return round(min(score,100),2)

    def _identify_risk_factors(self, emotion, behavior, sleep, social) -> List[str]:
        factors = []
        if emotion['detected']: factors.append(f"情绪下降{abs(emotion['change_rate'])*100:.1f}%")
        if behavior['detected']: factors.append("社交活动减少")
        if sleep['detected']: factors.append("作息紊乱")
        if social['detected']: factors.append(f"互动减少{abs(social['change_rate'])*100:.1f}%")
        return factors

    def _generate_intervention_suggestion(self, score: float, factors: List[str]) -> str:
        if score < 30: return '状态正常，持续观察。'
        if score < 60: return '中度异常：建议沟通疏导，推送积极内容，鼓励规律作息。'
        return '高度异常：立即通知家长并联系专业心理咨询师。'

    def _get_risk_level(self, score: float) -> str:
        if score < 30: return '🟢 低风险'
        if score < 60: return '🟡 中风险'
        return '🔴 高风险'

    def _fetch_user_data(self, user_id: str, days: int) -> List[Dict]:
        data = []
        base_date = datetime.now() - timedelta(days=days)
        for i in range(days):
            date = base_date + timedelta(days=i)
            emotion_score = 70 - i * 1.5 + np.random.normal(0,5)
            emotion_score = max(0,min(100,emotion_score))
            data.append({'date': date.isoformat(),'emotion_score': emotion_score,'activity_hour': np.random.choice([2,14,20,22,23,1]),'post_count': max(0,int(5 - i*0.1 + np.random.normal(0,2))),'interaction_count': max(0,int(20 - i*0.3 + np.random.normal(0,5))),'music_valence': -0.3 - i*0.01 + np.random.normal(0,0.1)})
        return data
