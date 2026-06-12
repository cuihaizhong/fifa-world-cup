# 2026 世界杯比赛胜率预测 — 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个基于 Elo + 泊松分布的 2026 世界杯比赛胜率预测 Web 应用。

**Architecture:** 三层架构 — data/ (数据层：模型 + API 封装 + SQLite 存储 + 种子数据)、engine/ (预测引擎：Elo + 泊松模拟 + 调整因子 + 编排器)、web/ (Streamlit 界面：赛程预测 + 球队分析 + 淘汰赛模拟)。

**Tech Stack:** Python 3.11+, Streamlit, pandas, numpy, scipy, plotly, SQLite, pydantic

---

## 文件结构总览

```
fifa_world_project/
├── config.py                       # Task 1: 全局配置
├── requirements.txt                # Task 1: 依赖
├── run.sh                          # Task 15: 启动脚本
├── README.md                       # Task 15: 说明文档
├── data/
│   ├── __init__.py                 # Task 1: 空文件
│   ├── models.py                   # Task 2: Team, Match, Prediction 数据类
│   ├── store.py                    # Task 3: SQLite 存储层
│   ├── seed_data.py                # Task 4: 48队 + 104场赛程种子数据
│   └── api_client.py               # Task 5: football-data.org API 封装
├── engine/
│   ├── __init__.py                 # Task 1: 空文件
│   ├── elo.py                      # Task 6: Elo 评分系统
│   ├── poisson.py                  # Task 7: 泊松蒙特卡洛模拟
│   ├── adjustments.py              # Task 8: 预测调整因子
│   └── predictor.py                # Task 9: 预测编排器
├── web/
│   ├── __init__.py                 # Task 1: 空文件
│   ├── theme.py                    # Task 10: 深色主题 CSS 注入
│   ├── components.py               # Task 10: UI 复用组件
│   ├── app.py                      # Task 11: Streamlit 主入口
│   └── pages/
│       ├── 01_赛程预测.py           # Task 12: 赛程与预测页面
│       ├── 02_球队分析.py           # Task 13: 球队分析页面
│       └── 03_淘汰赛模拟.py         # Task 14: 淘汰赛模拟页面
└── tests/
    ├── __init__.py                 # Task 1: 空文件
    ├── test_models.py              # Task 2: 模型测试
    ├── test_store.py               # Task 3: 存储测试
    ├── test_elo.py                 # Task 6: Elo 测试
    ├── test_poisson.py             # Task 7: 泊松测试
    ├── test_adjustments.py         # Task 8: 调整因子测试
    └── test_predictor.py           # Task 9: 编排器测试
```

---

### Task 1: 项目骨架搭建

**Files:**
- Create: `requirements.txt`, `config.py`, `data/__init__.py`, `engine/__init__.py`, `web/__init__.py`, `tests/__init__.py`, `run.sh`

- [ ] **Step 1: 创建 requirements.txt**

```txt
streamlit>=1.28
pandas>=2.0
numpy>=1.24
scipy>=1.10
requests>=2.31
plotly>=5.15
pydantic>=2.0
```

- [ ] **Step 2: 创建 config.py**

```python
"""全局配置"""

# === 预测引擎参数 ===
ELO_INIT_TOP = 2100.0          # FIFA 排名第1的初始 Elo 分
ELO_RANK_STEP = 8.0            # 每降1名扣分
ELO_K_GROUP = 30               # 小组赛 K 值
ELO_K_KNOCKOUT = 60            # 淘汰赛 K 值
ELO_HOME_ADVANTAGE = 100.0     # 主场优势 (Elo 加分)

# === 泊松模拟参数 ===
BASE_LAMBDA = 1.5              # 国际比赛平均进球
LAMBDA_PER_100_ELO = 0.15      # 每 100 Elo 优势的进球加成
HOME_LAMBDA_BONUS = 0.2        # 主场进球加成
LAMBDA_MIN = 0.3               # λ 下限
LAMBDA_MAX = 4.0               # λ 上限
MONTE_CARLO_N = 10000          # 模拟次数

# === 调整因子权重 ===
ADJ_RECENT_FORM_WEIGHT = 0.05  # 近期状态 ±5%
ADJ_H2H_WEIGHT = 0.03          # 交锋记录 ±3%
ADJ_REST_WEIGHT = 0.02         # 休息天数惩罚

# === API 配置 ===
API_BASE_URL = "https://api.football-data.org/v4"
API_KEY = ""  # 填入你的 API Key
API_CACHE_TTL = 300            # 缓存 5 分钟

# === 数据库 ===
DB_PATH = "data/fifa_world.db"

# === UI 主题 ===
THEME = {
    "primary": "#0C4AD1",
    "bg_dark": "#0A0E1A",
    "card_bg": "#131832",
    "text_primary": "#FFFFFF",
    "text_secondary": "#8892B0",
    "win": "#10B981",
    "draw": "#F59E0B",
    "lose": "#EF4444",
    "border": "#1E2340",
}
```

- [ ] **Step 3: 创建各模块 __init__.py**

```bash
mkdir -p data engine web pages tests
touch data/__init__.py
touch engine/__init__.py
touch web/__init__.py
touch tests/__init__.py
```

- [ ] **Step 4: 创建 run.sh 启动脚本**

```bash
#!/bin/bash
# 2026 世界杯预测 — 启动脚本

echo "🏆 启动 2026 世界杯预测系统..."

# 安装依赖
pip install -r requirements.txt -q

# 初始化数据 (首次运行会自动创建数据库和种子数据)
python -c "
from data.store import Store
from data.seed_data import seed_all
store = Store()
if store.is_empty():
    print('📦 首次运行，初始化种子数据...')
    seed_all(store)
    print('✅ 初始化完成')
else:
    print('✅ 数据已存在，跳过初始化')
store.close()
"

# 启动 Streamlit
streamlit run web/app.py --server.port 8501
```

```bash
chmod +x run.sh
```

- [ ] **Step 5: 安装依赖并验证**

```bash
pip install -r requirements.txt
```

- [ ] **Step 6: Commit**

```bash
git add requirements.txt config.py data/__init__.py engine/__init__.py web/__init__.py tests/__init__.py run.sh
git commit -m "feat: project skeleton with config and dependencies"
```

---

### Task 2: 数据模型定义

**Files:**
- Create: `data/models.py`, `tests/test_models.py`

- [ ] **Step 1: 编写模型测试**

```python
"""data/models.py 的单元测试"""
import pytest
from datetime import datetime
from data.models import Team, Match, MatchStage, Prediction


class TestTeam:
    def test_team_creation(self):
        team = Team(
            id=1, name="Argentina", name_cn="阿根廷",
            fifa_code="ARG", group="J", elo_rating=2100.0, fifa_rank=1
        )
        assert team.name == "Argentina"
        assert team.name_cn == "阿根廷"
        assert team.fifa_code == "ARG"
        assert team.group == "J"
        assert team.elo_rating == 2100.0
        assert team.fifa_rank == 1

    def test_team_default_values(self):
        team = Team(id=1, name="Test", name_cn="测试",
                    fifa_code="TST", group="A", elo_rating=1500.0, fifa_rank=50)
        assert isinstance(team.elo_rating, float)


class TestMatch:
    def test_match_creation_no_result(self):
        home = Team(id=1, name="Brazil", name_cn="巴西",
                    fifa_code="BRA", group="C", elo_rating=2080.0, fifa_rank=3)
        away = Team(id=2, name="Morocco", name_cn="摩洛哥",
                    fifa_code="MAR", group="C", elo_rating=1850.0, fifa_rank=22)
        match = Match(
            id=1, home_team=home, away_team=away,
            date=datetime(2026, 6, 13, 21, 0),
            stage=MatchStage.GROUP, venue="New York/New Jersey"
        )
        assert match.home_score is None
        assert match.away_score is None
        assert match.prediction is None
        assert match.stage == MatchStage.GROUP

    def test_match_with_result(self):
        home = Team(id=1, name="Brazil", name_cn="巴西",
                    fifa_code="BRA", group="C", elo_rating=2080.0, fifa_rank=3)
        away = Team(id=2, name="Morocco", name_cn="摩洛哥",
                    fifa_code="MAR", group="C", elo_rating=1850.0, fifa_rank=22)
        match = Match(
            id=1, home_team=home, away_team=away,
            date=datetime(2026, 6, 13), stage=MatchStage.GROUP,
            venue="NY", home_score=3, away_score=1
        )
        assert match.home_score == 3
        assert match.away_score == 1


class TestPrediction:
    def test_prediction_creation(self):
        pred = Prediction(
            home_win_pct=55.2, draw_pct=24.1, away_win_pct=20.7,
            expected_home_goals=2.1, expected_away_goals=1.3,
            elo_diff=120.0, confidence="中"
        )
        assert pred.home_win_pct == 55.2
        assert pred.confidence == "中"
        assert abs(pred.home_win_pct + pred.draw_pct + pred.away_win_pct - 100.0) < 1.0


class TestMatchStage:
    def test_stage_values(self):
        assert MatchStage.GROUP.value == "小组赛"
        assert MatchStage.R32.value == "1/16决赛"
        assert MatchStage.R16.value == "1/8决赛"
        assert MatchStage.QF.value == "1/4决赛"
        assert MatchStage.SF.value == "半决赛"
        assert MatchStage.THIRD.value == "三四名决赛"
        assert MatchStage.FINAL.value == "决赛"
```

- [ ] **Step 2: 运行测试确认失败**

```bash
python -m pytest tests/test_models.py -v
```

- [ ] **Step 3: 实现 data/models.py**

```python
"""数据模型定义"""
from dataclasses import dataclass, field
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
```

- [ ] **Step 4: 运行测试验证**

```bash
python -m pytest tests/test_models.py -v
```
Expected: All PASS

- [ ] **Step 5: Commit**

```bash
git add data/models.py tests/test_models.py
git commit -m "feat: add data models — Team, Match, Prediction, MatchStage"
```

---

### Task 3: SQLite 存储层

**Files:**
- Create: `data/store.py`, `tests/test_store.py`

- [ ] **Step 1: 编写存储层测试**

```python
"""data/store.py 的单元测试"""
import pytest
import os
from datetime import datetime
from data.store import Store
from data.models import Team, Match, MatchStage, Prediction


@pytest.fixture
def store():
    """使用内存数据库进行测试"""
    s = Store(":memory:")
    s.init_db()
    yield s
    s.close()


@pytest.fixture
def sample_team():
    return Team(
        id=1, name="Brazil", name_cn="巴西",
        fifa_code="BRA", group="C", elo_rating=2080.0, fifa_rank=3
    )


@pytest.fixture
def sample_teams():
    return [
        Team(id=1, name="Brazil", name_cn="巴西",
             fifa_code="BRA", group="C", elo_rating=2080.0, fifa_rank=3),
        Team(id=2, name="Argentina", name_cn="阿根廷",
             fifa_code="ARG", group="J", elo_rating=2100.0, fifa_rank=1),
    ]


class TestStoreTeams:
    def test_upsert_and_get_team(self, store, sample_team):
        store.upsert_team(sample_team)
        result = store.get_team(1)
        assert result is not None
        assert result.name == "Brazil"
        assert result.elo_rating == 2080.0

    def test_update_team_elo(self, store, sample_team):
        store.upsert_team(sample_team)
        sample_team.elo_rating = 2100.0
        store.upsert_team(sample_team)
        result = store.get_team(1)
        assert result.elo_rating == 2100.0

    def test_get_all_teams(self, store, sample_teams):
        for t in sample_teams:
            store.upsert_team(t)
        teams = store.get_all_teams()
        assert len(teams) == 2

    def test_get_teams_by_group(self, store, sample_teams):
        for t in sample_teams:
            store.upsert_team(t)
        group_c = store.get_teams_by_group("C")
        assert len(group_c) == 1
        assert group_c[0].name == "Brazil"

    def test_get_nonexistent_team(self, store):
        result = store.get_team(999)
        assert result is None


class TestStoreMatches:
    def test_upsert_and_get_match(self, store, sample_teams):
        store.upsert_team(sample_teams[0])
        store.upsert_team(sample_teams[1])
        match = Match(
            id=1, home_team=sample_teams[0], away_team=sample_teams[1],
            date=datetime(2026, 6, 13), stage=MatchStage.GROUP, venue="NY"
        )
        store.upsert_match(match)
        result = store.get_match(1)
        assert result.stage == MatchStage.GROUP
        assert result.home_team.id == 1

    def test_get_matches_by_date(self, store, sample_teams):
        store.upsert_team(sample_teams[0])
        store.upsert_team(sample_teams[1])
        m1 = Match(id=1, home_team=sample_teams[0], away_team=sample_teams[1],
                   date=datetime(2026, 6, 13), stage=MatchStage.GROUP, venue="NY")
        m2 = Match(id=2, home_team=sample_teams[1], away_team=sample_teams[0],
                   date=datetime(2026, 6, 14), stage=MatchStage.GROUP, venue="LA")
        store.upsert_match(m1)
        store.upsert_match(m2)
        day_matches = store.get_matches_by_date(datetime(2026, 6, 13).date())
        assert len(day_matches) == 1
        assert day_matches[0].id == 1

    def test_update_match_result(self, store, sample_teams):
        store.upsert_team(sample_teams[0])
        store.upsert_team(sample_teams[1])
        match = Match(id=1, home_team=sample_teams[0], away_team=sample_teams[1],
                      date=datetime(2026, 6, 13), stage=MatchStage.GROUP, venue="NY")
        store.upsert_match(match)
        store.update_match_result(1, home_score=2, away_score=0)
        result = store.get_match(1)
        assert result.home_score == 2
        assert result.away_score == 0

    def test_save_prediction(self, store, sample_teams):
        store.upsert_team(sample_teams[0])
        store.upsert_team(sample_teams[1])
        match = Match(id=1, home_team=sample_teams[0], away_team=sample_teams[1],
                      date=datetime(2026, 6, 13), stage=MatchStage.GROUP, venue="NY")
        store.upsert_match(match)
        pred = Prediction(
            home_win_pct=55.0, draw_pct=25.0, away_win_pct=20.0,
            expected_home_goals=1.8, expected_away_goals=1.2,
            elo_diff=100.0, confidence="中"
        )
        store.save_prediction(1, pred)
        result = store.get_match(1)
        assert result.prediction is not None
        assert result.prediction.home_win_pct == 55.0


class TestStoreEloHistory:
    def test_save_and_get_elo_history(self, store, sample_team):
        store.upsert_team(sample_team)
        store.save_elo_history(match_id=1, team_id=1,
                               old_elo=2080.0, new_elo=2095.0)
        history = store.get_elo_history(team_id=1)
        assert len(history) == 1
        assert history[0]["new_elo"] == 2095.0

    def test_elo_history_ordered_by_time(self, store, sample_team):
        store.upsert_team(sample_team)
        store.save_elo_history(match_id=1, team_id=1,
                               old_elo=2080.0, new_elo=2095.0)
        store.save_elo_history(match_id=2, team_id=1,
                               old_elo=2095.0, new_elo=2110.0)
        history = store.get_elo_history(team_id=1)
        assert len(history) == 2
        # 按时间升序
        assert history[0]["new_elo"] == 2095.0
        assert history[1]["new_elo"] == 2110.0


class TestStoreInit:
    def test_is_empty_returns_true(self, store):
        assert store.is_empty() is True

    def test_is_empty_returns_false_after_insert(self, store, sample_team):
        store.upsert_team(sample_team)
        assert store.is_empty() is False
```

- [ ] **Step 2: 实现 data/store.py**

```python
"""SQLite 本地存储"""
import sqlite3
import json
from datetime import date, datetime
from typing import Optional, List, Dict
from data.models import Team, Match, MatchStage, Prediction


class Store:
    def __init__(self, db_path: str = "data/fifa_world.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def init_db(self):
        """创建数据库表"""
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                name_cn TEXT NOT NULL,
                fifa_code TEXT NOT NULL UNIQUE,
                group_name TEXT NOT NULL,
                elo_rating REAL NOT NULL,
                fifa_rank INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY,
                home_team_id INTEGER NOT NULL,
                away_team_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                stage TEXT NOT NULL,
                venue TEXT NOT NULL,
                home_score INTEGER,
                away_score INTEGER,
                prediction_json TEXT,
                FOREIGN KEY (home_team_id) REFERENCES teams(id),
                FOREIGN KEY (away_team_id) REFERENCES teams(id)
            );

            CREATE TABLE IF NOT EXISTS elo_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER NOT NULL,
                team_id INTEGER NOT NULL,
                old_elo REAL NOT NULL,
                new_elo REAL NOT NULL,
                updated_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (team_id) REFERENCES teams(id)
            );
        """)
        self.conn.commit()

    def is_empty(self) -> bool:
        """检查数据库是否为空（无球队数据）"""
        cursor = self.conn.execute("SELECT COUNT(*) FROM teams")
        return cursor.fetchone()[0] == 0

    # === Team CRUD ===

    def upsert_team(self, team: Team):
        self.conn.execute("""
            INSERT OR REPLACE INTO teams (id, name, name_cn, fifa_code, group_name, elo_rating, fifa_rank)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (team.id, team.name, team.name_cn, team.fifa_code, team.group,
              team.elo_rating, team.fifa_rank))
        self.conn.commit()

    def get_team(self, team_id: int) -> Optional[Team]:
        row = self.conn.execute(
            "SELECT * FROM teams WHERE id = ?", (team_id,)
        ).fetchone()
        return self._row_to_team(row) if row else None

    def get_team_by_code(self, fifa_code: str) -> Optional[Team]:
        row = self.conn.execute(
            "SELECT * FROM teams WHERE fifa_code = ?", (fifa_code,)
        ).fetchone()
        return self._row_to_team(row) if row else None

    def get_all_teams(self) -> List[Team]:
        rows = self.conn.execute(
            "SELECT * FROM teams ORDER BY elo_rating DESC"
        ).fetchall()
        return [self._row_to_team(r) for r in rows]

    def get_teams_by_group(self, group_name: str) -> List[Team]:
        rows = self.conn.execute(
            "SELECT * FROM teams WHERE group_name = ? ORDER BY elo_rating DESC",
            (group_name,)
        ).fetchall()
        return [self._row_to_team(r) for r in rows]

    # === Match CRUD ===

    def upsert_match(self, match: Match):
        pred_json = None
        if match.prediction:
            pred_json = json.dumps({
                "home_win_pct": match.prediction.home_win_pct,
                "draw_pct": match.prediction.draw_pct,
                "away_win_pct": match.prediction.away_win_pct,
                "expected_home_goals": match.prediction.expected_home_goals,
                "expected_away_goals": match.prediction.expected_away_goals,
                "elo_diff": match.prediction.elo_diff,
                "confidence": match.prediction.confidence,
            })
        self.conn.execute("""
            INSERT OR REPLACE INTO matches
            (id, home_team_id, away_team_id, date, stage, venue, home_score, away_score, prediction_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (match.id, match.home_team.id, match.away_team.id,
              match.date.isoformat(), match.stage.value, match.venue,
              match.home_score, match.away_score, pred_json))
        self.conn.commit()

    def get_match(self, match_id: int) -> Optional[Match]:
        row = self.conn.execute("""
            SELECT m.*, t1.name as ht_name, t1.name_cn as ht_name_cn,
                   t1.fifa_code as ht_code, t1.group_name as ht_group,
                   t1.elo_rating as ht_elo, t1.fifa_rank as ht_rank,
                   t2.name as at_name, t2.name_cn as at_name_cn,
                   t2.fifa_code as at_code, t2.group_name as at_group,
                   t2.elo_rating as at_elo, t2.fifa_rank as at_rank
            FROM matches m
            JOIN teams t1 ON m.home_team_id = t1.id
            JOIN teams t2 ON m.away_team_id = t2.id
            WHERE m.id = ?
        """, (match_id,)).fetchone()
        return self._row_to_match(row) if row else None

    def get_matches_by_date(self, target_date: date) -> List[Match]:
        date_str = target_date.isoformat()
        rows = self.conn.execute("""
            SELECT m.*, t1.name as ht_name, t1.name_cn as ht_name_cn,
                   t1.fifa_code as ht_code, t1.group_name as ht_group,
                   t1.elo_rating as ht_elo, t1.fifa_rank as ht_rank,
                   t2.name as at_name, t2.name_cn as at_name_cn,
                   t2.fifa_code as at_code, t2.group_name as at_group,
                   t2.elo_rating as at_elo, t2.fifa_rank as at_rank
            FROM matches m
            JOIN teams t1 ON m.home_team_id = t1.id
            JOIN teams t2 ON m.away_team_id = t2.id
            WHERE date(m.date) = date(?)
            ORDER BY m.date
        """, (date_str,)).fetchall()
        return [self._row_to_match(r) for r in rows]

    def get_all_matches(self) -> List[Match]:
        rows = self.conn.execute("""
            SELECT m.*, t1.name as ht_name, t1.name_cn as ht_name_cn,
                   t1.fifa_code as ht_code, t1.group_name as ht_group,
                   t1.elo_rating as ht_elo, t1.fifa_rank as ht_rank,
                   t2.name as at_name, t2.name_cn as at_name_cn,
                   t2.fifa_code as at_code, t2.group_name as at_group,
                   t2.elo_rating as at_elo, t2.fifa_rank as at_rank
            FROM matches m
            JOIN teams t1 ON m.home_team_id = t1.id
            JOIN teams t2 ON m.away_team_id = t2.id
            ORDER BY m.date
        """).fetchall()
        return [self._row_to_match(r) for r in rows]

    def update_match_result(self, match_id: int, home_score: int, away_score: int):
        self.conn.execute("""
            UPDATE matches SET home_score = ?, away_score = ?
            WHERE id = ?
        """, (home_score, away_score, match_id))
        self.conn.commit()

    def save_prediction(self, match_id: int, pred: Prediction):
        pred_json = json.dumps({
            "home_win_pct": pred.home_win_pct,
            "draw_pct": pred.draw_pct,
            "away_win_pct": pred.away_win_pct,
            "expected_home_goals": pred.expected_home_goals,
            "expected_away_goals": pred.expected_away_goals,
            "elo_diff": pred.elo_diff,
            "confidence": pred.confidence,
        })
        self.conn.execute(
            "UPDATE matches SET prediction_json = ? WHERE id = ?",
            (pred_json, match_id)
        )
        self.conn.commit()

    def get_upcoming_matches(self) -> List[Match]:
        rows = self.conn.execute("""
            SELECT m.*, t1.name as ht_name, t1.name_cn as ht_name_cn,
                   t1.fifa_code as ht_code, t1.group_name as ht_group,
                   t1.elo_rating as ht_elo, t1.fifa_rank as ht_rank,
                   t2.name as at_name, t2.name_cn as at_name_cn,
                   t2.fifa_code as at_code, t2.group_name as at_group,
                   t2.elo_rating as at_elo, t2.fifa_rank as at_rank
            FROM matches m
            JOIN teams t1 ON m.home_team_id = t1.id
            JOIN teams t2 ON m.away_team_id = t2.id
            WHERE m.home_score IS NULL
            ORDER BY m.date
        """).fetchall()
        return [self._row_to_match(r) for r in rows]

    # === Elo History ===

    def save_elo_history(self, match_id: int, team_id: int,
                         old_elo: float, new_elo: float):
        self.conn.execute("""
            INSERT INTO elo_history (match_id, team_id, old_elo, new_elo)
            VALUES (?, ?, ?, ?)
        """, (match_id, team_id, old_elo, new_elo))
        self.conn.commit()

    def get_elo_history(self, team_id: int) -> List[Dict]:
        rows = self.conn.execute("""
            SELECT * FROM elo_history
            WHERE team_id = ?
            ORDER BY updated_at ASC
        """, (team_id,)).fetchall()
        return [dict(r) for r in rows]

    # === Helpers ===

    def _row_to_team(self, row) -> Team:
        return Team(
            id=row["id"],
            name=row["name"],
            name_cn=row["name_cn"],
            fifa_code=row["fifa_code"],
            group=row["group_name"],
            elo_rating=row["elo_rating"],
            fifa_rank=row["fifa_rank"],
        )

    def _row_to_match(self, row) -> Optional[Match]:
        if row is None:
            return None
        home = Team(
            id=row["home_team_id"],
            name=row["ht_name"],
            name_cn=row["ht_name_cn"],
            fifa_code=row["ht_code"],
            group=row["ht_group"],
            elo_rating=row["ht_elo"],
            fifa_rank=row["ht_rank"],
        )
        away = Team(
            id=row["away_team_id"],
            name=row["at_name"],
            name_cn=row["at_name_cn"],
            fifa_code=row["at_code"],
            group=row["at_group"],
            elo_rating=row["at_elo"],
            fifa_rank=row["at_rank"],
        )
        pred = None
        if row["prediction_json"]:
            p = json.loads(row["prediction_json"])
            pred = Prediction(
                home_win_pct=p["home_win_pct"],
                draw_pct=p["draw_pct"],
                away_win_pct=p["away_win_pct"],
                expected_home_goals=p["expected_home_goals"],
                expected_away_goals=p["expected_away_goals"],
                elo_diff=p["elo_diff"],
                confidence=p["confidence"],
            )
        return Match(
            id=row["id"],
            home_team=home,
            away_team=away,
            date=datetime.fromisoformat(row["date"]),
            stage=MatchStage(row["stage"]),
            venue=row["venue"],
            home_score=row["home_score"],
            away_score=row["away_score"],
            prediction=pred,
        )

    def close(self):
        self.conn.close()
```

- [ ] **Step 3: 运行测试验证**

```bash
python -m pytest tests/test_store.py -v
```
Expected: All PASS

- [ ] **Step 4: Commit**

```bash
git add data/store.py tests/test_store.py
git commit -m "feat: add SQLite store layer — teams, matches, elo_history"
```

---

### Task 4: 种子数据 — 48 队 + 104 场赛程

**Files:**
- Create: `data/seed_data.py`

- [ ] **Step 1: 实现 data/seed_data.py**

```python
"""种子数据：48 支球队 + 104 场比赛赛程"""
from datetime import datetime
from data.models import Team, Match, MatchStage
from data.store import Store
from config import ELO_INIT_TOP, ELO_RANK_STEP

# === 48 支球队 (FIFA 排名近似值, 2026年6月) ===
TEAMS_DATA = [
    # 组A
    (1, "Mexico", "墨西哥", "MEX", "A", 15),
    (2, "South Africa", "南非", "RSA", "A", 48),
    (3, "South Korea", "韩国", "KOR", "A", 24),
    (4, "Czechia", "捷克", "CZE", "A", 36),
    # 组B
    (5, "Canada", "加拿大", "CAN", "B", 33),
    (6, "Bosnia & Herzegovina", "波黑", "BIH", "B", 56),
    (7, "Qatar", "卡塔尔", "QAT", "B", 60),
    (8, "Switzerland", "瑞士", "SUI", "B", 19),
    # 组C
    (9, "Brazil", "巴西", "BRA", "C", 5),
    (10, "Morocco", "摩洛哥", "MAR", "C", 13),
    (11, "Haiti", "海地", "HAI", "C", 87),
    (12, "Scotland", "苏格兰", "SCO", "C", 42),
    # 组D
    (13, "United States", "美国", "USA", "D", 11),
    (14, "Paraguay", "巴拉圭", "PAR", "D", 52),
    (15, "Australia", "澳大利亚", "AUS", "D", 27),
    (16, "Türkiye", "土耳其", "TUR", "D", 35),
    # 组E
    (17, "Germany", "德国", "GER", "E", 10),
    (18, "Curaçao", "库拉索", "CUW", "E", 82),
    (19, "Ivory Coast", "科特迪瓦", "CIV", "E", 38),
    (20, "Ecuador", "厄瓜多尔", "ECU", "E", 30),
    # 组F
    (21, "Netherlands", "荷兰", "NED", "F", 6),
    (22, "Japan", "日本", "JPN", "F", 17),
    (23, "Sweden", "瑞典", "SWE", "F", 26),
    (24, "Tunisia", "突尼斯", "TUN", "F", 47),
    # 组G
    (25, "Belgium", "比利时", "BEL", "G", 8),
    (26, "Egypt", "埃及", "EGY", "G", 40),
    (27, "Iran", "伊朗", "IRN", "G", 21),
    (28, "New Zealand", "新西兰", "NZL", "G", 95),
    # 组H
    (29, "Spain", "西班牙", "ESP", "H", 2),
    (30, "Cape Verde", "佛得角", "CPV", "H", 65),
    (31, "Saudi Arabia", "沙特", "KSA", "H", 55),
    (32, "Uruguay", "乌拉圭", "URU", "H", 14),
    # 组I
    (33, "France", "法国", "FRA", "I", 1),
    (34, "Senegal", "塞内加尔", "SEN", "I", 18),
    (35, "Iraq", "伊拉克", "IRQ", "I", 70),
    (36, "Norway", "挪威", "NOR", "I", 43),
    # 组J
    (37, "Argentina", "阿根廷", "ARG", "J", 4),
    (38, "Algeria", "阿尔及利亚", "ALG", "J", 31),
    (39, "Austria", "奥地利", "AUT", "J", 25),
    (40, "Jordan", "约旦", "JOR", "J", 71),
    # 组K
    (41, "Portugal", "葡萄牙", "POR", "K", 7),
    (42, "DR Congo", "刚果(金)", "COD", "K", 63),
    (43, "Uzbekistan", "乌兹别克斯坦", "UZB", "K", 58),
    (44, "Colombia", "哥伦比亚", "COL", "K", 9),
    # 组L
    (45, "England", "英格兰", "ENG", "L", 3),
    (46, "Croatia", "克罗地亚", "CRO", "L", 12),
    (47, "Ghana", "加纳", "GHA", "L", 68),
    (48, "Panama", "巴拿马", "PAN", "L", 44),
]

# === 国旗 Emoji 映射 ===
FLAG_MAP = {
    "MEX": "🇲🇽", "RSA": "🇿🇦", "KOR": "🇰🇷", "CZE": "🇨🇿",
    "CAN": "🇨🇦", "BIH": "🇧🇦", "QAT": "🇶🇦", "SUI": "🇨🇭",
    "BRA": "🇧🇷", "MAR": "🇲🇦", "HAI": "🇭🇹", "SCO": "🏴󠁧󠁢󠁳󠁣󠁴󠁿",
    "USA": "🇺🇸", "PAR": "🇵🇾", "AUS": "🇦🇺", "TUR": "🇹🇷",
    "GER": "🇩🇪", "CUW": "🇨🇼", "CIV": "🇨🇮", "ECU": "🇪🇨",
    "NED": "🇳🇱", "JPN": "🇯🇵", "SWE": "🇸🇪", "TUN": "🇹🇳",
    "BEL": "🇧🇪", "EGY": "🇪🇬", "IRN": "🇮🇷", "NZL": "🇳🇿",
    "ESP": "🇪🇸", "CPV": "🇨🇻", "KSA": "🇸🇦", "URU": "🇺🇾",
    "FRA": "🇫🇷", "SEN": "🇸🇳", "IRQ": "🇮🇶", "NOR": "🇳🇴",
    "ARG": "🇦🇷", "ALG": "🇩🇿", "AUT": "🇦🇹", "JOR": "🇯🇴",
    "POR": "🇵🇹", "COD": "🇨🇩", "UZB": "🇺🇿", "COL": "🇨🇴",
    "ENG": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "CRO": "🇭🇷", "GHA": "🇬🇭", "PAN": "🇵🇦",
}


def _elo_from_rank(rank: int) -> float:
    """FIFA 排名 → Elo 初始分"""
    return ELO_INIT_TOP - (rank - 1) * ELO_RANK_STEP


def create_teams() -> list[Team]:
    """创建 48 支球队"""
    teams = []
    for tid, name, name_cn, code, group, rank in TEAMS_DATA:
        teams.append(Team(
            id=tid, name=name, name_cn=name_cn,
            fifa_code=code, group=group,
            elo_rating=round(_elo_from_rank(rank), 1),
            fifa_rank=rank,
        ))
    return teams


def create_group_matches(teams: list[Team]) -> list[Match]:
    """生成 12 组小组赛对阵 (每组 6 场 = 72 场)"""
    matches = []
    match_id = 1
    groups = {}
    for t in teams:
        groups.setdefault(t.group, []).append(t)

    # 小组赛日期：6月11日～6月27日
    group_dates = [
        # 每个比赛日 4-6 场比赛，这里简化处理
        datetime(2026, 6, 11, 13, 0), datetime(2026, 6, 11, 16, 0),
        datetime(2026, 6, 11, 19, 0), datetime(2026, 6, 11, 22, 0),
        datetime(2026, 6, 12, 13, 0), datetime(2026, 6, 12, 16, 0),
        datetime(2026, 6, 12, 19, 0), datetime(2026, 6, 12, 22, 0),
        datetime(2026, 6, 13, 13, 0), datetime(2026, 6, 13, 16, 0),
        datetime(2026, 6, 13, 19, 0), datetime(2026, 6, 13, 22, 0),
        datetime(2026, 6, 14, 13, 0), datetime(2026, 6, 14, 16, 0),
        datetime(2026, 6, 14, 19, 0), datetime(2026, 6, 14, 22, 0),
        datetime(2026, 6, 15, 13, 0), datetime(2026, 6, 15, 16, 0),
        datetime(2026, 6, 15, 19, 0), datetime(2026, 6, 15, 22, 0),
        datetime(2026, 6, 16, 13, 0), datetime(2026, 6, 16, 16, 0),
        datetime(2026, 6, 16, 19, 0), datetime(2026, 6, 16, 22, 0),
        datetime(2026, 6, 17, 13, 0), datetime(2026, 6, 17, 16, 0),
        datetime(2026, 6, 17, 19, 0), datetime(2026, 6, 17, 22, 0),
        datetime(2026, 6, 20, 13, 0), datetime(2026, 6, 20, 16, 0),
        datetime(2026, 6, 20, 19, 0), datetime(2026, 6, 20, 22, 0),
        datetime(2026, 6, 21, 13, 0), datetime(2026, 6, 21, 16, 0),
        datetime(2026, 6, 21, 19, 0), datetime(2026, 6, 21, 22, 0),
        datetime(2026, 6, 22, 13, 0), datetime(2026, 6, 22, 16, 0),
        datetime(2026, 6, 22, 19, 0), datetime(2026, 6, 22, 22, 0),
        datetime(2026, 6, 23, 13, 0), datetime(2026, 6, 23, 16, 0),
        datetime(2026, 6, 23, 19, 0), datetime(2026, 6, 23, 22, 0),
        datetime(2026, 6, 24, 13, 0), datetime(2026, 6, 24, 16, 0),
        datetime(2026, 6, 24, 19, 0), datetime(2026, 6, 24, 22, 0),
        datetime(2026, 6, 25, 13, 0), datetime(2026, 6, 25, 16, 0),
        datetime(2026, 6, 25, 19, 0), datetime(2026, 6, 25, 22, 0),
        datetime(2026, 6, 26, 13, 0), datetime(2026, 6, 26, 16, 0),
        datetime(2026, 6, 26, 19, 0), datetime(2026, 6, 26, 22, 0),
        datetime(2026, 6, 27, 13, 0), datetime(2026, 6, 27, 16, 0),
        datetime(2026, 6, 27, 19, 0), datetime(2026, 6, 27, 22, 0),
    ]

    date_idx = 0
    venues = ["Mexico City", "Guadalajara", "Toronto", "Los Angeles",
              "New York/New Jersey", "Dallas", "Houston", "San Francisco",
              "Atlanta", "Seattle", "Miami", "Philadelphia",
              "Kansas City", "Boston", "Vancouver", "Monterrey"]

    for group_name in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]:
        g = groups[group_name]
        # 小组内对阵: 1v2, 3v4, 1v3, 2v4, 1v4, 2v3
        pairings = [(0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2)]
        for h, a in pairings:
            matches.append(Match(
                id=match_id,
                home_team=g[h],
                away_team=g[a],
                date=group_dates[date_idx],
                stage=MatchStage.GROUP,
                venue=venues[date_idx % len(venues)],
            ))
            match_id += 1
            date_idx += 1

    return matches


def create_knockout_slots() -> list[Match]:
    """创建淘汰赛对阵槽位 (32个空位，等小组赛结束后填充)"""
    matches = []
    match_id = 73  # 小组赛 72 场之后

    # R32: 16 场 (6月28日-7月3日)
    r32_dates = [
        datetime(2026, 6, 28, 13, 0), datetime(2026, 6, 28, 16, 0),
        datetime(2026, 6, 28, 19, 0), datetime(2026, 6, 28, 22, 0),
        datetime(2026, 6, 29, 13, 0), datetime(2026, 6, 29, 16, 0),
        datetime(2026, 6, 29, 19, 0), datetime(2026, 6, 29, 22, 0),
        datetime(2026, 6, 30, 13, 0), datetime(2026, 6, 30, 16, 0),
        datetime(2026, 6, 30, 19, 0), datetime(2026, 6, 30, 22, 0),
        datetime(2026, 7, 1, 13, 0), datetime(2026, 7, 1, 16, 0),
        datetime(2026, 7, 2, 13, 0), datetime(2026, 7, 2, 16, 0),
    ]
    venues_knockout = ["Los Angeles", "San Francisco", "Seattle", "Vancouver",
                       "Houston", "Dallas", "Atlanta", "Miami",
                       "Philadelphia", "Boston", "New York/New Jersey",
                       "Kansas City", "Toronto", "Mexico City", "Guadalajara", "Monterrey"]

    for i in range(16):
        matches.append(Match(
            id=match_id,
            home_team=None, away_team=None,
            date=r32_dates[i],
            stage=MatchStage.R32,
            venue=venues_knockout[i % len(venues_knockout)],
        ))
        match_id += 1

    # R16: 8 场 (7月4日-7月7日)
    r16_dates = [
        datetime(2026, 7, 4, 13, 0), datetime(2026, 7, 4, 16, 0),
        datetime(2026, 7, 5, 13, 0), datetime(2026, 7, 5, 16, 0),
        datetime(2026, 7, 6, 13, 0), datetime(2026, 7, 6, 16, 0),
        datetime(2026, 7, 7, 13, 0), datetime(2026, 7, 7, 16, 0),
    ]
    for i in range(8):
        matches.append(Match(
            id=match_id,
            home_team=None, away_team=None,
            date=r16_dates[i],
            stage=MatchStage.R16,
            venue=venues_knockout[i],
        ))
        match_id += 1

    # QF: 4 场 (7月9日-7月11日)
    qf_dates = [
        datetime(2026, 7, 9, 16, 0), datetime(2026, 7, 9, 20, 0),
        datetime(2026, 7, 10, 16, 0), datetime(2026, 7, 10, 20, 0),
    ]
    for i in range(4):
        matches.append(Match(
            id=match_id,
            home_team=None, away_team=None,
            date=qf_dates[i],
            stage=MatchStage.QF,
            venue=venues_knockout[i],
        ))
        match_id += 1

    # SF: 2 场 (7月14日-7月15日)
    matches.append(Match(id=match_id, home_team=None, away_team=None,
                         date=datetime(2026, 7, 14, 20, 0),
                         stage=MatchStage.SF, venue="Dallas"))
    match_id += 1
    matches.append(Match(id=match_id, home_team=None, away_team=None,
                         date=datetime(2026, 7, 15, 20, 0),
                         stage=MatchStage.SF, venue="Atlanta"))
    match_id += 1

    # Third place (7月18日)
    matches.append(Match(id=match_id, home_team=None, away_team=None,
                         date=datetime(2026, 7, 18, 20, 0),
                         stage=MatchStage.THIRD, venue="Miami"))
    match_id += 1

    # Final (7月19日)
    matches.append(Match(id=match_id, home_team=None, away_team=None,
                         date=datetime(2026, 7, 19, 20, 0),
                         stage=MatchStage.FINAL,
                         venue="New York/New Jersey"))

    return matches


def seed_all(store: Store):
    """一键初始化所有种子数据"""
    store.init_db()

    teams = create_teams()
    for team in teams:
        store.upsert_team(team)

    group_matches = create_group_matches(teams)
    for match in group_matches:
        store.upsert_match(match)

    knockout_slots = create_knockout_slots()
    for match in knockout_slots:
        store.upsert_match(match)
```

- [ ] **Step 2: 验证种子数据能正确插入**

```bash
python -c "
from data.store import Store
from data.seed_data import seed_all, create_teams, create_group_matches, create_knockout_slots

store = Store(':memory:')
seed_all(store)

teams = store.get_all_teams()
print(f'球队数: {len(teams)}')  # 应为 48

matches = store.get_all_matches()
print(f'比赛数: {len(matches)}')  # 应为 72 + 32 = 104

# 检查各阶段比赛数
group = [m for m in matches if m.stage.value == '小组赛']
r32 = [m for m in matches if m.stage.value == '1/16决赛']
print(f'小组赛: {len(group)}, R32: {len(r32)}')

store.close()
"
```

- [ ] **Step 3: Commit**

```bash
git add data/seed_data.py
git commit -m "feat: add seed data — 48 teams + 104 match schedule for 2026 World Cup"
```

---

### Task 5: API 客户端封装

**Files:**
- Create: `data/api_client.py`

**注**: API 依赖 football-data.org 的 API Key。如果没有 Key，系统仍可通过种子数据和手动结果更新运行。

- [ ] **Step 1: 实现 data/api_client.py**

```python
"""football-data.org API 封装 (带缓存)"""
import time
import logging
from datetime import date, datetime
from functools import wraps
from typing import Optional, List, Dict, Any
import requests
from config import API_BASE_URL, API_KEY, API_CACHE_TTL

logger = logging.getLogger(__name__)

# 简易内存缓存
_cache: Dict[str, tuple[float, Any]] = {}


def cached(ttl: int = API_CACHE_TTL):
    """装饰器：缓存结果 ttl 秒"""
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
    """足球数据 API 客户端"""

    def __init__(self, api_key: str = API_KEY):
        self.api_key = api_key
        self.headers = {"X-Auth-Token": api_key} if api_key else {}
        self.available = bool(api_key)

    def _get(self, endpoint: str, params: dict = None) -> Optional[dict]:
        """发送 GET 请求"""
        if not self.available:
            logger.warning("API Key 未配置，跳过 API 请求")
            return None
        try:
            url = f"{API_BASE_URL}/{endpoint}"
            resp = requests.get(url, headers=self.headers,
                                params=params, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            logger.error(f"API 请求失败: {e}")
            return None

    @cached(ttl=API_CACHE_TTL)
    def get_matches(self, match_date: date) -> Optional[List[dict]]:
        """获取指定日期的比赛 (世界杯 competition_id=2000)"""
        data = self._get("competitions/2000/matches", {
            "dateFrom": match_date.isoformat(),
            "dateTo": match_date.isoformat(),
        })
        return data.get("matches", []) if data else None

    @cached(ttl=API_CACHE_TTL)
    def get_team_recent_matches(self, team_id: int, n: int = 10) -> Optional[List[dict]]:
        """获取球队近期比赛"""
        data = self._get(f"teams/{team_id}/matches", {
            "limit": n,
            "status": "FINISHED",
        })
        return data.get("matches", []) if data else None

    @cached(ttl=API_CACHE_TTL)
    def get_head_to_head(self, team_id_a: int, team_id_b: int,
                         n: int = 5) -> Optional[List[dict]]:
        """获取两队历史交锋记录"""
        data = self._get(f"matches", {
            "team1": team_id_a,
            "team2": team_id_b,
            "limit": n,
            "status": "FINISHED",
        })
        return data.get("matches", []) if data else None

    @cached(ttl=86400)  # 球队信息缓存1天
    def get_team(self, team_id: int) -> Optional[dict]:
        """获取球队详情"""
        return self._get(f"teams/{team_id}")

    def get_match_day_summary(self, match_date: date) -> Dict:
        """获取某比赛日摘要 (用于 Web 展示)"""
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
        return {
            "date": match_date.isoformat(),
            "matches": summary,
            "total": len(summary),
        }
```

- [ ] **Step 2: Commit**

```bash
git add data/api_client.py
git commit -m "feat: add API client — football-data.org wrapper with caching"
```

---

### Task 6: Elo 评分引擎

**Files:**
- Create: `engine/elo.py`, `tests/test_elo.py`

- [ ] **Step 1: 编写 Elo 测试**

```python
"""engine/elo.py 的单元测试"""
import pytest
from engine.elo import EloEngine


class TestEloEngine:
    def test_expected_win_rate_equal_teams(self):
        """同分球队应有 50% 胜率"""
        engine = EloEngine()
        rate = engine.expected_win_rate(2000, 2000)
        assert rate == pytest.approx(0.5, abs=0.01)

    def test_expected_win_rate_stronger(self):
        """高分球队胜率应大于 50%"""
        engine = EloEngine()
        rate = engine.expected_win_rate(2100, 1900)
        assert rate > 0.7  # 200分差，胜率约76%

    def test_expected_win_rate_weaker(self):
        """低分球队胜率应小于 50%"""
        engine = EloEngine()
        rate = engine.expected_win_rate(1800, 2000)
        assert rate < 0.3

    def test_update_elo_win(self):
        """赢球应加分"""
        engine = EloEngine()
        old_elo = 2000
        new_elo = engine.update_elo(
            team_elo=old_elo, opponent_elo=2000,
            result=1, goal_diff=2, is_knockout=False
        )
        assert new_elo > old_elo

    def test_update_elo_loss(self):
        """输球应扣分"""
        engine = EloEngine()
        old_elo = 2000
        new_elo = engine.update_elo(
            team_elo=old_elo, opponent_elo=2000,
            result=0, goal_diff=-2, is_knockout=False
        )
        assert new_elo < old_elo

    def test_update_elo_draw(self):
        """平局：高分扣分，低分加分"""
        engine = EloEngine()
        # 高分队平局
        new_strong = engine.update_elo(
            team_elo=2100, opponent_elo=1900,
            result=0.5, goal_diff=0, is_knockout=False
        )
        assert new_strong < 2100  # 高分队小扣
        # 低分队平局
        new_weak = engine.update_elo(
            team_elo=1900, opponent_elo=2100,
            result=0.5, goal_diff=0, is_knockout=False
        )
        assert new_weak > 1900  # 低分队小加

    def test_knockout_k_is_higher(self):
        """淘汰赛 K 值更大，变化幅度更大"""
        engine = EloEngine()
        group_change = engine.update_elo(
            team_elo=2000, opponent_elo=2000,
            result=1, goal_diff=1, is_knockout=False
        ) - 2000
        knockout_change = engine.update_elo(
            team_elo=2000, opponent_elo=2000,
            result=1, goal_diff=1, is_knockout=True
        ) - 2000
        assert abs(knockout_change) > abs(group_change)

    def test_goal_diff_multiplier(self):
        """大胜加分更多"""
        engine = EloEngine()
        small_win = engine.update_elo(
            team_elo=2000, opponent_elo=2000,
            result=1, goal_diff=1, is_knockout=False
        )
        big_win = engine.update_elo(
            team_elo=2000, opponent_elo=2000,
            result=1, goal_diff=3, is_knockout=False
        )
        assert big_win > small_win

    def test_get_home_advantage(self):
        """主队应有 Elo 加分"""
        engine = EloEngine()
        home_elo = engine.get_effective_elo(2000, is_home=True)
        away_elo = engine.get_effective_elo(2000, is_home=False)
        assert home_elo > away_elo
```

- [ ] **Step 2: 实现 engine/elo.py**

```python
"""Elo 动态评分系统"""
from config import (
    ELO_INIT_TOP, ELO_RANK_STEP,
    ELO_K_GROUP, ELO_K_KNOCKOUT, ELO_HOME_ADVANTAGE
)


class EloEngine:
    def __init__(self):
        self.k_group = ELO_K_GROUP
        self.k_knockout = ELO_K_KNOCKOUT
        self.home_advantage = ELO_HOME_ADVANTAGE

    def initial_elo(self, fifa_rank: int) -> float:
        """FIFA 排名 → 初始 Elo 分"""
        return round(ELO_INIT_TOP - (fifa_rank - 1) * ELO_RANK_STEP, 1)

    def expected_win_rate(self, elo_a: float, elo_b: float) -> float:
        """计算 A 队对 B 队的期望胜率 (0~1)"""
        return 1.0 / (1.0 + 10.0 ** ((elo_b - elo_a) / 400.0))

    def update_elo(self, team_elo: float, opponent_elo: float,
                   result: float, goal_diff: int, is_knockout: bool) -> float:
        """
        赛后更新 Elo 分
        - result: 1=赢, 0.5=平, 0=输
        - goal_diff: 净胜球 (正=赢, 负=输, 0=平)
        """
        k = self.k_knockout if is_knockout else self.k_group
        expected = self.expected_win_rate(team_elo, opponent_elo)

        # 进球差系数
        abs_diff = abs(goal_diff)
        if abs_diff <= 1:
            g = 1.0
        elif abs_diff == 2:
            g = 1.5
        else:
            g = 1.75

        new_elo = team_elo + k * g * (result - expected)
        return round(new_elo, 1)

    def get_effective_elo(self, elo: float, is_home: bool) -> float:
        """获取考虑主场优势后的有效 Elo"""
        return elo + self.home_advantage if is_home else elo
```

- [ ] **Step 3: 运行测试**

```bash
python -m pytest tests/test_elo.py -v
```
Expected: All PASS

- [ ] **Step 4: Commit**

```bash
git add engine/elo.py tests/test_elo.py
git commit -m "feat: add Elo rating engine with goal-diff multiplier and home advantage"
```

---

### Task 7: 泊松分布 & 蒙特卡洛模拟

**Files:**
- Create: `engine/poisson.py`, `tests/test_poisson.py`

- [ ] **Step 1: 编写泊松测试**

```python
"""engine/poisson.py 的单元测试"""
import pytest
import numpy as np
from engine.poisson import PoissonSimulator


class TestPoissonSimulator:
    def test_calc_lambda(self):
        sim = PoissonSimulator()
        home_lam, away_lam = sim.calc_lambda(elo_diff=100, is_home=True)
        assert home_lam > away_lam
        assert home_lam > 1.0
        assert away_lam > 0.3
        assert home_lam < 4.0

    def test_calc_lambda_equal_teams(self):
        sim = PoissonSimulator()
        home_lam, away_lam = sim.calc_lambda(elo_diff=0, is_home=True)
        # 主场优势
        assert home_lam > away_lam

    def test_calc_lambda_no_home(self):
        sim = PoissonSimulator()
        home_lam, away_lam = sim.calc_lambda(elo_diff=0, is_home=False)
        # 无主场优势
        assert abs(home_lam - away_lam) < 0.01

    def test_simulate_returns_valid_probabilities(self):
        sim = PoissonSimulator()
        result = sim.simulate(home_lambda=1.8, away_lambda=1.2)
        win, draw, lose, exp_hg, exp_ag = result

        # 概率之和应为 100%
        assert abs(win + draw + lose - 100.0) < 1.0

        # 各项应在合理范围
        assert 0 <= win <= 100
        assert 0 <= draw <= 100
        assert 0 <= lose <= 100

        # 预期进球应合理
        assert 0.5 < exp_hg < 3.5
        assert 0.5 < exp_ag < 3.5

    def test_simulate_favors_stronger_team(self):
        sim = PoissonSimulator()
        result_strong = sim.simulate(home_lambda=2.5, away_lambda=1.0)
        win, _, _, _, _ = result_strong
        assert win > 50  # 强队胜率应大于 50%

    def test_simulate_reproducibility(self):
        """设定随机种子验证可复现性"""
        sim1 = PoissonSimulator(seed=42)
        r1 = sim1.simulate(1.5, 1.5)

        sim2 = PoissonSimulator(seed=42)
        r2 = sim2.simulate(1.5, 1.5)

        assert r1 == r2

    def test_expected_goals_reasonable(self):
        """预期进球在合理范围内"""
        sim = PoissonSimulator()
        result = sim.simulate(home_lambda=1.5, away_lambda=1.5)
        _, _, _, exp_hg, exp_ag = result
        assert 1.0 < exp_hg < 2.0
        assert 1.0 < exp_ag < 2.0
```

- [ ] **Step 2: 实现 engine/poisson.py**

```python
"""泊松分布 + 蒙特卡洛模拟"""
import numpy as np
from config import (
    BASE_LAMBDA, LAMBDA_PER_100_ELO,
    HOME_LAMBDA_BONUS, LAMBDA_MIN, LAMBDA_MAX, MONTE_CARLO_N
)


class PoissonSimulator:
    def __init__(self, seed: int = None, n_simulations: int = MONTE_CARLO_N):
        self.rng = np.random.RandomState(seed)
        self.n = n_simulations

    def calc_lambda(self, elo_diff: float, is_home: bool) -> tuple[float, float]:
        """
        根据 Elo 分差计算预期进球数 λ
        elo_diff = 主队 Elo - 客队 Elo
        """
        elo_bonus = (elo_diff / 100.0) * LAMBDA_PER_100_ELO
        home_lam = BASE_LAMBDA + elo_bonus
        away_lam = BASE_LAMBDA - elo_bonus

        if is_home:
            home_lam += HOME_LAMBDA_BONUS

        home_lam = max(LAMBDA_MIN, min(LAMBDA_MAX, home_lam))
        away_lam = max(LAMBDA_MIN, min(LAMBDA_MAX, away_lam))

        return home_lam, away_lam

    def simulate(self, home_lambda: float, away_lambda: float) -> tuple:
        """
        蒙特卡洛模拟 N 场比赛
        返回: (胜率%, 平率%, 负率%, 预期主队进球, 预期客队进球)
        """
        home_goals = self.rng.poisson(home_lambda, self.n)
        away_goals = self.rng.poisson(away_lambda, self.n)

        home_wins = int(np.sum(home_goals > away_goals))
        draws = int(np.sum(home_goals == away_goals))
        away_wins = int(np.sum(home_goals < away_goals))

        return (
            round(home_wins / self.n * 100, 1),
            round(draws / self.n * 100, 1),
            round(away_wins / self.n * 100, 1),
            round(float(np.mean(home_goals)), 1),
            round(float(np.mean(away_goals)), 1),
        )
```

- [ ] **Step 3: 运行测试**

```bash
python -m pytest tests/test_poisson.py -v
```
Expected: All PASS

- [ ] **Step 4: Commit**

```bash
git add engine/poisson.py tests/test_poisson.py
git commit -m "feat: add Poisson Monte Carlo simulation engine"
```

---

### Task 8: 调整因子

**Files:**
- Create: `engine/adjustments.py`, `tests/test_adjustments.py`

- [ ] **Step 1: 编写调整因子测试**

```python
"""engine/adjustments.py 的单元测试"""
import pytest
from engine.adjustments import AdjustmentEngine


class TestAdjustmentEngine:
    def test_recent_form_hot_team(self):
        """近期状态好 (近5场4胜) → 正调整"""
        engine = AdjustmentEngine()
        factor = engine._recent_form_factor([1, 1, 1, 1, 0])
        assert factor > 0

    def test_recent_form_cold_team(self):
        """近期状态差 (近5场1胜) → 负调整"""
        engine = AdjustmentEngine()
        factor = engine._recent_form_factor([0, 0, 0, 0, 1])
        assert factor < 0

    def test_recent_form_empty(self):
        """无近期数据 → 调整=0"""
        engine = AdjustmentEngine()
        factor = engine._recent_form_factor([])
        assert factor == 0

    def test_h2h_dominant(self):
        """交锋记录占优 → 正调整"""
        engine = AdjustmentEngine()
        factor = engine._h2h_factor([1, 1, 1])
        assert factor > 0

    def test_h2h_empty(self):
        engine = AdjustmentEngine()
        factor = engine._h2h_factor([])
        assert factor == 0

    def test_rest_penalty(self):
        """休息不足 → 负调整"""
        engine = AdjustmentEngine()
        factor = engine._rest_factor(rest_days=2)
        assert factor < 0

    def test_rest_no_penalty(self):
        """充足休息 → 调整=0"""
        engine = AdjustmentEngine()
        factor = engine._rest_factor(rest_days=5)
        assert factor == 0

    def test_apply_adjustments_bounded(self):
        """调整总量不超过 ±10%"""
        engine = AdjustmentEngine()
        win, draw, lose = 50.0, 25.0, 25.0
        adj_win, adj_draw, adj_lose = engine.apply(
            win, draw, lose,
            recent_form_home=[1, 1, 1, 1, 1],  # 100%
            recent_form_away=[0, 0, 0, 0, 0],  # 0%
            h2h_results=[1, 1, 1],             # 主场全胜
            rest_days_home=4,
            rest_days_away=2,
        )
        # 总调整不超过 ±10%
        assert abs(adj_win - win) <= 12  # 主客同时作用可能超一点
        assert abs(adj_draw - draw) <= 12
        assert adj_win + adj_draw + adj_lose == pytest.approx(100.0, abs=1.0)

    def test_no_data_no_adjustment(self):
        """无数据时不做调整"""
        engine = AdjustmentEngine()
        win, draw, lose = 50.0, 25.0, 25.0
        adj_win, adj_draw, adj_lose = engine.apply(
            win, draw, lose,
            recent_form_home=[], recent_form_away=[],
            h2h_results=[], rest_days_home=5, rest_days_away=5,
        )
        assert adj_win == win
        assert adj_draw == draw
        assert adj_lose == lose
```

- [ ] **Step 2: 实现 engine/adjustments.py**

```python
"""预测调整因子"""
from config import ADJ_RECENT_FORM_WEIGHT, ADJ_H2H_WEIGHT, ADJ_REST_WEIGHT


class AdjustmentEngine:
    def __init__(self):
        self.recent_weight = ADJ_RECENT_FORM_WEIGHT
        self.h2h_weight = ADJ_H2H_WEIGHT
        self.rest_weight = ADJ_REST_WEIGHT

    def _recent_form_factor(self, recent_results: list) -> float:
        """
        近期状态因子
        recent_results: 近5场比赛结果 [1, 0.5, 1, ...]
        与历史50%胜率比较偏差
        """
        if not recent_results:
            return 0.0
        win_rate = sum(recent_results) / len(recent_results)
        deviation = win_rate - 0.5
        return deviation * self.recent_weight

    def _h2h_factor(self, h2h_results: list) -> float:
        """
        历史交锋因子
        h2h_results: 主队视角的交锋结果
        """
        if not h2h_results:
            return 0.0
        win_rate = sum(h2h_results) / len(h2h_results)
        deviation = win_rate - 0.5
        return deviation * self.h2h_weight

    def _rest_factor(self, rest_days: int) -> float:
        """休息天数惩罚：<3天则减分"""
        if rest_days < 3:
            return -(3 - rest_days) * self.rest_weight / 2
        return 0.0

    def apply(self, win_pct: float, draw_pct: float, lose_pct: float,
              recent_form_home: list = None, recent_form_away: list = None,
              h2h_results: list = None,
              rest_days_home: int = 5, rest_days_away: int = 5) -> tuple:
        """
        对基础概率施加调整因子
        返回: (调整后胜率, 调整后平率, 调整后负率)
        """
        recent_form_home = recent_form_home or []
        recent_form_away = recent_form_away or []
        h2h_results = h2h_results or []

        home_adj = (
            self._recent_form_factor(recent_form_home)
            - self._recent_form_factor(recent_form_away)
            + self._h2h_factor(h2h_results)
            + self._rest_factor(rest_days_home)
            - self._rest_factor(rest_days_away)
        )

        # 调整胜/负率，平率不变
        adj_win = win_pct * (1 + home_adj)
        adj_lose = lose_pct * (1 - home_adj)

        # 归一化使总和=100%
        total = adj_win + draw_pct + adj_lose
        if total > 0:
            adj_win = adj_win / total * 100
            adj_lose = adj_lose / total * 100
            draw_pct = draw_pct / total * 100

        return (
            round(adj_win, 1),
            round(draw_pct, 1),
            round(adj_lose, 1),
        )
```

- [ ] **Step 3: 运行测试**

```bash
python -m pytest tests/test_adjustments.py -v
```
Expected: All PASS

- [ ] **Step 4: Commit**

```bash
git add engine/adjustments.py tests/test_adjustments.py
git commit -m "feat: add prediction adjustment factors — form, H2H, rest"
```

---

### Task 9: 预测编排器

**Files:**
- Create: `engine/predictor.py`, `tests/test_predictor.py`

- [ ] **Step 1: 编写编排器测试**

```python
"""engine/predictor.py 的单元测试"""
import pytest
from datetime import datetime
from engine.predictor import Predictor
from data.models import Team, Match, MatchStage


@pytest.fixture
def predictor():
    return Predictor(seed=42)


@pytest.fixture
def strong_team():
    return Team(id=1, name="Brazil", name_cn="巴西",
                fifa_code="BRA", group="C", elo_rating=2100.0, fifa_rank=3)


@pytest.fixture
def weak_team():
    return Team(id=2, name="Haiti", name_cn="海地",
                fifa_code="HAI", group="C", elo_rating=1600.0, fifa_rank=87)


class TestPredictor:
    def test_predict_returns_valid_prediction(self, predictor, strong_team, weak_team):
        match = Match(id=1, home_team=strong_team, away_team=weak_team,
                      date=datetime(2026, 6, 13), stage=MatchStage.GROUP,
                      venue="NY")
        pred = predictor.predict(strong_team, weak_team, match)

        assert pred.home_win_pct > pred.away_win_pct
        assert pred.home_win_pct > 50
        assert abs(pred.home_win_pct + pred.draw_pct + pred.away_win_pct - 100) < 2
        assert pred.elo_diff == 500.0

    def test_predict_equal_teams(self, predictor):
        t1 = Team(id=1, name="Netherlands", name_cn="荷兰",
                  fifa_code="NED", group="F", elo_rating=2000.0, fifa_rank=6)
        t2 = Team(id=2, name="Japan", name_cn="日本",
                  fifa_code="JPN", group="F", elo_rating=2000.0, fifa_rank=17)
        match = Match(id=1, home_team=t1, away_team=t2,
                      date=datetime(2026, 6, 14), stage=MatchStage.GROUP,
                      venue="Dallas")
        pred = predictor.predict(t1, t2, match)

        # 实力相近，概率应接近
        assert 30 < pred.home_win_pct < 60
        assert 20 < pred.draw_pct < 40

    def test_confidence_high_for_large_diff(self, predictor, strong_team, weak_team):
        match = Match(id=1, home_team=strong_team, away_team=weak_team,
                      date=datetime(2026, 6, 13), stage=MatchStage.GROUP,
                      venue="NY")
        pred = predictor.predict(strong_team, weak_team, match)
        assert pred.confidence == "高"

    def test_confidence_low_for_small_diff(self, predictor):
        t1 = Team(id=1, name="Netherlands", name_cn="荷兰",
                  fifa_code="NED", group="F", elo_rating=2000.0, fifa_rank=6)
        t2 = Team(id=2, name="Sweden", name_cn="瑞典",
                  fifa_code="SWE", group="F", elo_rating=1980.0, fifa_rank=26)
        match = Match(id=1, home_team=t1, away_team=t2,
                      date=datetime(2026, 6, 14), stage=MatchStage.GROUP,
                      venue="Dallas")
        pred = predictor.predict(t1, t2, match)
        assert pred.confidence == "低"

    def test_predict_batch(self, predictor, strong_team, weak_team):
        """批量预测"""
        t3 = Team(id=3, name="Germany", name_cn="德国",
                  fifa_code="GER", group="E", elo_rating=2050.0, fifa_rank=10)
        t4 = Team(id=4, name="Ecuador", name_cn="厄瓜多尔",
                  fifa_code="ECU", group="E", elo_rating=1820.0, fifa_rank=30)

        m1 = Match(id=1, home_team=strong_team, away_team=weak_team,
                   date=datetime(2026, 6, 13), stage=MatchStage.GROUP, venue="NY")
        m2 = Match(id=2, home_team=t3, away_team=t4,
                   date=datetime(2026, 6, 14), stage=MatchStage.GROUP, venue="Houston")

        results = predictor.predict_batch([m1, m2])
        assert len(results) == 2
        assert 1 in results
        assert 2 in results
        assert results[1].home_win_pct > 50  # 巴西对海地
```

- [ ] **Step 2: 实现 engine/predictor.py**

```python
"""预测编排器 — 整合 Elo + 泊松 + 调整因子"""
from data.models import Team, Match, Prediction
from engine.elo import EloEngine
from engine.poisson import PoissonSimulator
from engine.adjustments import AdjustmentEngine


class Predictor:
    def __init__(self, seed: int = None):
        self.elo = EloEngine()
        self.poisson = PoissonSimulator(seed=seed)
        self.adjustments = AdjustmentEngine()

    def predict(self, home: Team, away: Team, match: Match) -> Prediction:
        """对单场比赛执行完整预测"""
        # 1. Elo 分差 (考虑主场)
        home_eff = self.elo.get_effective_elo(home.elo_rating, is_home=True)
        away_eff = self.elo.get_effective_elo(away.elo_rating, is_home=False)
        elo_diff = home_eff - away_eff

        # 2. 泊松模拟
        home_lam, away_lam = self.poisson.calc_lambda(
            elo_diff, is_home=True
        )
        win, draw, lose, exp_hg, exp_ag = self.poisson.simulate(
            home_lam, away_lam
        )

        # 3. 调整因子 (种子数据阶段暂时用空列表)
        win, draw, lose = self.adjustments.apply(
            win, draw, lose,
            recent_form_home=[],
            recent_form_away=[],
            h2h_results=[],
        )

        # 4. 置信度
        confidence = self._calc_confidence(abs(elo_diff))

        return Prediction(
            home_win_pct=win,
            draw_pct=draw,
            away_win_pct=lose,
            expected_home_goals=exp_hg,
            expected_away_goals=exp_ag,
            elo_diff=round(elo_diff, 1),
            confidence=confidence,
        )

    def predict_batch(self, matches: list[Match]) -> dict[int, Prediction]:
        """批量预测多场比赛"""
        results = {}
        for match in matches:
            if match.home_team and match.away_team:
                results[match.id] = self.predict(
                    match.home_team, match.away_team, match
                )
        return results

    def _calc_confidence(self, abs_elo_diff: float) -> str:
        """根据 Elo 分差评估预测置信度"""
        if abs_elo_diff >= 200:
            return "高"
        elif abs_elo_diff >= 80:
            return "中"
        else:
            return "低"
```

- [ ] **Step 3: 运行测试**

```bash
python -m pytest tests/test_predictor.py -v
```
Expected: All PASS

- [ ] **Step 4: Commit**

```bash
git add engine/predictor.py tests/test_predictor.py
git commit -m "feat: add predictor orchestrator — integrates Elo, Poisson, adjustments"
```

---

### Task 10: Web 主题和 UI 组件

**Files:**
- Create: `web/theme.py`, `web/components.py`

- [ ] **Step 1: 实现 web/theme.py**

```python
"""深色运动主题 CSS 注入"""
import streamlit as st
from config import THEME


def inject_theme():
    """将自定义深色主题注入 Streamlit"""
    css = f"""
    <style>
    /* === 全局 === */
    .stApp {{
        background-color: {THEME['bg_dark']};
        color: {THEME['text_primary']};
    }}
    .stMainBlockContainer {{
        padding-top: 1rem;
    }}

    /* === 侧边栏 === */
    [data-testid="stSidebar"] {{
        background-color: {THEME['card_bg']};
        border-right: 1px solid {THEME['border']};
    }}

    /* === 标题 === */
    h1, h2, h3 {{
        color: {THEME['text_primary']} !important;
    }}
    h1 {{
        font-size: 2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }}

    /* === 比赛卡片 === */
    .match-card {{
        background: linear-gradient(135deg, {THEME['card_bg']}, #0F1428);
        border-left: 4px solid {THEME['primary']};
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        transition: all 0.2s ease;
        cursor: pointer;
    }}
    .match-card:hover {{
        border-left-color: #3B82F6;
        box-shadow: 0 4px 20px rgba(12, 74, 209, 0.15);
        transform: translateX(2px);
    }}

    /* === 统计卡片 === */
    .stat-card {{
        background: {THEME['card_bg']};
        border-radius: 12px;
        padding: 20px 16px;
        text-align: center;
        border: 1px solid {THEME['border']};
    }}
    .stat-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {THEME['primary']};
        line-height: 1.2;
    }}
    .stat-label {{
        font-size: 0.85rem;
        color: {THEME['text_secondary']};
        margin-top: 4px;
    }}

    /* === 进度条 === */
    .progress-container {{
        display: flex;
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        background: #1E2340;
        margin: 12px 0 8px 0;
    }}
    .progress-win {{
        background: {THEME['win']};
        transition: width 0.3s ease;
    }}
    .progress-draw {{
        background: {THEME['draw']};
        transition: width 0.3s ease;
    }}
    .progress-lose {{
        background: {THEME['lose']};
        transition: width 0.3s ease;
    }}

    /* === 概率标签 === */
    .pct-label {{
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: {THEME['text_secondary']};
    }}
    .pct-label .win {{ color: {THEME['win']}; font-weight: 600; }}
    .pct-label .draw {{ color: {THEME['draw']}; font-weight: 600; }}
    .pct-label .lose {{ color: {THEME['lose']}; font-weight: 600; }}

    /* === 比分预测 === */
    .score-prediction {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {THEME['primary']};
        text-align: center;
        margin-top: 8px;
    }}

    /* === 置信度标签 === */
    .confidence-tag {{
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }}
    .confidence-high {{ background: rgba(16, 185, 129, 0.15); color: {THEME['win']}; }}
    .confidence-mid {{ background: rgba(245, 158, 11, 0.15); color: {THEME['draw']}; }}
    .confidence-low {{ background: rgba(239, 68, 68, 0.15); color: {THEME['lose']}; }}

    /* === 按钮 === */
    .stButton > button {{
        background: {THEME['primary']} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        transition: all 0.2s !important;
    }}
    .stButton > button:hover {{
        background: #3B82F6 !important;
        box-shadow: 0 4px 12px rgba(12, 74, 209, 0.3) !important;
    }}

    /* === 选择框 === */
    .stSelectbox [data-baseweb="select"] {{
        background: {THEME['card_bg']} !important;
        border-color: {THEME['border']} !important;
    }}

    /* === 日期输入 === */
    .stDateInput [data-baseweb="input"] {{
        background: {THEME['card_bg']} !important;
        border-color: {THEME['border']} !important;
        color: {THEME['text_primary']} !important;
    }}

    /* === 数据表格 === */
    [data-testid="stDataFrame"] {{
        background: {THEME['card_bg']} !important;
    }}

    /* === 展开器 === */
    .streamlit-expander {{
        background: {THEME['card_bg']} !important;
        border: 1px solid {THEME['border']} !important;
        border-radius: 8px !important;
    }}

    /* === 页脚 === */
    .footer {{
        text-align: center;
        color: {THEME['text_secondary']};
        font-size: 0.8rem;
        padding: 20px 0;
        border-top: 1px solid {THEME['border']};
        margin-top: 40px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
```

- [ ] **Step 2: 实现 web/components.py**

```python
"""复用 UI 组件"""
import streamlit as st
from config import THEME
from data.seed_data import FLAG_MAP
from data.models import Match, Prediction, Team


def match_card(match: Match, show_detail: bool = True):
    """渲染一张比赛预测卡片"""
    home = match.home_team
    away = match.away_team
    pred = match.prediction

    home_flag = FLAG_MAP.get(home.fifa_code, "")
    away_flag = FLAG_MAP.get(away.fifa_code, "")

    card_html = f"""
    <div class="match-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1; text-align: right; font-size: 1.1rem; font-weight: 600;">
                {home_flag} {home.name_cn}
            </div>
            <div style="margin: 0 20px; color: {THEME['text_secondary']}; font-size: 0.85rem;">
                VS
            </div>
            <div style="flex: 1; font-size: 1.1rem; font-weight: 600;">
                {away_flag} {away.name_cn}
            </div>
        </div>
    """

    if pred:
        card_html += f"""
        <div style="text-align: center; margin-top: 4px; font-size: 0.8rem; color: {THEME['text_secondary']};">
            {match.stage.value} · {match.venue} · Elo差: {pred.elo_diff:+.0f}
            <span class="confidence-tag confidence-{
                'high' if pred.confidence == '高' else 'mid' if pred.confidence == '中' else 'low'
            }" style="margin-left: 8px;">置信度: {pred.confidence}</span>
        </div>
        <div class="progress-container">
            <div class="progress-win" style="width: {pred.home_win_pct}%;"></div>
            <div class="progress-draw" style="width: {pred.draw_pct}%;"></div>
            <div class="progress-lose" style="width: {pred.away_win_pct}%;"></div>
        </div>
        <div class="pct-label">
            <span class="win">胜 {pred.home_win_pct}%</span>
            <span class="draw">平 {pred.draw_pct}%</span>
            <span class="lose">负 {pred.away_win_pct}%</span>
        </div>
        <div class="score-prediction">
            ⚽ 预测比分: {pred.expected_home_goals} - {pred.expected_away_goals}
        </div>
        """
    else:
        card_html += f"""
        <div style="text-align: center; margin-top: 12px; color: {THEME['text_secondary']}; font-size: 0.9rem;">
            {match.stage.value} · {match.date.strftime('%m月%d日 %H:%M')} · {match.venue}
        </div>
        <div style="text-align: center; margin-top: 4px; color: {THEME['text_secondary']}; font-size: 0.8rem;">
            暂无预测数据
        </div>
        """

    card_html += "</div>"
    st.markdown(card_html, unsafe_allow_html=True)

    # 展开详情
    if show_detail and pred:
        with st.expander(f"📊 {home.name_cn} vs {away.name_cn} 详细数据"):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(f"{home_flag} {home.name_cn} Elo", f"{home.elo_rating:.0f}")
                st.metric("FIFA 排名", f"#{home.fifa_rank}")
            with col2:
                st.metric(f"{away_flag} {away.name_cn} Elo", f"{away.elo_rating:.0f}")
                st.metric("FIFA 排名", f"#{away.fifa_rank}")
            with col3:
                st.metric("Elo 分差", f"{pred.elo_diff:+.0f}")
                st.metric("置信度", pred.confidence)


def stat_cards(today_count: int, predicted_count: int, total_count: int):
    """顶部统计卡片行"""
    cols = st.columns(3)
    with cols[0]:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{today_count}</div>
            <div class="stat-label">🏟️ 今日比赛</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{predicted_count}</div>
            <div class="stat-label">🔮 已预测场次</div>
        </div>
        """, unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{total_count}</div>
            <div class="stat-label">📅 总比赛数</div>
        </div>
        """, unsafe_allow_html=True)


def team_selector(teams: list[Team], key: str = "team_select") -> Team | None:
    """球队下拉选择器"""
    options = {f"{FLAG_MAP.get(t.fifa_code, '')} {t.name_cn} ({t.fifa_code})": t
               for t in teams}
    selected = st.selectbox(
        "选择球队", list(options.keys()), key=key
    )
    return options.get(selected)


def footer():
    """页脚"""
    st.markdown("""
    <div class="footer">
        🏆 2026 FIFA World Cup 预测系统 · 仅供娱乐参考 · 数据基于数学模型
    </div>
    """, unsafe_allow_html=True)
```

- [ ] **Step 3: Commit**

```bash
git add web/theme.py web/components.py
git commit -m "feat: add web theme (dark sports blue) and reusable UI components"
```

---

### Task 11: Streamlit 主入口

**Files:**
- Create: `web/app.py`

- [ ] **Step 1: 实现 web/app.py**

```python
"""2026 世界杯预测系统 — Streamlit 主入口"""
import streamlit as st
from datetime import date, datetime

from web.theme import inject_theme
from data.store import Store
from data.seed_data import seed_all
from engine.predictor import Predictor


def main():
    # 页面配置
    st.set_page_config(
        page_title="2026 世界杯预测",
        page_icon="🏆",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # 注入深色主题
    inject_theme()

    # 初始化数据库
    if "store" not in st.session_state:
        store = Store()
        if store.is_empty():
            seed_all(store)
        st.session_state.store = store

    # 初始化预测器
    if "predictor" not in st.session_state:
        st.session_state.predictor = Predictor(seed=42)

    # 侧边栏
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 2.5rem; margin: 0;">🏆</h1>
            <h2 style="font-size: 1.2rem; margin: 8px 0; color: #0C4AD1;">
                2026 世界杯预测
            </h2>
            <p style="font-size: 0.75rem; color: #8892B0;">
                加拿大 · 墨西哥 · 美国
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # 导航 (Streamlit pages 会自动显示)
        st.markdown(f"""
        <div style="font-size: 0.85rem; color: #8892B0; margin-bottom: 8px;">
            📋 导航
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # 数据状态
        store = st.session_state.store
        team_count = len(store.get_all_teams())
        match_count = len(store.get_all_matches())
        upcoming = len(store.get_upcoming_matches())

        st.markdown(f"""
        <div style="font-size: 0.8rem; color: #8892B0; line-height: 1.8;">
            📊 球队: <b style="color: #fff;">{team_count}</b> 支<br>
            📅 比赛: <b style="color: #fff;">{match_count}</b> 场<br>
            ⏳ 待赛: <b style="color: #0C4AD1;">{upcoming}</b> 场
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        st.markdown(f"""
        <div style="font-size: 0.7rem; color: #8892B0;">
            🕐 数据更新: {datetime.now().strftime('%m/%d %H:%M')}<br>
            📡 API 状态: 离线模式
        </div>
        """, unsafe_allow_html=True)

    # 页面标题
    st.title("🏆 2026 世界杯预测中心")
    st.markdown("""
    <p style="color: #8892B0; font-size: 0.9rem; margin-bottom: 24px;">
        基于 Elo 评分 + 泊松分布的数学预测模型 · 数据驱动 · 仅供参考
    </p>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 验证 Streamlit 能启动**

```bash
streamlit run web/app.py --server.headless true &
sleep 3
curl -s http://localhost:8501 | head -20
kill %1
```

- [ ] **Step 3: Commit**

```bash
git add web/app.py
git commit -m "feat: add Streamlit main entry with sidebar navigation and theme"
```

---

### Task 12: 赛程预测页面

**Files:**
- Create: `web/pages/01_赛程预测.py`

- [ ] **Step 1: 实现 web/pages/01_赛程预测.py**

```python
"""赛程预测页面"""
import streamlit as st
from datetime import date, timedelta, datetime
from web.components import match_card, stat_cards, footer
from engine.predictor import Predictor


def show():
    store = st.session_state.store
    predictor: Predictor = st.session_state.predictor

    # 日期选择器
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_date = st.date_input(
            "📅 选择日期",
            value=date.today(),
            min_value=date(2026, 6, 11),
            max_value=date(2026, 7, 19),
        )

    # 统计
    all_matches = store.get_all_matches()
    today_matches = store.get_matches_by_date(selected_date)
    predicted = [m for m in all_matches if m.prediction is not None]

    stat_cards(
        today_count=len(today_matches),
        predicted_count=len(predicted),
        total_count=len(all_matches),
    )

    st.divider()

    if not today_matches:
        st.info(f"📭 {selected_date} 当天没有安排比赛")
        footer()
        return

    st.subheader(f"📋 {selected_date.strftime('%m月%d日')} 比赛 ({len(today_matches)} 场)")

    # 为每场比赛生成预测
    for match in today_matches:
        if match.home_team and match.away_team:
            if match.prediction is None:
                pred = predictor.predict(match.home_team, match.away_team, match)
                store.save_prediction(match.id, pred)
                match.prediction = pred
            match_card(match)

    footer()


show()
```

- [ ] **Step 2: Commit**

```bash
git add web/pages/01_赛程预测.py
git commit -m "feat: add schedule & prediction page — daily matches with win rates"
```

---

### Task 13: 球队分析页面

**Files:**
- Create: `web/pages/02_球队分析.py`

- [ ] **Step 1: 实现 web/pages/02_球队分析.py**

```python
"""球队分析页面"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from web.components import team_selector, footer
from web.theme import THEME


def show():
    store = st.session_state.store
    teams = store.get_all_teams()

    if not teams:
        st.warning("暂无球队数据")
        return

    st.subheader("📊 球队深度分析")

    team = team_selector(teams)
    if not team:
        footer()
        return

    # 球队基本信息卡片
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Elo 评分", f"{team.elo_rating:.0f}")
    with col2:
        st.metric("🏅 FIFA 排名", f"#{team.fifa_rank}")
    with col3:
        group_teams = store.get_teams_by_group(team.group)
        elo_ranks = sorted([t.elo_rating for t in group_teams], reverse=True)
        group_rank = elo_ranks.index(team.elo_rating) + 1
        st.metric("📊 小组内 Elo 排名", f"#{group_rank}/4")
    with col4:
        st.metric("🏟️ 小组", f"组 {team.group}")

    st.divider()

    # Elo 历史趋势图
    st.subheader("📈 Elo 变化趋势")

    history = store.get_elo_history(team.id)
    if history:
        df = pd.DataFrame(history)
        df["updated_at"] = pd.to_datetime(df["updated_at"])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["updated_at"], y=df["new_elo"],
            mode="lines+markers",
            line=dict(color=THEME["primary"], width=2),
            marker=dict(size=6, color=THEME["primary"]),
            name="Elo",
            hovertemplate="%{y:.0f}<extra></extra>",
        ))

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=THEME["bg_dark"],
            plot_bgcolor=THEME["card_bg"],
            font=dict(color=THEME["text_secondary"]),
            xaxis=dict(gridcolor=THEME["border"], title=""),
            yaxis=dict(gridcolor=THEME["border"], title="Elo 评分"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=300,
            hovermode="x",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无 Elo 历史数据 (比赛尚未开始)")

    # 同组对手对比
    st.subheader(f"🏟️ 组 {team.group} 实力对比")

    group_teams = store.get_teams_by_group(team.group)
    if group_teams:
        df_group = pd.DataFrame([
            {"球队": t.name_cn, "Elo": t.elo_rating, "FIFA排名": t.fifa_rank}
            for t in group_teams
        ]).sort_values("Elo", ascending=False)

        fig2 = go.Figure()
        colors = [THEME["primary"] if t.name_cn == team.name_cn else THEME["text_secondary"]
                  for t in group_teams]
        fig2.add_trace(go.Bar(
            x=[t.name_cn for t in sorted(group_teams, key=lambda t: t.elo_rating, reverse=True)],
            y=[t.elo_rating for t in sorted(group_teams, key=lambda t: t.elo_rating, reverse=True)],
            marker_color=colors,
            text=[f"{t.elo_rating:.0f}" for t in sorted(group_teams, key=lambda t: t.elo_rating, reverse=True)],
            textposition="outside",
            textfont=dict(color=THEME["text_primary"]),
        ))
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor=THEME["bg_dark"],
            plot_bgcolor=THEME["card_bg"],
            font=dict(color=THEME["text_secondary"]),
            xaxis=dict(gridcolor=THEME["border"], title=""),
            yaxis=dict(gridcolor=THEME["border"], title="Elo 评分"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=300,
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    footer()


show()
```

- [ ] **Step 2: Commit**

```bash
git add web/pages/02_球队分析.py
git commit -m "feat: add team analysis page — Elo trend chart and group comparison"
```

---

### Task 14: 淘汰赛模拟页面

**Files:**
- Create: `web/pages/03_淘汰赛模拟.py`

- [ ] **Step 1: 实现 web/pages/03_淘汰赛模拟.py**

```python
"""淘汰赛模拟页面"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from collections import Counter
from web.components import footer
from web.theme import THEME
from engine.elo import EloEngine


def simulate_knockout_match(team_a, team_b, elo: EloEngine, rng: np.random.RandomState) -> object:
    """模拟一场淘汰赛，返回胜者"""
    if team_a is None:
        return team_b
    if team_b is None:
        return team_a

    # 获取有效 Elo (单场淘汰赛，中立场地，A队轻微"主场")
    elo_a = elo.get_effective_elo(team_a.elo_rating, is_home=False)
    elo_b = elo.get_effective_elo(team_b.elo_rating, is_home=False)

    expected_a = elo.expected_win_rate(elo_a, elo_b)

    # 随机决定胜者 (忽略平局，淘汰赛必须分胜负)
    return team_a if rng.random() < expected_a else team_b


def run_tournament_simulation(teams, elo, rng, n_sims=1000):
    """运行整个淘汰赛模拟 N 次"""
    win_counts = Counter()

    for _ in range(n_sims):
        # 随机抽签 (32 强)
        shuffled = teams.copy()
        rng.shuffle(shuffled)

        # R32 → R16 → QF → SF → Final
        round_teams = shuffled
        while len(round_teams) > 1:
            next_round = []
            for i in range(0, len(round_teams), 2):
                winner = simulate_knockout_match(
                    round_teams[i], round_teams[i + 1] if i + 1 < len(round_teams) else None,
                    elo, rng
                )
                next_round.append(winner)
            round_teams = next_round

        if round_teams:
            win_counts[round_teams[0].name_cn] += 1

    return win_counts


def show():
    store = st.session_state.store

    st.subheader("🏆 淘汰赛模拟器")
    st.markdown(f"""
    <p style="color: {THEME['text_secondary']}; font-size: 0.85rem; margin-bottom: 20px;">
        基于当前 Elo 评分，模拟淘汰赛 1000 次，统计各球队夺冠概率。<br>
        小组赛结束后，将使用实际对阵表替换随机抽签。
    </p>
    """, unsafe_allow_html=True)

    # 获取所有球队
    all_teams = store.get_all_teams()

    if not all_teams:
        st.warning("暂无球队数据")
        return

    # 按 Elo 排序取前 32 名
    top32 = sorted(all_teams, key=lambda t: t.elo_rating, reverse=True)[:32]

    # 一键模拟按钮
    if st.button("🎲 一键模拟淘汰赛 (1000次)", type="primary", use_container_width=True):
        with st.spinner("正在进行 1000 次淘汰赛模拟..."):
            elo = EloEngine()
            rng = np.random.RandomState(42)
            win_counts = run_tournament_simulation(top32, elo, rng, n_sims=1000)

        # 夺冠概率排行
        st.subheader("👑 夺冠概率 TOP 20")

        df = pd.DataFrame([
            {"球队": team, "夺冠概率%": round(count / 10, 1)}
            for team, count in win_counts.most_common(20)
        ])

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df["球队"][::-1],
            x=df["夺冠概率%"][::-1],
            orientation="h",
            marker=dict(
                color=df["夺冠概率%"][::-1],
                colorscale=[
                    [0, THEME["lose"]],
                    [0.5, THEME["draw"]],
                    [1, THEME["win"]],
                ],
                showscale=False,
            ),
            text=[f"{v}%" for v in df["夺冠概率%"][::-1]],
            textposition="outside",
            textfont=dict(color=THEME["text_primary"]),
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=THEME["bg_dark"],
            plot_bgcolor=THEME["card_bg"],
            font=dict(color=THEME["text_secondary"]),
            xaxis=dict(gridcolor=THEME["border"], title="夺冠概率 (%)"),
            yaxis=dict(gridcolor=THEME["border"], title=""),
            margin=dict(l=0, r=40, t=10, b=0),
            height=500,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        # 晋级概率表
        st.subheader("📋 前 16 名球队晋级概率")

        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]
        rounds = ["32强", "16强", "8强", "4强", "决赛"]

        for i, (team_name, win_count) in enumerate(win_counts.most_common(16)):
            with cols[i % 5]:
                st.markdown(f"""
                <div class="stat-card" style="padding: 12px; margin-bottom: 8px;">
                    <div style="font-weight: 600; font-size: 0.95rem;">{team_name}</div>
                    <div style="font-size: 1.5rem; color: {THEME['primary']}; margin: 4px 0;">
                        {win_count / 10:.1f}%
                    </div>
                    <div style="font-size: 0.7rem; color: {THEME['text_secondary']};">夺冠概率</div>
                </div>
                """, unsafe_allow_html=True)

        st.caption(f"💡 模拟基于前 32 Elo 排名球队随机对阵，共 1000 次迭代。")

    else:
        # 默认展示 TOP 10 Elo 球队
        st.info("👆 点击上方按钮开始模拟")
        st.subheader("📊 当前 Elo TOP 10")

        top10 = top32[:10]
        df_top = pd.DataFrame([
            {"排名": i + 1, "球队": t.name_cn, "Elo": t.elo_rating, "FIFA排名": t.fifa_rank}
            for i, t in enumerate(top10)
        ])
        st.dataframe(df_top, hide_index=True, use_container_width=True)

    footer()


show()
```

- [ ] **Step 2: Commit**

```bash
git add web/pages/03_淘汰赛模拟.py
git commit -m "feat: add knockout simulation page — Monte Carlo tournament with win probability"
```

---

### Task 15: 收尾 — README + 完整验证

**Files:**
- Create: `README.md`

- [ ] **Step 1: 编写 README.md**

```markdown
# 🏆 2026 世界杯预测中心

基于 **Elo 评分系统 + 泊松分布蒙特卡洛模拟** 的 2026 年世界杯比赛胜率预测工具。

## 快速开始

```bash
# 1. 克隆/进入项目
cd fifa_world_project

# 2. 安装依赖
pip install -r requirements.txt

# 3. (可选) 配置 API Key — 编辑 config.py
# API_KEY = "your-football-data-api-key"

# 4. 启动
streamlit run web/app.py

# 访问 http://localhost:8501
```

## 功能

| 页面 | 功能 |
|------|------|
| 🏠 赛程预测 | 每日比赛 + 胜/平/负概率预测 |
| 📊 球队分析 | Elo 趋势图 + 同组实力对比 |
| 🏆 淘汰赛模拟 | 蒙特卡洛淘汰赛 1000 次模拟 + 夺冠概率 |

## 预测方法

1. **Elo 评分**: 48 支球队基于 FIFA 排名初始化，赛后动态更新
2. **泊松模拟**: 根据 Elo 分差估算预期进球数，10,000 次蒙特卡洛
3. **调整因子**: 近期状态、历史交锋、休息天数修正

## 数据

- 2026 世界杯完整赛程 (48 队 × 12 组 = 104 场)
- 数据来源: football-data.org API

## 免责声明

本工具仅供娱乐参考，不构成任何博彩建议。
```

- [ ] **Step 2: 运行全部测试**

```bash
python -m pytest tests/ -v
```
Expected: All tests PASS (13–15 tests across 6 test files)

- [ ] **Step 3: 验证 Streamlit 可以正常启动**

```bash
streamlit run web/app.py --server.headless true &
sleep 5
curl -s http://localhost:8501 > /dev/null && echo "✅ Streamlit OK" || echo "❌ Failed"
kill %1
```

- [ ] **Step 4: 最终 Commit**

```bash
git add README.md
git commit -m "docs: add README with quick start guide"
```

- [ ] **Step 5: 最终验证 — 确认所有文件就位**

```bash
echo "=== 文件结构 ==="
find . -name "*.py" -o -name "*.md" -o -name "*.txt" -o -name "*.sh" | grep -v __pycache__ | sort
echo ""
echo "=== 测试 ==="
python -m pytest tests/ -v --tb=short
echo ""
echo "=== Git Log ==="
git log --oneline
```

---

## 实现顺序总结

| # | 任务 | 核心产出 |
|---|------|---------|
| 1 | 项目骨架 | requirements.txt, config.py, run.sh |
| 2 | 数据模型 | data/models.py — Team, Match, Prediction |
| 3 | SQLite 存储 | data/store.py — CRUD |
| 4 | 种子数据 | data/seed_data.py — 48队 + 104场赛程 |
| 5 | API 客户端 | data/api_client.py |
| 6 | Elo 引擎 | engine/elo.py |
| 7 | 泊松模拟 | engine/poisson.py |
| 8 | 调整因子 | engine/adjustments.py |
| 9 | 预测编排 | engine/predictor.py |
| 10 | Web 主题 | web/theme.py + web/components.py |
| 11 | 主入口 | web/app.py |
| 12 | 赛程预测 | web/pages/01_赛程预测.py |
| 13 | 球队分析 | web/pages/02_球队分析.py |
| 14 | 淘汰赛模拟 | web/pages/03_淘汰赛模拟.py |
| 15 | 收尾验证 | README.md + 全量测试 |
