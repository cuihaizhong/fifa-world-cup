"""百度体育球队数据爬虫 (带本地缓存)"""
import json
import os
from typing import Optional, Dict, Any

CACHE_PATH = os.path.join(os.path.dirname(__file__), "baidu_teams.json")


class BaiduTeamScraper:
    """从百度体育获取球队详情数据。

    数据来源: https://tiyu.baidu.com/al/team?id={team_id}
    缓存策略: 优先读本地 baidu_teams.json，未命中返回 None
    """

    BAIDU_TEAM_URL = "https://tiyu.baidu.com/al/team?id={team_id}"

    def __init__(self, cache_path: str = CACHE_PATH):
        self.cache_path = cache_path
        self._cache: Optional[Dict] = None

    def load_cache(self) -> Dict[str, Any]:
        """加载缓存"""
        if self._cache is not None:
            return self._cache
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r", encoding="utf-8") as f:
                self._cache = json.load(f)
        else:
            self._cache = {}
        return self._cache

    def get_team_data(self, fifa_code: str) -> Optional[Dict[str, Any]]:
        """获取某球队的百度体育数据。未收录返回 None。"""
        cache = self.load_cache()
        return cache.get(fifa_code.upper())

    def get_team_url(self, fifa_code: str) -> Optional[str]:
        """获取球队的百度体育页面 URL"""
        data = self.get_team_data(fifa_code)
        if data and data.get("team_id"):
            return self.BAIDU_TEAM_URL.format(team_id=data["team_id"])
        return None

    def has_data(self, fifa_code: str) -> bool:
        return self.get_team_data(fifa_code) is not None

    def get_all_codes(self) -> list[str]:
        """获取已收录的球队代码列表"""
        return list(self.load_cache().keys())
