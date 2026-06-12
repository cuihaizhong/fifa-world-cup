"""Team Detail View — 百度体育全量数据 + Elo 分析"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from config import THEME
from web.components import footer
from data.seed_data import FLAG_MAP
from data.team_scraper import BaiduTeamScraper


def render_match_row(m: dict):
    home = m.get("home", ""); away = m.get("away", "")
    hs = m.get("home_score", "-"); aws = m.get("away_score", "-")
    status = m.get("status", ""); stage = m.get("stage", "")
    if "进行中" in status: icon, color = "🟢", "#10B981"
    elif "未开赛" in status: icon, color = "⚪", "#F59E0B"
    else: icon, color = "⏹", "#6B7280"
    score = f"{hs} - {aws}" if hs not in (None, "-", "") else "vs"
    st.markdown(f"""
    <div style="background:{THEME['card_bg']};border-radius:8px;padding:8px 14px;margin:4px 0;
                display:flex;align-items:center;justify-content:space-between;font-size:0.9rem;">
        <div style="color:{THEME['text_secondary']};min-width:140px;">{m.get('date','')} {m.get('time','')}</div>
        <div style="font-weight:600;flex:1;text-align:center;">{home} <span style="color:{THEME['primary']};">{score}</span> {away}</div>
        <div style="display:flex;align-items:center;gap:6px;min-width:160px;justify-content:flex-end;">
            <span style="color:{THEME['text_secondary']};font-size:0.8rem;">{stage}</span>
            <span style="color:{color};font-size:0.75rem;">{icon}{status}</span></div></div>""", unsafe_allow_html=True)


def render_squad_table(players: list):
    if not players: st.caption("暂无数据"); return
    rows = [{"号码":p.get("number",""),"姓名":p.get("name",""),"俱乐部":p.get("club",""),
             "出场":p.get("apps",""),"进球":p.get("goals","")} for p in players]
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)


def show_team_detail(team):
    """渲染球队详情页的全部内容。team 为 data.models.Team 对象。"""
    store = st.session_state.store
    scraper = BaiduTeamScraper()
    baidu_data = scraper.get_team_data(team.fifa_code) or {}
    baidu_url = scraper.get_team_url(team.fifa_code)
    flag = FLAG_MAP.get(team.fifa_code, "")

    # 返回首页 (保留 u 参数防丢登录)
    u_param = st.session_state.get("username", "")
    home_url = f"/?u={u_param}" if u_param else "/"
    st.markdown(f'<a href="{home_url}" target="_self" style="color:{THEME["text_secondary"]};text-decoration:none;font-size:0.85rem;">← 返回首页</a>', unsafe_allow_html=True)

    # === HEADER ===
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.markdown(f'<div style="font-size:5rem;text-align:center;line-height:1;">{flag}</div>', unsafe_allow_html=True)
    with col2:
        st.title(team.name_cn)
        rank_info = f"{team.name} · FIFA #{team.fifa_rank} · Elo {team.elo_rating:.0f}"
        wr = baidu_data.get("world_rank") or (baidu_data.get("info", {}).get("世界排名"))
        if wr: rank_info += f" · 百度世界排名 #{wr}"
        st.markdown(f'<p style="color:{THEME["text_secondary"]};font-size:1rem;">{rank_info}</p>', unsafe_allow_html=True)
    with col3:
        if baidu_url:
            st.markdown(f'<a href="{baidu_url}" target="_blank" style="display:inline-block;margin-top:20px;padding:6px 16px;background:{THEME["primary"]};color:#fff;border-radius:8px;text-decoration:none;font-size:0.85rem;">🔗 百度体育</a>', unsafe_allow_html=True)

    st.divider()

    # === 详情标签页 ===
    tab1, tab2, tab3, tab4 = st.tabs(["📋 赛程", "👥 阵容", "📊 资料", "🏅 历史成绩"])

    # TAB 1: 赛程
    with tab1:
        all_matches = store.get_all_matches()
        team_matches = [m for m in all_matches
                      if m.home_team and m.away_team
                      and (m.home_team.fifa_code == team.fifa_code
                           or m.away_team.fifa_code == team.fifa_code)]
        if team_matches:
            for m in team_matches:
                st.markdown(f"""
                <div style="background:{THEME['card_bg']};border-radius:10px;padding:12px 16px;margin:6px 0;
                            display:flex;align-items:center;justify-content:space-between;font-size:0.95rem;
                            border-left:3px solid {THEME['primary']};">
                    <div style="min-width:120px;"><div style="font-weight:600;">{m.date.strftime('%m月%d日')}</div>
                        <div style="color:{THEME['text_secondary']};font-size:0.8rem;">{m.date.strftime('%H:%M')}</div></div>
                    <div style="flex:1;text-align:center;">
                        <span style="font-weight:600;">{FLAG_MAP.get(m.home_team.fifa_code,'')} {m.home_team.name_cn}</span>
                        <span style="color:{THEME['primary']};margin:0 10px;font-weight:700;">VS</span>
                        <span style="font-weight:600;">{FLAG_MAP.get(m.away_team.fifa_code,'')} {m.away_team.name_cn}</span></div>
                    <div style="min-width:160px;text-align:right;">
                        <div style="color:{THEME['text_secondary']};font-size:0.8rem;">{m.stage.value}</div>
                        <div style="color:{THEME['text_secondary']};font-size:0.75rem;">🏟️ {m.venue}</div></div></div>""", unsafe_allow_html=True)
        else:
            st.info("暂无赛程数据")

    # TAB 2: 阵容
    with tab2:
        squad = baidu_data.get("squad", {})
        coaches = squad.get("coaches", []) if isinstance(squad, dict) else []
        if coaches:
            st.subheader("🧑‍🏫 教练组")
            cols = st.columns(min(len(coaches), 5))
            for i, c in enumerate(coaches):
                with cols[i % 5]:
                    st.markdown(f"""<div style="background:{THEME['card_bg']};border-radius:8px;padding:10px;text-align:center;margin:4px 0;">
                        <div style="font-weight:600;font-size:0.9rem;">{c.get('name','')}</div>
                        <div style="color:{THEME['text_secondary']};font-size:0.75rem;">{c.get('info','')}</div></div>""", unsafe_allow_html=True)
        players_by_pos = squad.get("players", {}) if isinstance(squad, dict) else {}
        if players_by_pos:
            for pos, players in players_by_pos.items():
                st.subheader(f"⚽ {pos}")
                render_squad_table(players)
        elif not coaches:
            st.info("暂无阵容数据")

    # TAB 3: 资料
    with tab3:
        info = baidu_data.get("info", {})
        if info:
            rank_cols = st.columns(4)
            rank_keys = [("世界排名","🌍"),("欧洲排名","🏰"),("亚洲排名","🏯"),("非洲排名","🦁"),("南美排名","🦅"),("中北美排名","🌎")]
            ci = 0
            for key, icon in rank_keys:
                if key in info:
                    with rank_cols[ci % 4]: st.metric(f"{icon} {key}", f"#{info[key]}")
                    ci += 1
        st.divider(); st.caption("本系统数据：")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("🎯 Elo 评分", f"{team.elo_rating:.0f}")
        with c2: st.metric("🏅 FIFA 排名", f"#{team.fifa_rank}")
        with c3: st.metric("🏟️ 小组", f"组 {team.group}")

    # TAB 4: 历史成绩
    with tab4:
        history_data = baidu_data.get("history", {}) if isinstance(baidu_data.get("history"), dict) else {}
        honors = history_data.get("honors", []) if isinstance(history_data, dict) else []

        if honors:
            # 解析破碎的 Baidu JSON 荣誉数据
            import re
            joined = "".join(str(h) for h in honors)
            # 匹配: 标题","list":["年份"... 或 标题","mark_desc":"描述"...
            entries = re.split(r'\},\{|\},\s*\{', joined)
            shown = set()
            for entry in entries:
                # 提取标题 (第一个中文/英文名称)
                title_m = re.match(r'"?([^"]+)"', entry)
                title = title_m.group(1) if title_m else ""
                # 去重
                if not title or title in shown:
                    continue
                shown.add(title)

                # 提取年份列表
                years = []
                year_m = re.search(r'"list"\s*:\s*\[(.*?)\]', entry)
                if year_m:
                    years = re.findall(r'"(\d{4})"', year_m.group(1))

                # 提取描述
                desc = ""
                desc_m = re.search(r'"mark_desc"\s*:\s*"([^"]*)"', entry)
                if desc_m:
                    desc = desc_m.group(1)

                # 构建显示文本
                parts = [f"🏆 {title}"]
                if years:
                    parts.append(f"({'、'.join(years)})")
                if desc:
                    parts.append(f"— {desc}")

                st.markdown(f'<div style="background:{THEME["card_bg"]};border-radius:8px;padding:10px 16px;margin:6px 0;border-left:3px solid {THEME["primary"]};">{" ".join(parts)}</div>', unsafe_allow_html=True)
        else:
            st.info("暂无历史荣誉数据")

    st.divider()

    # === Elo 分析 ===
    st.subheader("📈 Elo 趋势分析")
    elo_history = store.get_elo_history(team.id)
    if elo_history:
        df = pd.DataFrame(elo_history); df["updated_at"] = pd.to_datetime(df["updated_at"])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["updated_at"], y=df["new_elo"],
            mode="lines+markers", line=dict(color=THEME["primary"],width=2),
            marker=dict(size=6,color=THEME["primary"]), name="Elo"))
        fig.update_layout(template="plotly_dark",paper_bgcolor=THEME["bg_dark"],
            plot_bgcolor=THEME["card_bg"],font=dict(color=THEME["text_secondary"]),
            xaxis=dict(gridcolor=THEME["border"]),yaxis=dict(gridcolor=THEME["border"],title="Elo"),
            margin=dict(l=0,r=0,t=10,b=0),height=300,hovermode="x")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无 Elo 历史数据 (比赛尚未开始)")

    st.subheader(f"🏟️ 组 {team.group} 实力对比")
    group_teams = store.get_teams_by_group(team.group)
    if group_teams:
        sorted_teams = sorted(group_teams, key=lambda t: t.elo_rating, reverse=True)
        colors = [THEME["primary"] if t.name_cn == team.name_cn else THEME["text_secondary"] for t in sorted_teams]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=[t.name_cn for t in sorted_teams], y=[t.elo_rating for t in sorted_teams],
            marker_color=colors, text=[f"{t.elo_rating:.0f}" for t in sorted_teams],
            textposition="outside", textfont=dict(color=THEME["text_primary"])))
        fig2.update_layout(template="plotly_dark",paper_bgcolor=THEME["bg_dark"],
            plot_bgcolor=THEME["card_bg"],font=dict(color=THEME["text_secondary"]),
            xaxis=dict(gridcolor=THEME["border"]),yaxis=dict(gridcolor=THEME["border"],title="Elo"),
            margin=dict(l=0,r=0,t=10,b=0),height=300,showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    footer()
