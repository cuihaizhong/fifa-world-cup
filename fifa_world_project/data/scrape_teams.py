#!/usr/bin/env python3
"""百度体育全量爬虫 v2 — JSON解析，批量爬取48队阵容/排名/荣誉
运行: python3 data/scrape_teams.py
"""
import json, os, re, time, urllib.request, urllib.parse, sys

CACHE_PATH = os.path.join(os.path.dirname(__file__), "baidu_teams.json")
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

TAB_ENCODED = {
    "squad": "%E9%98%B5%E5%AE%B9",
    "info": "%E8%B5%84%E6%96%99",
    "history": "%E5%8E%86%E5%8F%B2%E6%88%90%E7%BB%A9",
}
BAIDU_TEAM = "https://tiyu.baidu.com/al/team?id={tid}&tab={tab}"


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_squad(html: str) -> dict:
    """从HTML中提取阵容JSON数据"""
    result = {"coaches": [], "players": {}}

    # 教练组
    for m in re.finditer(r'\{"avatar":"[^"]*","name":"([^"]+)","subTitle":"([^"]*)","url":"[^"]*","schema":"[^"]*"\}', html):
        result["coaches"].append({"name": m.group(1), "info": m.group(2)})

    # 球员 (按位置)
    for pos in ["前锋", "中场", "后卫", "门将"]:
        pos_m = re.search(f'"position":"{pos}","data":\\[', html)
        if not pos_m:
            continue

        # 用括号匹配找到完整的 data 数组
        start = pos_m.end()
        depth, end = 1, start
        while depth > 0 and end < len(html):
            if html[end] == '[': depth += 1
            elif html[end] == ']': depth -= 1
            end += 1
        section = html[start:end-1]

        # 逐对象JSON解析
        players = []
        d, obj_start = 0, -1
        for i, c in enumerate(section):
            if c == '{':
                if d == 0: obj_start = i
                d += 1
            elif c == '}':
                d -= 1
                if d == 0 and obj_start >= 0:
                    try:
                        obj = json.loads(section[obj_start:i+1])
                        players.append({
                            "name": obj.get("name", ""),
                            "number": obj.get("number", ""),
                            "age": obj.get("age", ""),
                            "club": obj.get("teamName", ""),
                            "apps": obj.get("court", ""),
                            "goals": obj.get("goals", ""),
                            "assists": obj.get("assists", ""),
                            "value": obj.get("value", ""),
                        })
                    except json.JSONDecodeError:
                        pass
                    obj_start = -1

        if players:
            result["players"][pos] = players

    return result


def parse_rankings(html: str) -> dict:
    """提取排名信息"""
    info = {}
    for key, pat in [("世界排名", r"世界排名\s*(\d+)"), ("欧洲排名", r"欧洲排名\s*(\d+)"),
                     ("亚洲排名", r"亚洲排名\s*(\d+)"), ("非洲排名", r"非洲排名\s*(\d+)"),
                     ("南美排名", r"南美排名\s*(\d+)"), ("中北美排名", r"中北美排名\s*(\d+)")]:
        m = re.search(pat, html)
        if m: info[key] = int(m.group(1))
    return info


def parse_history(html: str) -> dict:
    """提取历史荣誉"""
    honors = []
    for m in re.finditer(r"(世界杯|欧洲杯|美洲杯|亚洲杯|非洲杯|联合会杯|奥运会|金杯赛)[^\n]{0,20}冠军[^\n]{0,20}", html):
        honors.append(m.group().strip())
    return {"honors": honors}


def scrape_team(code: str, team_id: str) -> dict:
    result = {}
    for key, tab in TAB_ENCODED.items():
        url = BAIDU_TEAM.format(tid=team_id, tab=tab)
        try:
            html = fetch(url)
            time.sleep(0.3)
        except Exception as e:
            print(f"    ⚠️ {key} 请求失败: {e}")
            continue

        if key == "squad":
            result["squad"] = parse_squad(html)
            p_count = sum(len(v) for v in result["squad"]["players"].values())
            print(f"    ✅ 阵容: {p_count}球员 {len(result['squad']['coaches'])}教练")
        elif key == "info":
            result["info"] = parse_rankings(html)
            print(f"    ✅ 排名: {result['info']}")
        elif key == "history":
            result["history"] = parse_history(html)
            print(f"    ✅ 荣誉: {len(result['history']['honors'])}项")

    return result


def main():
    with open(CACHE_PATH, "r", encoding="utf-8") as f:
        cache = json.load(f)

    targets = [(c, d["team_id"]) for c, d in cache.items() if d.get("team_id")]
    print(f"🎯 开始爬取 {len(targets)} 支球队 (v2 JSON解析)...\n")
    start = time.time()

    for i, (code, tid) in enumerate(targets):
        name = cache[code].get("name_cn", code)
        print(f"[{i+1}/{len(targets)}] {code} ({name})")
        try:
            data = scrape_team(code, tid)
            cache[code] = {**cache[code], **data}
            if (i + 1) % 10 == 0:
                with open(CACHE_PATH, "w", encoding="utf-8") as f:
                    json.dump(cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"  ❌ 失败: {e}")

    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

    elapsed = time.time() - start
    total_p = sum(len(v) for d in cache.values() if "squad" in d
                  for v in d["squad"]["players"].values())
    print(f"\n✅ 完成! {elapsed:.0f}s | {total_p}球员 | 数据: {CACHE_PATH}")


if __name__ == "__main__":
    main()
