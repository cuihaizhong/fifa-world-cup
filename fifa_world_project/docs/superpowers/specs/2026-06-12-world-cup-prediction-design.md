# 2026 世界杯比赛胜率预测 — 设计文档

> 创建日期: 2026-06-12 | 状态: 已确认

---

## 一、项目概述

### 目标
构建一个 2026 年世界杯比赛胜率预测系统，基于球队实力数据，用数学模型预测每场比赛的胜/平/负概率。

### 用户
个人学习和娱乐使用。

### 数据范围
- **赛事**: 2026 FIFA World Cup (加拿大/墨西哥/美国)
- **日期**: 2026年6月11日 — 7月19日
- **规模**: 48 支球队，12 个小组，104 场比赛
- **赛制**: 小组赛 (12组×4队) → 32强 → 16强 → 8强 → 半决赛 → 决赛

---

## 二、技术架构

```
fifa_world_project/
├── data/                       # 数据层
│   ├── __init__.py
│   ├── api_client.py           # 足球数据 API 封装 (football-data.org)
│   ├── models.py               # 数据模型 (Team, Match, Prediction)
│   ├── store.py                # SQLite 本地存储
│   └── seed_data.py            # 预置 48 队 + 104 场赛程
│
├── engine/                     # 预测引擎
│   ├── __init__.py
│   ├── elo.py                  # Elo 动态评分系统
│   ├── poisson.py              # 泊松分布 + 蒙特卡洛模拟
│   ├── adjustments.py          # 调整因子
│   └── predictor.py            # 预测编排器
│
├── web/                        # Web 界面 (Streamlit)
│   ├── __init__.py
│   ├── app.py                  # 主入口 + CSS 主题 + 导航
│   ├── pages/
│   │   ├── 01_赛程预测.py       # 每日比赛 + 胜率
│   │   ├── 02_球队分析.py       # 球队详情 + Elo 趋势
│   │   └── 03_淘汰赛模拟.py      # 淘汰赛对阵 + 夺冠概率
│   └── components.py           # 复用 UI 组件
│
├── config.py                   # 配置项 (API Key, K值, 颜色等)
├── requirements.txt
├── run.sh                      # 启动脚本
└── README.md
```

### 技术栈

| 层级 | 技术 |
|------|------|
| 语言 | Python 3.11+ |
| Web 框架 | Streamlit |
| 数据处理 | pandas, numpy |
| 科学计算 | scipy (泊松分布) |
| HTTP 客户端 | requests + cache |
| 图表 | plotly (深色主题) |
| 本地存储 | SQLite (内置 sqlite3) |
| 数据校验 | pydantic |

---

## 三、数据层详细设计

### 3.1 数据模型 (`models.py`)

```python
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
    name_cn: str              # 中文名
    fifa_code: str            # "ARG", "FRA", "BRA"
    group: str                # "A" ~ "L"
    elo_rating: float         # 当前 Elo 分
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
    home_win_pct: float       # 主队胜率 %
    draw_pct: float           # 平局率 %
    away_win_pct: float       # 客队胜率 %
    expected_home_goals: float
    expected_away_goals: float
    elo_diff: float           # 双方 Elo 分差
    confidence: str           # "高" / "中" / "低"
```

### 3.2 API 封装 (`api_client.py`)

- 封装对 football-data.org 的 HTTP 请求
- **缓存装饰器**: 同一资源 5 分钟内返回缓存，减少 API 调用
- 核心方法:
  - `get_matches(date)` — 获取指定日期赛程
  - `get_team_recent_matches(team_id, n=10)` — 近 N 场比赛
  - `get_head_to_head(team_a_id, team_b_id, n=5)` — 历史交锋

### 3.3 本地存储 (`store.py`)

SQLite 数据库，三张表:

| 表 | 用途 |
|----|------|
| `teams` | 48 支球队基本信息 + 实时 Elo |
| `matches` | 104 场赛程 + 结果 + 预测 |
| `elo_history` | Elo 变动历史 (match_id, team_id, old_elo, new_elo) |

### 3.4 预置数据 (`seed_data.py`)

首次运行时自动初始化:
- 48 支球队信息 (名称、编码、分组)
- 从 FIFA 排名初始化 Elo 分
- 104 场完整赛程 (小组赛 + 淘汰赛对阵槽位)

**12 个小组:**

| 组 | 球队 |
|----|------|
| A | 🇲🇽 墨西哥, 🇿🇦 南非, 🇰🇷 韩国, 🇨🇿 捷克 |
| B | 🇨🇦 加拿大, 🇧🇦 波黑, 🇶🇦 卡塔尔, 🇨🇭 瑞士 |
| C | 🇧🇷 巴西, 🇲🇦 摩洛哥, 🇭🇹 海地, 🏴󠁧󠁢󠁳󠁣󠁴󠁿 苏格兰 |
| D | 🇺🇸 美国, 🇵🇾 巴拉圭, 🇦🇺 澳大利亚, 🇹🇷 土耳其 |
| E | 🇩🇪 德国, 🇨🇼 库拉索, 🇨🇮 科特迪瓦, 🇪🇨 厄瓜多尔 |
| F | 🇳🇱 荷兰, 🇯🇵 日本, 🇸🇪 瑞典, 🇹🇳 突尼斯 |
| G | 🇧🇪 比利时, 🇪🇬 埃及, 🇮🇷 伊朗, 🇳🇿 新西兰 |
| H | 🇪🇸 西班牙, 🇨🇻 佛得角, 🇸🇦 沙特, 🇺🇾 乌拉圭 |
| I | 🇫🇷 法国, 🇸🇳 塞内加尔, 🇮🇶 伊拉克, 🇳🇴 挪威 |
| J | 🇦🇷 阿根廷, 🇩🇿 阿尔及利亚, 🇦🇹 奥地利, 🇯🇴 约旦 |
| K | 🇵🇹 葡萄牙, 🇨🇩 刚果(金), 🇺🇿 乌兹别克斯坦, 🇨🇴 哥伦比亚 |
| L | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 英格兰, 🇭🇷 克罗地亚, 🇬🇭 加纳, 🇵🇦 巴拿马 |

---

## 四、预测引擎详细设计

### 4.1 Elo 评分系统 (`elo.py`)

**初始分数**: 以 FIFA 排名转换，第1名=2100，每降1名−8分，48队范围约 1724-2100。

**胜率期望**:
```
E_a = 1 / (1 + 10^((R_b - R_a) / 400))
```
- `E_a` = A 队期望胜率 (0~1)
- `R_a`, `R_b` = 两队当前 Elo 分

**赛后更新**:
```
R_new = R_old + K * G * (结果 - 预期)
```
- K 值: 小组赛=30, 淘汰赛=60
- G = 进球差系数 (净胜1球=1.0, 2球=1.5, 3球+=1.75)
- 结果: 赢=1, 平=0.5, 输=0

### 4.2 泊松分布模拟 (`poisson.py`)

**预期进球数 (λ)**:
- 基准 λ = 1.5 (国际比赛平均进球)
- 根据 Elo 分差调整: 每 100 分 Elo 优势 ≈ +0.15 λ
- 主场优势: +0.2 λ
- λ 下限 0.3, 上限 4.0

**蒙特卡洛模拟**:
```python
def simulate(home_lambda, away_lambda, n=10000):
    """
    模拟 n 场比赛
    返回: (胜率, 平率, 负率, 预期比分)
    """
    home_wins = draw = away_wins = 0
    home_goals_sum = away_goals_sum = 0

    for _ in range(n):
        hg = np.random.poisson(home_lambda)
        ag = np.random.poisson(away_lambda)
        home_goals_sum += hg
        away_goals_sum += ag
        if hg > ag: home_wins += 1
        elif hg == ag: draw += 1
        else: away_wins += 1

    return (
        home_wins/n * 100,
        draw/n * 100,
        away_wins/n * 100,
        home_goals_sum/n,
        away_goals_sum/n
    )
```

### 4.3 调整因子 (`adjustments.py`)

对泊松结果微调（乘性修正，总和不超过 ±10%）:

| 因子 | 计算方式 | 最大影响 |
|------|----------|---------|
| 近期状态 | 近5场胜率 vs 历史胜率偏差 | ±5% |
| 交锋记录 | 近3次直接对话胜率 | ±3% |
| 休息天数 | < 3天休息则轻微惩罚 | −2% |

调整公式: `final_pct = base_pct * (1 + sum(adjustments))`

### 4.4 预测编排器 (`predictor.py`)

```python
class Predictor:
    def predict(self, home: Team, away: Team, match: Match) -> Prediction:
        elo_diff = home.elo_rating - away.elo_rating
        home_lambda, away_lambda = self._calc_lambda(elo_diff)
        win, draw, lose, exp_hg, exp_ag = simulate(home_lambda, away_lambda)
        win, draw, lose = self._apply_adjustments(
            win, draw, lose, home, away
        )
        return Prediction(
            home_win_pct=win, draw_pct=draw, away_win_pct=lose,
            expected_home_goals=exp_hg, expected_away_goals=exp_ag,
            elo_diff=elo_diff,
            confidence=self._calc_confidence(abs(elo_diff))
        )
```

---

## 五、Web 界面设计

### 5.1 设计系统

| 变量 | 值 | 用途 |
|------|-----|------|
| `--primary` | `#0C4AD1` | 主色 / 链接 / 强调 |
| `--bg-dark` | `#0A0E1A` | 页面背景 |
| `--card-bg` | `#131832` | 卡片背景 |
| `--text-primary` | `#FFFFFF` | 主文字 |
| `--text-secondary` | `#8892B0` | 次文字 |
| `--win` | `#10B981` | 胜率绿色 |
| `--draw` | `#F59E0B` | 平局琥珀色 |
| `--lose` | `#EF4444` | 负率红色 |
| `--border` | `#1E2340` | 边框/分割线 |

### 5.2 页面结构

**主入口 `app.py`**:
- 注入全局深色主题 CSS
- 左侧边栏: 导航链接 + 数据刷新状态
- 页面路由: 赛程预测 → 球队分析 → 淘汰赛模拟

**第 1 页 — 赛程预测 `01_赛程预测.py`**:
- 顶部: 3 张统计卡片 (今日比赛数 / 已预测场次 / 累计更新次数)
- 日期选择器，默认当天
- 比赛卡片列表，每张卡片包含:
  - 双方球队名称 + 国旗 emoji
  - 三色胜率进度条 (绿/琥珀/红)
  - 预测比分
  - 点击展开: 双方近况、Elo 对比、交锋记录
- 自动刷新: 每 6 小时更新一次数据

**第 2 页 — 球队分析 `02_球队分析.py`**:
- 下拉选择球队
- 球队信息卡片: Elo 分、小组排名、FIFA 排名
- Plotly 深色主题折线图: Elo 变化趋势
- 近期比赛列表

**第 3 页 — 淘汰赛模拟 `03_淘汰赛模拟.py`**:
- 淘汰赛对阵树 (32强起)
- 「🎲 一键模拟」按钮: 基于 Elo 逐轮模拟淘汰赛，1000 次迭代
- 夺冠概率排行榜 (横向柱状图)
- 模拟结果: 各轮晋级概率表

### 5.3 全局 CSS 注入

```python
# app.py
def inject_theme():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0A0E1A;
    }
    .match-card {
        background: linear-gradient(135deg, #131832, #0F1428);
        border-left: 4px solid #0C4AD1;
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        transition: all 0.2s;
    }
    .match-card:hover {
        border-left-color: #3B82F6;
        box-shadow: 0 4px 20px rgba(12, 74, 209, 0.15);
    }
    .progress-win { background: #10B981; }
    .progress-draw { background: #F59E0B; }
    .progress-lose { background: #EF4444; }
    .stat-card {
        background: #131832;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0C4AD1;
    }
    </style>
    """, unsafe_allow_html=True)
```

---

## 六、数据流

```
启动时
  └─ seed_data.py 初始化 48 队 + 104 场赛程 → SQLite

用户访问页面
  └─ API Client 获取最新赛程/结果 → 更新 SQLite
       └─ Elo 引擎计算/更新每队分数
            └─ 泊松模拟器对每场未进行的比赛跑预测
                 └─ Store 保存预测结果
                      └─ Streamlit 读取并渲染

比赛结束后
  └─ API 推送结果 → Elo 更新 → 下一轮预测自动刷新
```

---

## 七、依赖清单 (`requirements.txt`)

```
streamlit>=1.28
pandas>=2.0
numpy>=1.24
scipy>=1.10
requests>=2.31
plotly>=5.15
pydantic>=2.0
```

---

## 八、待实现功能 (P2 — 不做初期版本)

- [ ] API Key 不可用时的纯离线模式
- [ ] 用户自定义调整因子权重
- [ ] 预测准确率统计面板
- [ ] 导出预测报告 (PDF)

---

## 九、注意事项

1. **API 额度**: football-data.org 免费版每分钟 10 次请求，需要合理设置缓存
2. **初始 Elo**: 小组赛第一轮预测准确率较低 (无近期比赛数据)，随赛程推进逐步提高
3. **冷门处理**: 泊松模型对低概率事件预测偏保守，冷门 (概率 <15%) 需要单独标注
4. **淘汰赛槽位**: 小组赛结束前淘汰赛对阵未知，需要等 12 个小组排名确定后动态填充
