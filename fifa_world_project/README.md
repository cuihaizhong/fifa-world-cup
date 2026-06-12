# 🏆 2026 世界杯预测中心

基于 **Elo 评分系统 + 泊松分布蒙特卡洛模拟** 的 2026 年世界杯比赛胜率预测工具。

## 快速开始

```bash
# 1. 进入项目
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

## 项目结构

```
fifa_world_project/
├── config.py              # 全局配置
├── data/                  # 数据层
│   ├── models.py          # Team, Match, Prediction
│   ├── store.py           # SQLite 存储
│   ├── seed_data.py       # 48队 + 104场赛程
│   └── api_client.py      # API 封装
├── engine/                # 预测引擎
│   ├── elo.py             # Elo 评分
│   ├── poisson.py         # 泊松模拟
│   ├── adjustments.py     # 调整因子
│   └── predictor.py       # 编排器
├── web/                   # Web 界面
│   ├── app.py             # 主入口
│   ├── theme.py           # 深色主题
│   ├── components.py      # UI 组件
│   └── pages/             # 三个页面
├── tests/                 # 单元测试
└── requirements.txt
```

## 免责声明

本工具仅供娱乐参考，不构成任何博彩建议。
