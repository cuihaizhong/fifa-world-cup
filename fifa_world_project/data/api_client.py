"""football-data.org API 封装 (带缓存)"""
import time
import logging
from datetime import date, datetime
from functools import wraps
from typing import Optional, List, Dict, Any
import requests
from config import API_BASE_URL, API_KEY, API_CACHE_TTL

logger = logging.getLogger(__name__)

# Simple in-memory cache
_cache: Dict[str, tuple[float, Any]] = {}

def cached(ttl: int = API_CACHE_TTL):
    """Decorator: cache results for ttl seconds"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            now = time.time()
            if key in _cache:
                cached_at, value = _cache[key]
                if now - cached_at < ttl:
                    return value
            result = func(*args, **kwargs)
            _cache[key] = (now, result)
            return result
        return wrapper
    return decorator


class ApiClient:
    """Football data API client"""

    def __init__(self, api_key: str = API_KEY):
        self.api_key = api_key
        self.headers = {"X-Auth-Token": api_key} if api_key else {}
        self.available = bool(api_key)

    def _get(self, endpoint: str, params: dict = None) -> Optional[dict]:
        """Send GET request. Returns None if no API key or request fails."""
        if not self.available:
            logger.warning("API Key not configured, skipping request")
            return None
        try:
            url = f"{API_BASE_URL}/{endpoint}"
            resp = requests.get(url, headers=self.headers, params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None

    @cached(ttl=API_CACHE_TTL)
    def get_matches(self, match_date: date) -> Optional[List[dict]]:
        """Get matches for a date (World Cup competition_id=2000)"""
        data = self._get("competitions/2000/matches", {
            "dateFrom": match_date.isoformat(),
            "dateTo": match_date.isoformat(),
        })
        return data.get("matches", []) if data else None

    @cached(ttl=API_CACHE_TTL)
    def get_team_recent_matches(self, team_id: int, n: int = 10) -> Optional[List[dict]]:
        """Get team's recent finished matches"""
        data = self._get(f"teams/{team_id}/matches", {
            "limit": n,
            "status": "FINISHED",
        })
        return data.get("matches", []) if data else None

    @cached(ttl=API_CACHE_TTL)
    def get_head_to_head(self, team_id_a: int, team_id_b: int, n: int = 5) -> Optional[List[dict]]:
        """Get head-to-head history between two teams"""
        data = self._get("matches", {
            "team1": team_id_a,
            "team2": team_id_b,
            "limit": n,
            "status": "FINISHED",
        })
        return data.get("matches", []) if data else None

    @cached(ttl=86400)  # Team info cached for 1 day
    def get_team(self, team_id: int) -> Optional[dict]:
        """Get team details"""
        return self._get(f"teams/{team_id}")

    def get_match_day_summary(self, match_date: date) -> Dict:
        """Get match day summary for web display"""
        matches = self.get_matches(match_date)
        if not matches:
            return {"date": match_date.isoformat(), "matches": [], "total": 0}

        summary = []
        for m in matches:
            summary.append({
                "home_team": m["homeTeam"]["name"],
                "away_team": m["awayTeam"]["name"],
                "home_score": m["score"]["fullTime"]["home"],
                "away_score": m["score"]["fullTime"]["away"],
                "status": m["status"],
                "stage": m.get("stage", "UNKNOWN"),
                "utc_date": m["utcDate"],
            })
        return {"date": match_date.isoformat(), "matches": summary, "total": len(summary)}
