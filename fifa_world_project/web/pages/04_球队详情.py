"""Team Detail Page — 百度体育全量数据 + Elo 分析"""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from config import THEME
from web.components import footer
from data.store import Store
from data.seed_data import FLAG_MAP, seed_all
from engine.predictor import Predictor
from data.team_scraper import BaiduTeamScraper

# Initialize shared state
if "store" not in st.session_state:
    store = Store()
    store.init_db()
    if store.is_empty():
        seed_all(store)
    st.session_state.store = store
if "predictor" not in st.session_state:
    st.session_state.predictor = Predictor(seed=42)


def render_match_row(m: dict):
    """渲染一场比赛的行"""
    home = m.get("home", "")
    away = m.get("away", "")
    hs = m.get("home_score", "-")
    aws = m.get("away_score", "-")
    status = m.get("status", "")
    stage = m.get("stage", "")

    # Status styling
    if "进行中" in status:
        icon, color = "🟢", "#10B981"
    elif "未开赛" in status:
        icon, color = "⚪", "#F59E0B"
    else:
        icon, color = "⏹", "#6B7280"

    score = f"{hs} - {aws}" if hs not in (None, "-", "") and aws not in (None, "-", "") else "vs"

    st.markdown(f"""
    <div style="background:{THEME['card_bg']}; border-radius:8px; padding:8px 14px; margin:4px 0;
                display:flex; align-items:center; justify-content:space-between; font-size:0.9rem;">
        <div style="color:{THEME['text_secondary']}; min-width:140px;">
            {m.get('date', '')} {m.get('time', '')}
        </div>
        <div style="font-weight:600; flex:1; text-align:center;">
            {home} <span style="color:{THEME['primary']};">{score}</span> {away}
        </div>
        <div style="display:flex; align-items:center; gap:6px; min-width:160px; justify-content:flex-end;">
            <span style="color:{THEME['text_secondary']}; font-size:0.8rem;">{stage}</span>
            <span style="color:{color}; font-size:0.75rem;">{icon} {status}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_squad_table(players: list):
    """渲染球员大名单表格"""
    if not players:
        st.caption("暂无数据")
        return
    rows = []
    for p in players:
        rows.append({
            "号码": p.get("number", ""),
            "姓名": p.get("name", ""),
            "俱乐部": p.get("club", ""),
            "出场": p.get("apps", ""),
            "进球": p.get("goals", ""),
        })
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True,
                 column_config={"号码": st.column_config.TextColumn(width="small"),
                               "姓名": st.column_config.TextColumn(width="medium"),
                               "俱乐部": st.column_config.TextColumn(width="medium"),
                               "出场": st.column_config.TextColumn(width="small"),
                               "进球": st.column_config.TextColumn(width="small")})


def show():
    store = st.session_state.store
    teams = store.get_all_teams()
    scraper = BaiduTeamScraper()

    # Determine team from query params or selector
    params = st.query_params
    team_code = params.get("team", None)
    team = None
    if team_code:
        team = store.get_team_by_code(team_code.upper())

    # Team selector
    options = [f"{FLAG_MAP.get(t.fifa_code, '')} {t.name_cn} ({t.fifa_code})" for t in teams]
    if team:
        try:
            idx = next(i for i, t in enumerate(teams) if t.fifa_code == team.fifa_code)
        except StopIteration:
            idx = 0
    else:
        idx = 0

    selected_label = st.selectbox("选择球队", options, index=idx, key="detail_team_select")
    if selected_label:
        selected = teams[options.index(selected_label)]
        if not team or selected.fifa_code != team.fifa_code:
            st.query_params["team"] = selected.fifa_code
            st.rerun()

    if not team:
        st.info("👈 请从上方选择一支球队，或从首页轮播点击进入")
        footer()
        return

    flag = FLAG_MAP.get(team.fifa_code, "")
    baidu_data = scraper.get_team_data(team.fifa_code) or {}
    baidu_url = scraper.get_team_url(team.fifa_code)

    # === HEADER ===
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.markdown(f'<div style="font-size:5rem;text-align:center;line-height:1;">{flag}</div>', unsafe_allow_html=True)
    with col2:
        st.title(team.name_cn)
        rank_info = f"FIFA #{team.fifa_rank} · Elo {team.elo_rating:.0f}"
        if baidu_data.get("world_rank"):
            rank_info += f" · 百度世界排名 #{baidu_data['world_rank']}"
        st.markdown(f'<p style="color:{THEME["text_secondary"]};font-size:1rem;">{team.name} · {rank_info}</p>', unsafe_allow_html=True)
    with col3:
        if baidu_url:
            st.markdown(f'<a href="{baidu_url}" target="_blank" style="display:inline-block;margin-top:20px;padding:6px 16px;background:{THEME["primary"]};color:#fff;border-radius:8px;text-decoration:none;font-size:0.85rem;">🔗 百度体育</a>', unsafe_allow_html=True)

    st.divider()

    # === TABBED BAIDU DATA ===
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 赛程", "👥 阵容", "📊 资料", "🏅 历史成绩", "📈 Elo分析"])

    # --- TAB 1: 赛程 ---
    with tab1:
        matches = baidu_data.get("matches", [])
        schedule_raw = baidu_data.get("schedule_raw", "")
        if matches:
            for m in matches:
                render_match_row(m)
        elif schedule_raw:
            st.text(schedule_raw[:2000])
        else:
            st.info("暂无赛程数据")
            # Show matches from our database for this team
            all_matches = store.get_all_matches()
            team_matches = [m for m in all_matches
                          if m.home_team and m.away_team
                          and m.home_team.fifa_code == team.fifa_code
                          or (m.away_team and m.away_team.fifa_code == team.fifa_code)]
            if team_matches:
                st.caption("以下为本系统赛程数据：")
                for m in team_matches:
                    st.markdown(f"""
                    <div style="background:{THEME['card_bg']};border-radius:8px;padding:8px 14px;margin:4px 0;
                                display:flex;align-items:center;justify-content:space-between;font-size:0.9rem;">
                        <span style="color:{THEME['text_secondary']};">{m.date.strftime('%m/%d %H:%M')}</span>
                        <span style="font-weight:600;">{m.home_team.name_cn} vs {m.away_team.name_cn}</span>
                        <span style="color:{THEME['text_secondary']};font-size:0.8rem;">{m.stage.value} · {m.venue}</span>
                    </div>
                    """, unsafe_allow_html=True)

    # --- TAB 2: 阵容 ---
    with tab2:
        squad = baidu_data.get("squad", {})
        coaches = squad.get("coaches", []) if isinstance(squad, dict) else []

        if coaches:
            st.subheader("🧑‍🏫 教练组")
            coach_cols = st.columns(min(len(coaches), 4))
            for i, c in enumerate(coaches):
                with coach_cols[i % 4]:
                    st.markdown(f"""
                    <div style="background:{THEME['card_bg']};border-radius:8px;padding:10px;text-align:center;margin:4px 0;">
                        <div style="font-weight:600;font-size:0.9rem;">{c.get('name', '')}</div>
                        <div style="color:{THEME['text_secondary']};font-size:0.75rem;">{c.get('info', '')}</div>
                    </div>
                    """, unsafe_allow_html=True)

        players_by_pos = squad.get("players", {}) if isinstance(squad, dict) else {}
        if players_by_pos:
            for pos, players in players_by_pos.items():
                st.subheader(f"⚽ {pos}")
                render_squad_table(players)
        elif not coaches:
            st.info("暂无阵容数据")

    # --- TAB 3: 资料 ---
    with tab3:
        info = baidu_data.get("info", {})
        if info:
            rank_cols = st.columns(4)
            rank_keys = [("世界排名", "🌍"), ("欧洲排名", "🏰"), ("亚洲排名", "🏯"),
                        ("非洲排名", "🦁"), ("南美排名", "🦅"), ("中北美排名", "🌎")]
            col_idx = 0
            for key, icon in rank_keys:
                if key in info:
                    with rank_cols[col_idx % 4]:
                        st.metric(f"{icon} {key}", f"#{info[key]}")
                    col_idx += 1
            if col_idx == 0:
                st.info("暂无排名数据")
        else:
            st.info("暂无详细资料")

        # Our database info
        st.divider()
        st.caption("本系统数据：")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("🎯 Elo 评分", f"{team.elo_rating:.0f}")
        with c2:
            st.metric("🏅 FIFA 排名", f"#{team.fifa_rank}")
        with c3:
            st.metric("🏟️ 小组", f"组 {team.group}")

    # --- TAB 4: 历史成绩 ---
    with tab4:
        history_data = baidu_data.get("history", {})
        history_raw = history_data.get("raw", "") if isinstance(history_data, dict) else ""
        if history_raw:
            st.text(history_raw[:2000])
        else:
            st.info("暂无历史成绩数据")

    # --- TAB 5: Elo分析 ---
    with tab5:
        elo_history = store.get_elo_history(team.id)
        if elo_history:
            df = pd.DataFrame(elo_history)
            df["updated_at"] = pd.to_datetime(df["updated_at"])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df["updated_at"], y=df["new_elo"],
                mode="lines+markers", line=dict(color=THEME["primary"], width=2),
                marker=dict(size=6, color=THEME["primary"]), name="Elo"))
            fig.update_layout(template="plotly_dark", paper_bgcolor=THEME["bg_dark"],
                plot_bgcolor=THEME["card_bg"], font=dict(color=THEME["text_secondary"]),
                xaxis=dict(gridcolor=THEME["border"], title=""),
                yaxis=dict(gridcolor=THEME["border"], title="Elo 评分"),
                margin=dict(l=0, r=0, t=10, b=0), height=300, hovermode="x")
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
            fig2.update_layout(template="plotly_dark", paper_bgcolor=THEME["bg_dark"],
                plot_bgcolor=THEME["card_bg"], font=dict(color=THEME["text_secondary"]),
                xaxis=dict(gridcolor=THEME["border"], title=""),
                yaxis=dict(gridcolor=THEME["border"], title="Elo 评分"),
                margin=dict(l=0, r=0, t=10, b=0), height=300, showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

    footer()


show()
