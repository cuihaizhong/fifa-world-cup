"""种子数据 — 48 支球队 + 104 场比赛赛程"""

from datetime import datetime

from config import ELO_INIT_TOP, ELO_RANK_STEP
from data.models import Match, MatchStage, Team
from data.store import Store

# ======================================================================
# 1. 球队数据 — 48 队, 按分组整理
# ======================================================================
TEAMS_DATA: list[tuple[int, str, str, str, str, int]] = [
    # Group A
    (1, "Mexico", "墨西哥", "MEX", "A", 15),
    (2, "South Africa", "南非", "RSA", "A", 48),
    (3, "South Korea", "韩国", "KOR", "A", 24),
    (4, "Czechia", "捷克", "CZE", "A", 36),
    # Group B
    (5, "Canada", "加拿大", "CAN", "B", 33),
    (6, "Bosnia & Herzegovina", "波黑", "BIH", "B", 56),
    (7, "Qatar", "卡塔尔", "QAT", "B", 60),
    (8, "Switzerland", "瑞士", "SUI", "B", 19),
    # Group C
    (9, "Brazil", "巴西", "BRA", "C", 5),
    (10, "Morocco", "摩洛哥", "MAR", "C", 13),
    (11, "Haiti", "海地", "HAI", "C", 87),
    (12, "Scotland", "苏格兰", "SCO", "C", 42),
    # Group D
    (13, "United States", "美国", "USA", "D", 11),
    (14, "Paraguay", "巴拉圭", "PAR", "D", 52),
    (15, "Australia", "澳大利亚", "AUS", "D", 27),
    (16, "Türkiye", "土耳其", "TUR", "D", 35),
    # Group E
    (17, "Germany", "德国", "GER", "E", 10),
    (18, "Curaçao", "库拉索", "CUW", "E", 82),
    (19, "Ivory Coast", "科特迪瓦", "CIV", "E", 38),
    (20, "Ecuador", "厄瓜多尔", "ECU", "E", 30),
    # Group F
    (21, "Netherlands", "荷兰", "NED", "F", 6),
    (22, "Japan", "日本", "JPN", "F", 17),
    (23, "Sweden", "瑞典", "SWE", "F", 26),
    (24, "Tunisia", "突尼斯", "TUN", "F", 47),
    # Group G
    (25, "Belgium", "比利时", "BEL", "G", 8),
    (26, "Egypt", "埃及", "EGY", "G", 40),
    (27, "Iran", "伊朗", "IRN", "G", 21),
    (28, "New Zealand", "新西兰", "NZL", "G", 95),
    # Group H
    (29, "Spain", "西班牙", "ESP", "H", 2),
    (30, "Cape Verde", "佛得角", "CPV", "H", 65),
    (31, "Saudi Arabia", "沙特", "KSA", "H", 55),
    (32, "Uruguay", "乌拉圭", "URU", "H", 14),
    # Group I
    (33, "France", "法国", "FRA", "I", 1),
    (34, "Senegal", "塞内加尔", "SEN", "I", 18),
    (35, "Iraq", "伊拉克", "IRQ", "I", 70),
    (36, "Norway", "挪威", "NOR", "I", 43),
    # Group J
    (37, "Argentina", "阿根廷", "ARG", "J", 4),
    (38, "Algeria", "阿尔及利亚", "ALG", "J", 31),
    (39, "Austria", "奥地利", "AUT", "J", 25),
    (40, "Jordan", "约旦", "JOR", "J", 71),
    # Group K
    (41, "Portugal", "葡萄牙", "POR", "K", 7),
    (42, "DR Congo", "刚果(金)", "COD", "K", 63),
    (43, "Uzbekistan", "乌兹别克斯坦", "UZB", "K", 58),
    (44, "Colombia", "哥伦比亚", "COL", "K", 9),
    # Group L
    (45, "England", "英格兰", "ENG", "L", 3),
    (46, "Croatia", "克罗地亚", "CRO", "L", 12),
    (47, "Ghana", "加纳", "GHA", "L", 68),
    (48, "Panama", "巴拿马", "PAN", "L", 44),
]

# ======================================================================
# 2. 国旗 emoji 映射
# ======================================================================
FLAG_MAP: dict[str, str] = {
    "MEX": "\U0001f1f2\U0001f1fd",
    "RSA": "\U0001f1ff\U0001f1e6",
    "KOR": "\U0001f1f0\U0001f1f7",
    "CZE": "\U0001f1e8\U0001f1ff",
    "CAN": "\U0001f1e8\U0001f1e6",
    "BIH": "\U0001f1e7\U0001f1e6",
    "QAT": "\U0001f1f6\U0001f1e6",
    "SUI": "\U0001f1e8\U0001f1ed",
    "BRA": "\U0001f1e7\U0001f1f7",
    "MAR": "\U0001f1f2\U0001f1e6",
    "HAI": "\U0001f1ed\U0001f1f9",
    "SCO": "\U0001f3f4\U000e0067\U000e0062\U000e0073\U000e0063\U000e0074\U000e007f",
    "USA": "\U0001f1fa\U0001f1f8",
    "PAR": "\U0001f1f5\U0001f1fe",
    "AUS": "\U0001f1e6\U0001f1fa",
    "TUR": "\U0001f1f9\U0001f1f7",
    "GER": "\U0001f1e9\U0001f1ea",
    "CUW": "\U0001f1e8\U0001f1fc",
    "CIV": "\U0001f1e8\U0001f1ee",
    "ECU": "\U0001f1ea\U0001f1e8",
    "NED": "\U0001f1f3\U0001f1f1",
    "JPN": "\U0001f1ef\U0001f1f5",
    "SWE": "\U0001f1f8\U0001f1ea",
    "TUN": "\U0001f1f9\U0001f1f3",
    "BEL": "\U0001f1e7\U0001f1ea",
    "EGY": "\U0001f1ea\U0001f1ec",
    "IRN": "\U0001f1ee\U0001f1f7",
    "NZL": "\U0001f1f3\U0001f1ff",
    "ESP": "\U0001f1ea\U0001f1f8",
    "CPV": "\U0001f1e8\U0001f1fb",
    "KSA": "\U0001f1f8\U0001f1e6",
    "URU": "\U0001f1fa\U0001f1fe",
    "FRA": "\U0001f1eb\U0001f1f7",
    "SEN": "\U0001f1f8\U0001f1f3",
    "IRQ": "\U0001f1ee\U0001f1f6",
    "NOR": "\U0001f1f3\U0001f1f4",
    "ARG": "\U0001f1e6\U0001f1f7",
    "ALG": "\U0001f1e9\U0001f1ff",
    "AUT": "\U0001f1e6\U0001f1f9",
    "JOR": "\U0001f1ef\U0001f1f4",
    "POR": "\U0001f1f5\U0001f1f9",
    "COD": "\U0001f1e8\U0001f1e9",
    "UZB": "\U0001f1fa\U0001f1ff",
    "COL": "\U0001f1e8\U0001f1f4",
    "ENG": "\U0001f3f4\U000e0067\U000e0062\U000e0065\U000e006e\U000e0067\U000e007f",
    "CRO": "\U0001f1ed\U0001f1f7",
    "GHA": "\U0001f1ec\U0001f1ed",
    "PAN": "\U0001f1f5\U0001f1e6",
}

# ======================================================================
# 3. 常量
# ======================================================================

TBD_TEAM = Team(
    id=0, name="TBD", name_cn="待定", fifa_code="TBD",
    group="", elo_rating=0, fifa_rank=0,
)

# 官方 2026 世界杯小组赛赛程 (72场)
# 格式: (日期, 主队CODE, 客队CODE, 组别, 球场)
GROUP_SCHEDULE = [
    # === 6月11日 (周四) ===
    (1,  "2026-06-11 13:00", "MEX", "RSA", "A", "Mexico City"),
    (2,  "2026-06-11 16:00", "KOR", "CZE", "A", "Guadalajara"),
    # === 6月12日 (周五) ===
    (3,  "2026-06-12 13:00", "CAN", "BIH", "B", "Toronto"),
    (4,  "2026-06-12 16:00", "USA", "PAR", "D", "Los Angeles"),
    # === 6月13日 (周六) ===
    (5,  "2026-06-13 13:00", "HAI", "SCO", "C", "Boston"),
    (6,  "2026-06-13 16:00", "AUS", "TUR", "D", "Vancouver"),
    (7,  "2026-06-13 19:00", "BRA", "MAR", "C", "New York/New Jersey"),
    (8,  "2026-06-13 22:00", "QAT", "SUI", "B", "San Francisco"),
    # === 6月14日 (周日) ===
    (9,  "2026-06-14 13:00", "CIV", "ECU", "E", "Philadelphia"),
    (10, "2026-06-14 16:00", "GER", "CUW", "E", "Houston"),
    (11, "2026-06-14 19:00", "NED", "JPN", "F", "Dallas"),
    (12, "2026-06-14 22:00", "SWE", "TUN", "F", "Monterrey"),
    # === 6月15日 (周一) ===
    (13, "2026-06-15 13:00", "KSA", "URU", "H", "Miami"),
    (14, "2026-06-15 16:00", "ESP", "CPV", "H", "Atlanta"),
    (15, "2026-06-15 19:00", "IRN", "NZL", "G", "Los Angeles"),
    (16, "2026-06-15 22:00", "BEL", "EGY", "G", "Seattle"),
    # === 6月16日 (周二) ===
    (17, "2026-06-16 13:00", "FRA", "SEN", "I", "New York/New Jersey"),
    (18, "2026-06-16 16:00", "IRQ", "NOR", "I", "Boston"),
    (19, "2026-06-16 19:00", "ARG", "ALG", "J", "Kansas City"),
    (20, "2026-06-16 22:00", "AUT", "JOR", "J", "San Francisco"),
    # === 6月17日 (周三) ===
    (21, "2026-06-17 13:00", "GHA", "PAN", "L", "Toronto"),
    (22, "2026-06-17 16:00", "ENG", "CRO", "L", "Dallas"),
    (23, "2026-06-17 19:00", "POR", "COD", "K", "Houston"),
    (24, "2026-06-17 22:00", "UZB", "COL", "K", "Mexico City"),
    # === 6月18日 (周四) — 小组第2轮 ===
    (25, "2026-06-18 13:00", "CZE", "RSA", "A", "Atlanta"),
    (26, "2026-06-18 16:00", "SUI", "BIH", "B", "Los Angeles"),
    (27, "2026-06-18 19:00", "CAN", "QAT", "B", "Vancouver"),
    (28, "2026-06-18 22:00", "MEX", "KOR", "A", "Guadalajara"),
    # === 6月19日 (周五) ===
    (29, "2026-06-19 13:00", "BRA", "HAI", "C", "Philadelphia"),
    (30, "2026-06-19 16:00", "SCO", "MAR", "C", "Boston"),
    (31, "2026-06-19 19:00", "TUR", "PAR", "D", "San Francisco"),
    (32, "2026-06-19 22:00", "USA", "AUS", "D", "Seattle"),
    # === 6月20日 (周六) ===
    (33, "2026-06-20 13:00", "GER", "CIV", "E", "Toronto"),
    (34, "2026-06-20 16:00", "ECU", "CUW", "E", "Kansas City"),
    (35, "2026-06-20 19:00", "NED", "SWE", "F", "Houston"),
    (36, "2026-06-20 22:00", "TUN", "JPN", "F", "Monterrey"),
    # === 6月21日 (周日) ===
    (37, "2026-06-21 13:00", "URU", "CPV", "H", "Miami"),
    (38, "2026-06-21 16:00", "ESP", "KSA", "H", "Atlanta"),
    (39, "2026-06-21 19:00", "BEL", "IRN", "G", "Los Angeles"),
    (40, "2026-06-21 22:00", "NZL", "EGY", "G", "Vancouver"),
    # === 6月22日 (周一) ===
    (41, "2026-06-22 13:00", "NOR", "SEN", "I", "New York/New Jersey"),
    (42, "2026-06-22 16:00", "FRA", "IRQ", "I", "Philadelphia"),
    (43, "2026-06-22 19:00", "ARG", "AUT", "J", "Dallas"),
    (44, "2026-06-22 22:00", "JOR", "ALG", "J", "San Francisco"),
    # === 6月23日 (周二) ===
    (45, "2026-06-23 13:00", "ENG", "GHA", "L", "Boston"),
    (46, "2026-06-23 16:00", "PAN", "CRO", "L", "Toronto"),
    (47, "2026-06-23 19:00", "POR", "UZB", "K", "Houston"),
    (48, "2026-06-23 22:00", "COL", "COD", "K", "Guadalajara"),
    # === 6月24日 (周三) — 小组第3轮 (A/B/C组) ===
    (49, "2026-06-24 16:00", "SCO", "BRA", "C", "Miami"),
    (50, "2026-06-24 16:00", "MAR", "HAI", "C", "Atlanta"),
    (51, "2026-06-24 20:00", "SUI", "CAN", "B", "Vancouver"),
    (52, "2026-06-24 20:00", "BIH", "QAT", "B", "Seattle"),
    (53, "2026-06-24 20:00", "CZE", "MEX", "A", "Mexico City"),
    (54, "2026-06-24 20:00", "RSA", "KOR", "A", "Monterrey"),
    # === 6月25日 (周四) — 小组第3轮 (D/E/F组) ===
    (55, "2026-06-25 16:00", "CUW", "CIV", "E", "Philadelphia"),
    (56, "2026-06-25 16:00", "ECU", "GER", "E", "New York/New Jersey"),
    (57, "2026-06-25 20:00", "JPN", "SWE", "F", "Dallas"),
    (58, "2026-06-25 20:00", "TUN", "NED", "F", "Kansas City"),
    (59, "2026-06-25 20:00", "TUR", "USA", "D", "Los Angeles"),
    (60, "2026-06-25 20:00", "PAR", "AUS", "D", "San Francisco"),
    # === 6月26日 (周五) — 小组第3轮 (G/H/I组) ===
    (61, "2026-06-26 16:00", "NOR", "FRA", "I", "Boston"),
    (62, "2026-06-26 16:00", "SEN", "IRQ", "I", "Toronto"),
    (63, "2026-06-26 20:00", "EGY", "IRN", "G", "Seattle"),
    (64, "2026-06-26 20:00", "NZL", "BEL", "G", "Vancouver"),
    (65, "2026-06-26 20:00", "CPV", "KSA", "H", "Houston"),
    (66, "2026-06-26 20:00", "URU", "ESP", "H", "Guadalajara"),
    # === 6月27日 (周六) — 小组第3轮 (J/K/L组) ===
    (67, "2026-06-27 16:00", "PAN", "ENG", "L", "New York/New Jersey"),
    (68, "2026-06-27 16:00", "CRO", "GHA", "L", "Philadelphia"),
    (69, "2026-06-27 20:00", "ALG", "AUT", "J", "Kansas City"),
    (70, "2026-06-27 20:00", "JOR", "ARG", "J", "Dallas"),
    (71, "2026-06-27 20:00", "COL", "POR", "K", "Miami"),
    (72, "2026-06-27 20:00", "COD", "UZB", "K", "Atlanta"),
]


# ======================================================================
# 4. Helper functions
# ======================================================================

def _elo_from_rank(rank: int) -> float:
    """FIFA 排名 -> Elo 初始分"""
    return ELO_INIT_TOP - (rank - 1) * ELO_RANK_STEP


# ======================================================================
# 5. 创建球队
# ======================================================================

def create_teams() -> list[Team]:
    """Create 48 Team objects from TEAMS_DATA."""
    teams: list[Team] = []
    for tid, name, name_cn, fifa_code, group, fifa_rank in TEAMS_DATA:
        teams.append(Team(
            id=tid,
            name=name,
            name_cn=name_cn,
            fifa_code=fifa_code,
            group=group,
            elo_rating=_elo_from_rank(fifa_rank),
            fifa_rank=fifa_rank,
        ))
    return teams


# ======================================================================
# 6. 创建小组赛 — 72 场 (官方赛程)
# ======================================================================

def create_group_matches(teams: list[Team]) -> list[Match]:
    """根据 2026 世界杯官方赛程创建 72 场小组赛。"""
    # Build lookup: fifa_code -> Team
    code_map: dict[str, Team] = {t.fifa_code: t for t in teams}
    matches: list[Match] = []
    for mid, date_str, home_code, away_code, group, venue in GROUP_SCHEDULE:
        matches.append(Match(
            id=mid,
            home_team=code_map[home_code],
            away_team=code_map[away_code],
            date=datetime.fromisoformat(date_str),
            stage=MatchStage.GROUP,
            venue=venue,
        ))
    return matches


# ======================================================================
# 7. 创建淘汰赛占位 — 32 场 (match_id 73-104)
# ======================================================================

# 官方淘汰赛对阵表 (match_id, 日期, 阶段, 球场)
KNOCKOUT_SCHEDULE = [
    # === R32: 16 matches (6月28日-7月3日) ===
    (73, "2026-06-28 13:00", MatchStage.R32, "Los Angeles"),
    (74, "2026-06-29 13:00", MatchStage.R32, "Boston"),
    (75, "2026-06-29 16:00", MatchStage.R32, "Monterrey"),
    (76, "2026-06-29 19:00", MatchStage.R32, "Houston"),
    (77, "2026-06-30 13:00", MatchStage.R32, "New York/New Jersey"),
    (78, "2026-06-30 16:00", MatchStage.R32, "Dallas"),
    (79, "2026-06-30 19:00", MatchStage.R32, "Mexico City"),
    (80, "2026-07-01 13:00", MatchStage.R32, "Atlanta"),
    (81, "2026-07-01 16:00", MatchStage.R32, "San Francisco"),
    (82, "2026-07-01 19:00", MatchStage.R32, "Seattle"),
    (83, "2026-07-02 13:00", MatchStage.R32, "Toronto"),
    (84, "2026-07-02 16:00", MatchStage.R32, "Los Angeles"),
    (85, "2026-07-02 19:00", MatchStage.R32, "Vancouver"),
    (86, "2026-07-03 13:00", MatchStage.R32, "Miami"),
    (87, "2026-07-03 16:00", MatchStage.R32, "Kansas City"),
    (88, "2026-07-03 19:00", MatchStage.R32, "Dallas"),
    # === R16: 8 matches (7月4日-7月7日) ===
    (89, "2026-07-04 13:00", MatchStage.R16, "Philadelphia"),
    (90, "2026-07-04 16:00", MatchStage.R16, "Houston"),
    (91, "2026-07-05 13:00", MatchStage.R16, "New York/New Jersey"),
    (92, "2026-07-05 16:00", MatchStage.R16, "Mexico City"),
    (93, "2026-07-06 13:00", MatchStage.R16, "Dallas"),
    (94, "2026-07-06 16:00", MatchStage.R16, "Seattle"),
    (95, "2026-07-07 13:00", MatchStage.R16, "Atlanta"),
    (96, "2026-07-07 16:00", MatchStage.R16, "Vancouver"),
    # === QF: 4 matches (7月9日-7月11日) ===
    (97,  "2026-07-09 16:00", MatchStage.QF, "Boston"),
    (98,  "2026-07-10 16:00", MatchStage.QF, "Los Angeles"),
    (99,  "2026-07-11 16:00", MatchStage.QF, "Miami"),
    (100, "2026-07-11 20:00", MatchStage.QF, "Kansas City"),
    # === SF: 2 matches (7月14日-7月15日) ===
    (101, "2026-07-14 20:00", MatchStage.SF, "Dallas"),
    (102, "2026-07-15 20:00", MatchStage.SF, "Atlanta"),
    # === Third place (7月18日) ===
    (103, "2026-07-18 16:00", MatchStage.THIRD, "Miami"),
    # === Final (7月19日) ===
    (104, "2026-07-19 16:00", MatchStage.FINAL, "New York/New Jersey"),
]


def create_knockout_slots() -> list[Match]:
    """根据官方淘汰赛对阵表创建 32 场淘汰赛占位。"""
    matches: list[Match] = []
    for mid, date_str, stage, venue in KNOCKOUT_SCHEDULE:
        matches.append(Match(
            id=mid,
            home_team=TBD_TEAM,
            away_team=TBD_TEAM,
            date=datetime.fromisoformat(date_str),
            stage=stage,
            venue=venue,
        ))
    return matches


# ======================================================================
# 8. 一键初始化
# ======================================================================

def seed_all(store: Store) -> None:
    """One-call initialization: init_db, upsert all teams and matches."""
    store.init_db()

    # Insert TBD placeholder team first (id=0) so FK constraints pass
    store.upsert_team(TBD_TEAM)

    teams = create_teams()
    for team in teams:
        store.upsert_team(team)

    group_matches = create_group_matches(teams)
    for match in group_matches:
        store.upsert_match(match)

    knockout_matches = create_knockout_slots()
    for match in knockout_matches:
        store.upsert_match(match)

    store._conn.commit()
