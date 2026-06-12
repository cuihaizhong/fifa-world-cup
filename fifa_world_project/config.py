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
