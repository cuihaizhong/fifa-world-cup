"""数据模型定义"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class MatchStage(Enum):
    GROUP = "小组赛"
    R32 = "1/16决赛"
    R16 = "1/8决赛"
    QF = "1/4决赛"
    SF = "半决赛"
    THIRD = "三四名决赛"
    FINAL = "决赛"


@dataclass
class Team:
    id: int
    name: str
    name_cn: str
    fifa_code: str            # 三字母代码, 如 "ARG", "FRA", "BRA"
    group: str                # "A" ~ "L"
    elo_rating: float         # 当前 Elo 评分
    fifa_rank: int            # FIFA 世界排名


@dataclass
class Match:
    id: int
    home_team: Team
    away_team: Team
    date: datetime
    stage: MatchStage
    venue: str                # 球场/城市
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    prediction: Optional['Prediction'] = None


@dataclass
class Prediction:
    home_win_pct: float       # 主队胜率 (%)
    draw_pct: float           # 平局率 (%)
    away_win_pct: float       # 客队胜率 (%)
    expected_home_goals: float
    expected_away_goals: float
    elo_diff: float           # 双方 Elo 分差 (主-客)
    confidence: str           # "高" / "中" / "低"
