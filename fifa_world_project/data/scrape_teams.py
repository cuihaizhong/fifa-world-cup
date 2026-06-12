#!/usr/bin/env python3
"""百度体育球队数据爬虫 — 批量爬取所有 48 支球队的赛程/阵容/资料/历史成绩

用法:
    python3 data/scrape_teams.py              # 爬取全部 48 队
    python3 data/scrape_teams.py FRA KOR BRA  # 只爬指定球队
    python3 data/scrape_teams.py --top 10     # 只爬 Elo 前 10 名

输出: data/baidu_teams.json (增量更新)
"""

import json
import os
import sys
import time
import re
import argparse
from typing import Optional

CACHE_PATH = os.path.join(os.path.dirname(__file__), "baidu_teams.json")
BAIDU_TEAM_URL = "https://tiyu.baidu.com/al/team?id={team_id}&tab={tab}"

TABS = ["赛程", "阵容", "资料", "历史成绩"]


def load_cache() -> dict:
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(data: dict):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 已保存到 {CACHE_PATH}")


def extract_tab_text(page) -> str:
    """从 Playwright page 中提取当前标签页的纯文本"""
    try:
        page.wait_for_timeout(1500)
        text = page.evaluate("document.body.innerText")
        return text
    except Exception:
        return ""


def parse_squad(text: str) -> dict:
    """解析阵容页文本, 提取教练组和按位置分组的大名单"""
    result = {"coaches": [], "players": {}}

    # 教练组
    coach_start = text.find("教练组")
    positions = ["前锋", "中场", "后卫", "门将"]
    first_pos = min((text.find(p) for p in positions if text.find(p) > 0), default=len(text))
    if coach_start > 0 and first_pos > coach_start:
        coach_text = text[coach_start:first_pos]
        lines = [l.strip() for l in coach_text.split("\n") if l.strip()]
        for i in range(1, len(lines), 3):
            if i + 1 < len(lines):
                result["coaches"].append({
                    "name": lines[i],
                    "info": lines[i + 1],
                })

    # 球员 (按位置)
    for idx, pos in enumerate(positions):
        start = text.find(pos)
        end = text.find(positions[idx + 1]) if idx + 1 < len(positions) else len(text)
        if start < 0:
            continue
        section = text[start:end]
        lines = [l.strip() for l in section.split("\n") if l.strip()]
        players = []
        # 跳过位置标题行和表头 (出场/进球/助攻/身价)
        data_start = 0
        for j, line in enumerate(lines):
            if "身价" in line:
                data_start = j + 1
                break
        for j in range(data_start, len(lines), 5):
            if j + 4 < len(lines):
                players.append({
                    "number": lines[j],
                    "name": lines[j + 1],
                    "club": lines[j + 2],
                    "apps": lines[j + 3],
                    "goals": lines[j + 4].split("/")[0] if "/" in lines[j + 4] else "",
                })
        if players:
            result["players"][pos] = players

    return result


def parse_schedule(text: str) -> list:
    """解析赛程页文本, 提取比赛列表"""
    matches = []
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 匹配日期行: "06-12/今天" 或 "06-19/周五"
        if re.match(r"\d{2}-\d{2}/", line):
            matches.append({"date_label": line})
        # 匹配时间+赛事行
        elif re.match(r"\d{2}:\d{2}", line):
            matches.append({"time": line})
        # 匹配比分
        elif re.match(r".+\s+\d+\s*-\s*\d+\s+.+", line) or "vs" in line.lower():
            matches.append({"fixture": line})
    return matches


def parse_info(text: str) -> dict:
    """解析资料页文本"""
    info = {}
    for key in ["世界排名", "欧洲排名", "亚洲排名", "非洲排名", "南美排名", "中北美排名"]:
        m = re.search(f"{key}(\\d+)", text)
        if m:
            info[key] = int(m.group(1))
    return info


def parse_history(text: str) -> dict:
    """解析历史成绩页文本"""
    return {"raw": text[:1000]}


def scrape_team(page, team_id: str, code: str) -> dict:
    """爬取一支球队的全部数据"""
    data = {"team_id": team_id}

    for tab in TABS:
        tab_encoded = {
            "赛程": "%E8%B5%9B%E7%A8%8B",
            "阵容": "%E9%98%B5%E5%AE%B9",
            "资料": "%E8%B5%84%E6%96%99",
            "历史成绩": "%E5%8E%86%E5%8F%B2%E6%88%90%E7%BB%A9",
        }[tab]
        url = BAIDU_TEAM_URL.format(team_id=team_id, tab=tab_encoded)
        try:
            page.goto(url, timeout=15000)
            text = extract_tab_text(page)

            if tab == "赛程":
                data["schedule"] = parse_schedule(text)
            elif tab == "阵容":
                data["squad"] = parse_squad(text)
            elif tab == "资料":
                data["info"] = parse_info(text)
            elif tab == "历史成绩":
                data["history"] = parse_history(text)

            print(f"    ✅ {tab} ({len(text)} chars)")
        except Exception as e:
            print(f"    ⚠️ {tab} 失败: {e}")
            data[{"赛程": "schedule", "阵容": "squad", "资料": "info", "历史成绩": "history"}[tab]] = None

    return data


def main():
    parser = argparse.ArgumentParser(description="爬取百度体育球队数据")
    parser.add_argument("codes", nargs="*", help="球队 FIFA 代码 (如 FRA BRA)")
    parser.add_argument("--top", type=int, help="只爬 Elo 前 N 名")
    args = parser.parse_args()

    cache = load_cache()

    # 确定要爬的球队
    if args.codes:
        targets = [(c.upper(), cache.get(c.upper(), {}).get("team_id")) for c in args.codes]
    else:
        targets = [(c, d.get("team_id")) for c, d in cache.items() if d.get("team_id")]

    if args.top:
        # 从 seed_data 导入排序
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from data.seed_data import create_teams
        from engine.elo import EloEngine
        elo = EloEngine()
        teams = create_teams()
        teams.sort(key=lambda t: elo.initial_elo(t.fifa_rank), reverse=True)
        top_codes = [t.fifa_code for t in teams[:args.top]]
        targets = [(c, cache.get(c, {}).get("team_id")) for c in top_codes if cache.get(c, {}).get("team_id")]

    print(f"\n{'='*60}")
    print(f"🎯 目标: {len(targets)} 支球队")
    print(f"{'='*60}\n")

    # Playwright 延迟导入
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ 请先安装 Playwright: pip install playwright && playwright install chromium")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for i, (code, team_id) in enumerate(targets):
            if not team_id:
                print(f"  [{i+1}/{len(targets)}] {code} — 无 team_id, 跳过")
                continue

            print(f"  [{i+1}/{len(targets)}] {code} (id={team_id[:8]}...)")
            try:
                team_data = scrape_team(page, team_id, code)
                cache[code] = {**cache.get(code, {}), **team_data}
                save_cache(cache)
            except Exception as e:
                print(f"    ❌ 失败: {e}")

            time.sleep(0.5)  # 礼貌延迟

        browser.close()

    print(f"\n{'='*60}")
    print(f"✅ 完成! 数据已保存到 {CACHE_PATH}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
