"""
音乐心理学分析模块（核心创新点⭐⭐⭐⭐⭐）
"""
import json
import numpy as np
from typing import List, Dict
from datetime import datetime
from collections import Counter
import os

class MusicPsychologyAnalyzer:
    def __init__(self):
        self.high_risk_songs = self._load_high_risk_songs()
        self.genre_emotion = {'流行':0.2,'摇滚':0.1,'电子':0.3,'古典':0.4,'民谣':-0.2,'说唱':0.0,'轻音乐':0.5,'治愈系':0.7}

    def analyze(self, user_id: str, song_ids: List[str], listening_times: List[str], song_details: List[Dict] = None) -> Dict:
        valence_analysis = self._analyze_valence(song_ids, song_details)
        time_pattern = self._analyze_time_pattern(listening_times)
        loop_detection = self._detect_single_loop(song_ids)
        high_risk_analysis = self._analyze_high_risk_songs(song_ids)
        emotion_distribution = self._analyze_emotion_distribution(song_details or [])
        music_risk_score = self._calculate_music_risk(valence_analysis, time_pattern, loop_detection, high_risk_analysis)
        recommendations = self._generate_music_therapy_recommendations(valence_analysis['overall_valence'], music_risk_score)
        return {
            'user_id': user_id,
            'valence_score': valence_analysis['overall_valence'],
            'valence_trend': valence_analysis['trend'],
            'insomnia_risk': time_pattern['late_night_ratio'] > 0.3,
            'single_loop_detected': loop_detection['detected'],
            'looped_songs': loop_detection['top_songs'],
            'high_risk_songs_count': high_risk_analysis['count'],
            'high_risk_songs': high_risk_analysis['songs'],
            'emotion_distribution': emotion_distribution,
            'music_risk_score': music_risk_score,
            'risk_level': self._get_risk_level(music_risk_score),
            'recommendations': recommendations,
            'genre_sentiment': self._get_favorite_genre_sentiment(song_details or []),
            'analysis_timestamp': datetime.now().isoformat()
        }

    def _analyze_valence(self, song_ids: List[str], song_details: List[Dict]=None) -> Dict:
        if not song_details:
            song_details = self._fetch_song_details(song_ids)
        valences = [self._calculate_song_valence(song) for song in song_details]
        overall_valence = np.mean(valences) if valences else 0.0
        if len(valences) >= 20:
            recent_valence = np.mean(valences[-10:])
            previous_valence = np.mean(valences[-20:-10])
            trend = 'improving' if recent_valence > previous_valence else 'worsening'
        else:
            trend = 'stable'
        return {'overall_valence': round(overall_valence,3),'valence_std': round(np.std(valences),3) if valences else 0,'trend': trend,'valence_history': valences}

    def _calculate_song_valence(self, song: Dict) -> float:
        valence = 0.0
        tags = song.get('tags', [])
        for tag in tags:
            if any(k in tag for k in ['悲伤','伤感','孤独']):
                valence -= 0.3
            elif any(k in tag for k in ['治愈','温暖','励志','正能量']):
                valence += 0.3
        genre = song.get('genre','')
        valence += self.genre_emotion.get(genre,0)
        if self._is_high_risk_song(song.get('name','')):
            valence -= 0.5
        return max(-1,min(1,valence))

    def _analyze_time_pattern(self, listening_times: List[str]) -> Dict:
        if not listening_times:
            return {'late_night_count':0,'late_night_ratio':0,'insomnia_detected':False,'hour_distribution':{},'peak_hours':[]}
        hour_distribution = {i:0 for i in range(24)}
        late_night_count = 0
        for t in listening_times:
            try:
                dt = datetime.fromisoformat(t)
                h = dt.hour
                hour_distribution[h]+=1
                if h>=22 or h<6:
                    late_night_count+=1
            except:
                continue
        total = len(listening_times)
        ratio = late_night_count/total if total>0 else 0
        return {'hour_distribution':hour_distribution,'late_night_count':late_night_count,'total_count':total,'late_night_ratio':round(ratio,3),'insomnia_detected':ratio>0.3,'peak_hours':self._get_peak_hours(hour_distribution)}

    def _detect_single_loop(self, song_ids: List[str]) -> Dict:
        if not song_ids:
            return {'detected':False,'top_songs':[],'max_loop_ratio':0}
        counter = Counter(song_ids)
        top = counter.most_common(5)
        total = len(song_ids)
        max_plays = top[0][1] if top else 0
        detected = max_plays > total * 0.3
        return {'detected':detected,'top_songs':[{'song_id':sid,'play_count':c,'ratio':round(c/total,3)} for sid,c in top],'max_loop_ratio':round(max_plays/total,3) if total else 0}

    def _analyze_high_risk_songs(self, song_ids: List[str]) -> Dict:
        count = 0
        songs = []
        for sid in song_ids:
            if sid in self.high_risk_songs:
                count += 1
                songs.append(self.high_risk_songs[sid])
        total = len(song_ids)
        ratio = count/total if total else 0
        return {'count':count,'total':total,'ratio':round(ratio,3),'songs':songs[:10],'high_risk_detected':ratio>0.5}

    def _analyze_emotion_distribution(self, song_details: List[Dict]) -> Dict:
        if not song_details:
            return {'happy':0,'neutral':0,'sad':0}
        counts = {'happy':0,'neutral':0,'sad':0}
        for song in song_details:
            v = self._calculate_song_valence(song)
            if v>0.3: counts['happy']+=1
            elif v<-0.3: counts['sad']+=1
            else: counts['neutral']+=1
        total = len(song_details)
        return {k: round(v/total*100,1) for k,v in counts.items()}

    def _calculate_music_risk(self, valence_analysis, time_pattern, loop_detection, high_risk_analysis) -> float:
        score = 0.0
        valence = valence_analysis['overall_valence']
        if valence < -0.5: score += 30
        elif valence < 0: score += 15
        if time_pattern['insomnia_detected']: score += 25
        if loop_detection['detected']: score += 20
        score += high_risk_analysis['ratio'] * 25
        return round(min(score,100),2)

    def _generate_music_therapy_recommendations(self, current_valence: float, risk_score: float) -> List[str]:
        if risk_score < 30:
            return ['晴天 - 周杰伦','起风了 - 买辣椒也用券','追光者 - 岑宁儿']
        elif risk_score < 70:
            return ['第1周：舒缓音乐','第2周：温暖治愈','第3周：正能量']
        else:
            return ['建议专业音乐治疗','尝试古典与自然音效','避免长时间悲伤循环']

    def _get_favorite_genre_sentiment(self, song_details: List[Dict]) -> str:
        if not song_details: return 'unknown'
        counter = Counter([s.get('genre','') for s in song_details])
        genre = counter.most_common(1)[0][0] if counter else ''
        valence = self.genre_emotion.get(genre,0)
        if valence>0.3: return 'positive'
        elif valence<-0.3: return 'negative'
        return 'neutral'

    def _get_peak_hours(self, hour_distribution: Dict[int,int]) -> List[int]:
        return [h for h,_ in sorted(hour_distribution.items(), key=lambda x:x[1], reverse=True)[:3]]

    def _get_risk_level(self, score: float) -> str:
        if score < 30: return '🟢 低风险'
        if score < 70: return '🟡 中风险'
        return '🔴 高风险'

    def _is_high_risk_song(self, name: str) -> bool:
        keywords = ['消愁','像我这样的人','无人之岛','演员','孤独','悲伤','失眠','告别','遗憾']
        return any(k in name for k in keywords)

    def _load_high_risk_songs(self) -> Dict:
        path = 'data/high_risk_songs.json'
        if os.path.exists(path):
            try:
                with open(path,'r',encoding='utf-8') as f:
                    data = json.load(f)
                    return {str(item.get('song_id', item.get('id'))): item for item in data}
            except Exception:
                pass
        return {'1': {'song_id':'1','name':'消愁','artist':'毛不易'}}

    def _fetch_song_details(self, song_ids: List[str]) -> List[Dict]:
        return [{'song_id': sid, 'name': f'Song {sid}', 'tags': [], 'genre': '流行'} for sid in song_ids]
