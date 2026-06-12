"""种子数据 — 48 支球队 + 104 场比赛赛程"""

from datetime import datetime, timedelta

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

VENUES = [
    "Mexico City", "Guadalajara", "Toronto", "Los Angeles",
    "New York/New Jersey", "Dallas", "Houston", "San Francisco",
    "Atlanta", "Seattle", "Miami", "Philadelphia",
    "Kansas City", "Boston", "Vancouver", "Monterrey",
]

TIME_SLOTS = ["13:00", "16:00", "19:00", "22:00"]
GROUP_START = datetime(2026, 6, 11)
GROUP_PAIRINGS = [(0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2)]

TBD_TEAM = Team(
    id=0, name="TBD", name_cn="待定", fifa_code="TBD",
    group="", elo_rating=0, fifa_rank=0,
)


# ======================================================================
# 4. Helper functions
# ======================================================================

def _elo_from_rank(rank: int) -> float:
    """FIFA 排名 -> Elo 初始分"""
    return ELO_INIT_TOP - (rank - 1) * ELO_RANK_STEP


def _slot_date(slot_index: int, start_date: datetime) -> datetime:
    """Return the datetime for a given sequential slot index."""
    day_offset = slot_index // len(TIME_SLOTS)
    time_str = TIME_SLOTS[slot_index % len(TIME_SLOTS)]
    d = start_date + timedelta(days=day_offset)
    return datetime.fromisoformat(f"{d.date().isoformat()}T{time_str}:00")


def _slot_venue(slot_index: int) -> str:
    """Return the venue for a given sequential slot index (cycles through VENUES)."""
    return VENUES[slot_index % len(VENUES)]


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
# 6. 创建小组赛 — 72 场
# ======================================================================

def create_group_matches(teams: list[Team]) -> list[Match]:
    """Generate 72 group stage matches.

    Each of the 12 groups (A-L) plays 6 matches, using pairings:
    (0,1), (2,3), (0,2), (1,3), (0,3), (1,2).

    Matches are spread across June 11-28, 2026 (18 days x 4 slots = 72),
    with venues cycling through 16 host cities.
    """
    # Build lookup: group_name -> sorted list of teams
    group_map: dict[str, list[Team]] = {}
    for t in teams:
        group_map.setdefault(t.group, []).append(t)
    for g in group_map:
        group_map[g].sort(key=lambda t: t.id)

    matches: list[Match] = []
    match_id = 0
    slot_idx = 0

    for group_name in "ABCDEFGHIJKL":
        g_teams = group_map[group_name]
        for home_idx, away_idx in GROUP_PAIRINGS:
            match_id += 1
            home = g_teams[home_idx]
            away = g_teams[away_idx]

            match_date = _slot_date(slot_idx, GROUP_START)
            venue = _slot_venue(slot_idx)

            matches.append(Match(
                id=match_id,
                home_team=home,
                away_team=away,
                date=match_date,
                stage=MatchStage.GROUP,
                venue=venue,
            ))
            slot_idx += 1

    return matches


# ======================================================================
# 7. 创建淘汰赛占位 — 32 场 (match_id 73-104)
# ======================================================================

def create_knockout_slots() -> list[Match]:
    """Create 32 knockout placeholder matches with TBD teams.

    - R32: 16 matches, June 28 - July 1,   match_id 73-88
    - R16:  8 matches, July  4 - July 7,   match_id 89-96
    - QF:   4 matches, July  9 - July 10,  match_id 97-100
    - SF:   2 matches, July 14 - July 15,  match_id 101-102
    - Third: 1 match,  July 18,            match_id 103
    - Final: 1 match,  July 19,            match_id 104
    """
    matches: list[Match] = []

    stages_def: list[tuple[MatchStage, int, str]] = [
        (MatchStage.R32,   16, "2026-06-28"),
        (MatchStage.R16,    8, "2026-07-04"),
        (MatchStage.QF,     4, "2026-07-09"),
        (MatchStage.SF,     2, "2026-07-14"),
        (MatchStage.THIRD,  1, "2026-07-18"),
        (MatchStage.FINAL,  1, "2026-07-19"),
    ]

    match_id = 72  # will increment to 73 on first iteration

    for stage, count, start_date_str in stages_def:
        start_date = datetime.fromisoformat(start_date_str)
        for i in range(count):
            match_id += 1
            match_date = _slot_date(i, start_date)
            venue = _slot_venue(match_id)  # deterministic spread across venues
            matches.append(Match(
                id=match_id,
                home_team=TBD_TEAM,
                away_team=TBD_TEAM,
                date=match_date,
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
