#!/usr/bin/env python3
"""百度体育全量爬虫 — 使用 urllib 直接抓取，批量爬取 48 队的所有数据。
运行: python3 data/scrape_teams.py
"""
import json, os, re, time, urllib.request, urllib.parse, sys
from html import unescape

CACHE_PATH = os.path.join(os.path.dirname(__file__), "baidu_teams.json")
BAIDU_TEAM = "https://tiyu.baidu.com/al/team?id={tid}&tab={tab}"

TABS = {
    "schedule": "赛程",
    "squad": "阵容",
    "info": "资料",
    "history": "历史成绩",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "zh-CN,zh;q=0.9",
}


def fetch(url: str) -> str:
    """获取页面 HTML 文本"""
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        html = resp.read().decode("utf-8", errors="replace")
    # 去掉 HTML 标签，提取纯文本
    text = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = re.sub(r"\s{3,}", "\n", text)
    return text.strip()


def parse_squad(text: str) -> dict:
    """解析阵容页"""
    result = {"coaches": [], "players": {}}

    # 教练组
    coach_m = re.search(r"教练组\s*\n(.*?)(?=前锋|中场|后卫|门将|\Z)", text, re.DOTALL)
    if coach_m:
        lines = [l.strip() for l in coach_m.group(1).split("\n") if l.strip()]
        for i in range(0, len(lines) - 1, 2):
            if i + 1 < len(lines):
                result["coaches"].append({"name": lines[i], "info": lines[i+1]})

    # 球员 (四个位置)
    for pos in ["前锋", "中场", "后卫", "门将"]:
        next_pos = {"前锋": "中场", "中场": "后卫", "后卫": "门将", "门将": None}[pos]
        pattern = f"{pos}\\s*\\n(.*?)"
        if next_pos:
            pattern += f"(?={next_pos})"
        m = re.search(pattern, text, re.DOTALL)
        if not m:
            continue
        section = m.group(1)
        # 跳过表头 (出场/进球/助攻/身价)
        lines = [l.strip() for l in section.split("\n") if l.strip()]
        # 找到数据起始行 (数字开头的行)
        players = []
        i = 0
        while i < len(lines):
            if re.match(r"^\d{1,2}$", lines[i]):
                if i + 1 < len(lines):
                    name = lines[i+1]
                    # 格式: "姓名 年龄/俱乐部"
                    parts = name.rsplit("/", 1)
                    player_name = parts[0] if len(parts) > 1 else name
                    club = parts[1] if len(parts) > 1 else ""
                    # 下一行是 stats: "出场 进球 助攻"
                    apps = lines[i+2] if i+2 < len(lines) else ""
                    goals = lines[i+3] if i+3 < len(lines) else ""
                    players.append({
                        "number": lines[i],
                        "name": player_name.strip(),
                        "club": club.strip(),
                        "apps": apps.strip(),
                        "goals": goals.strip(),
                    })
                    i += 4
                else:
                    i += 1
            else:
                i += 1
        if players:
            result["players"][pos] = players

    return result


def parse_schedule(text: str) -> list:
    """解析赛程 — 提取我们的数据库赛程作为 fallback"""
    matches = []
    # 匹配标准赛程行: 日期 时间 主队 vs 客队 赛事
    for m in re.finditer(
        r"(\d{2}-\d{2})\S*\s+(\d{2}:\d{2})\s+(.+?)\s+(vs|-)\s+(.+?)\s+(.+)",
        text
    ):
        matches.append({
            "date": m.group(1),
            "time": m.group(2),
            "home": m.group(3).strip(),
            "away": m.group(5).strip(),
            "stage": m.group(6).strip(),
        })
    return matches


def parse_info(text: str) -> dict:
    """解析资料/排名"""
    info = {}
    rank_map = [
        ("世界排名", r"世界排名\s*(\d+)"),
        ("欧洲排名", r"欧洲排名\s*(\d+)"),
        ("亚洲排名", r"亚洲排名\s*(\d+)"),
        ("非洲排名", r"非洲排名\s*(\d+)"),
        ("南美排名", r"南美排名\s*(\d+)"),
        ("中北美排名", r"中北美排名\s*(\d+)"),
    ]
    for key, pattern in rank_map:
        m = re.search(pattern, text)
        if m:
            info[key] = int(m.group(1))
    return info


def parse_history(text: str) -> dict:
    """解析历史成绩"""
    # 提取奖杯/荣誉
    honors = []
    for m in re.finditer(r"(世界杯|欧洲杯|美洲杯|亚洲杯|非洲杯|联合会杯|奥运会|金杯赛)[^\n]*冠军[^\n]*", text):
        honors.append(m.group().strip())
    return {"honors": honors}


def scrape_team(code: str, team_id: str) -> dict:
    """爬取一支球队的全部数据"""
    result = {}
    for key, tab_name in TABS.items():
        encoded = urllib.parse.quote(tab_name)
        url = BAIDU_TEAM.format(tid=team_id, tab=encoded)
        try:
            text = fetch(url)
            time.sleep(0.3)  # 礼貌延迟
        except Exception as e:
            print(f"    ⚠️ {tab_name} 请求失败: {e}")
            continue

        if key == "schedule":
            result["matches"] = parse_schedule(text)
        elif key == "squad":
            result["squad"] = parse_squad(text)
        elif key == "info":
            result["info"] = parse_info(text)
        elif key == "history":
            result["history"] = parse_history(text)

        count = len(result.get({"schedule":"matches","squad":"squad","info":"info","history":"history"}[key], []))
        if isinstance(result.get(key if key=="squad" else ""), dict):
            count = sum(len(v) for v in result["squad"]["players"].values()) + len(result["squad"]["coaches"])
        print(f"    ✅ {tab_name} ({count} items)")

    return result


def main():
    cache = load_cache()
    # 筛选需要爬取的球队 (有 team_id 但没有 squad 的优先)
    targets = [(c, d["team_id"]) for c, d in cache.items() if d.get("team_id")]

    print(f"🎯 开始爬取 {len(targets)} 支球队...\n")
    start = time.time()

    for i, (code, tid) in enumerate(targets):
        # 跳过已经有 squad 数据的
        existing = cache[code]
        if "squad" in existing and existing["squad"].get("players"):
            print(f"[{i+1}/{len(targets)}] {code} — 已有数据，跳过")
            continue

        print(f"[{i+1}/{len(targets)}] {code} ({existing.get('name_cn','')})")
        try:
            team_data = scrape_team(code, tid)
            cache[code] = {**existing, **team_data}
            # 每 5 队保存一次
            if (i + 1) % 5 == 0:
                save_cache(cache)
        except Exception as e:
            print(f"  ❌ 失败: {e}")

    save_cache(cache)
    elapsed = time.time() - start
    print(f"\n✅ 完成! 耗时 {elapsed:.0f}s, 数据保存到 {CACHE_PATH}")


def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(data):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
