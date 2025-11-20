"""
网易云音乐数据采集器（占位实现）
说明：为保证项目可运行与导入，提供最小可用异步接口。
"""
from typing import Dict, List
from datetime import datetime

class NeteaseMusicCrawler:
    async def crawl_user_data(self, user_id: str, days: int = 30) -> Dict:
        # 占位：返回模拟数据结构
        listening_history = [
            {"song_id": "1", "song_name": "消愁", "artist": "毛不易", "play_count": 3, "timestamp": datetime.now().isoformat()}
        ]
        return {
            "user_id": user_id,
            "user_info": {"nickname": "demo", "age": 16},
            "listening_history": listening_history,
            "comments": [],
            "playlists": [],
            "resonance_data": {"resonance_intensity": 0.2},
            "crawl_time": datetime.now().isoformat(),
            "total_records": len(listening_history)
        }
