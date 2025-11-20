"""
数据采集相关 API 路由
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List

from backend.crawler.netease_music import NeteaseMusicCrawler
from backend.crawler.qzone import QZoneCrawler
from backend.crawler.douban import DoubanCrawler
from backend.crawler.weibo import WeiboCrawler

router = APIRouter()

class NeteaseCrawlRequest(BaseModel):
    user_id: str
    netease_uid: str
    days: int = 30

class QZoneCrawlRequest(BaseModel):
    user_id: str
    qq_number: str
    days: int = 30

class DoubanCrawlRequest(BaseModel):
    user_id: str
    douban_uid: str
    groups: List[str] = ["depression", "anxiety"]

class WeiboCrawlRequest(BaseModel):
    user_id: str
    weibo_uid: str
    keywords: List[str] = ["抑郁", "焦虑"]

@router.post("/netease/crawl")
async def crawl_netease_music(request: NeteaseCrawlRequest, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(crawl_netease_data, request.user_id, request.netease_uid, request.days)
        return {"message": "网易云音乐数据采集任务已启动", "user_id": request.user_id, "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动采集失败: {str(e)}")

@router.post("/qzone/crawl")
async def crawl_qzone(request: QZoneCrawlRequest, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(crawl_qzone_data, request.user_id, request.qq_number, request.days)
        return {"message": "QQ空间数据采集任务已启动", "user_id": request.user_id, "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动采集失败: {str(e)}")

@router.post("/douban/crawl")
async def crawl_douban(request: DoubanCrawlRequest, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(crawl_douban_data, request.user_id, request.douban_uid, request.groups)
        return {"message": "豆瓣数据采集任务已启动", "user_id": request.user_id, "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动采集失败: {str(e)}")

@router.post("/weibo/crawl")
async def crawl_weibo(request: WeiboCrawlRequest, background_tasks: BackgroundTasks):
    try:
        background_tasks.add_task(crawl_weibo_data, request.user_id, request.weibo_uid, request.keywords)
        return {"message": "微博数据采集任务已启动", "user_id": request.user_id, "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动采集失败: {str(e)}")

@router.get("/status/{user_id}")
async def get_crawl_status(user_id: str):
    try:
        status = {
            "user_id": user_id,
            "netease": {"status": "completed", "records": 1234, "last_update": "2025-11-19 14:30:00"},
            "qzone": {"status": "processing", "records": 567, "last_update": "2025-11-19 14:45:00"},
            "douban": {"status": "idle", "records": 0, "last_update": None},
            "weibo": {"status": "idle", "records": 0, "last_update": None}
        }
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取状态失败: {str(e)}")

async def crawl_netease_data(user_id: str, netease_uid: str, days: int):
    try:
        crawler = NeteaseMusicCrawler()
        data = await crawler.crawl_user_data(netease_uid, days)
        print(f"✅ 用户 {user_id} 网易云数据采集完成: {len(data.get('listening_history', []))} 条记录")
    except Exception as e:
        print(f"❌ 用户 {user_id} 网易云数据采集失败: {e}")

async def crawl_qzone_data(user_id: str, qq_number: str, days: int):
    try:
        crawler = QZoneCrawler()
        data = await crawler.crawl_qzone_data(qq_number, days)
        print(f"✅ 用户 {user_id} QQ空间数据采集完成: {len(data.get('posts', []))} 条记录")
    except Exception as e:
        print(f"❌ 用户 {user_id} QQ空间数据采集失败: {e}")

async def crawl_douban_data(user_id: str, douban_uid: str, groups: List[str]):
    try:
        crawler = DoubanCrawler()
        data = await crawler.crawl_douban_data(douban_uid, groups)
        print(f"✅ 用户 {user_id} 豆瓣数据采集完成: {len(data.get('group_topics', []))} 条记录")
    except Exception as e:
        print(f"❌ 用户 {user_id} 豆瓣数据采集失败: {e}")

async def crawl_weibo_data(user_id: str, weibo_uid: str, keywords: List[str]):
    try:
        crawler = WeiboCrawler()
        data = await crawler.crawl_weibo_data(weibo_uid, keywords)
        print(f"✅ 用户 {user_id} 微博数据采集完成: {len(data.get('posts', []))} 条记录")
    except Exception as e:
        print(f"❌ 用户 {user_id} 微博数据采集失败: {e}")
