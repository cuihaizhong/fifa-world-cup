"""Team Detail Page — 百度体育数据 + Elo 分析"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from config import THEME
from web.components import team_selector, footer
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

    # Build options list (same order as team_selector for index matching)
    from data.seed_data import FLAG_MAP as _FM
    options = [f"{_FM.get(t.fifa_code, '')} {t.name_cn} ({t.fifa_code})" for t in teams]
    # Pre-select the URL team if available
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
            team = selected
            st.rerun()

    if not team:
        st.info("👈 请从上方选择一支球队，或从首页轮播点击进入")
        footer()
        return

    flag = FLAG_MAP.get(team.fifa_code, "")

    # === HEADER ===
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown(f'<div style="font-size: 5rem; text-align: center; line-height: 1;">{flag}</div>', unsafe_allow_html=True)
    with col2:
        st.title(team.name_cn)
        st.markdown(f'<p style="color: {THEME["text_secondary"]}; font-size: 1rem;">{team.name} · FIFA #{team.fifa_rank} · Elo {team.elo_rating:.0f}</p>', unsafe_allow_html=True)

    st.divider()

    # === BAIDU SPORTS DATA ===
    baidu_data = scraper.get_team_data(team.fifa_code)

    if baidu_data:
        st.subheader("📡 百度体育数据")

        # Rankings
        cols = st.columns(4)
        with cols[0]:
            st.metric("🌍 世界排名", f"#{baidu_data.get('world_rank', '?')}")
        with cols[1]:
            asia = baidu_data.get('asian_rank')
            if asia:
                st.metric("🏯 亚洲排名", f"#{asia}")

        # Match schedule from Baidu
        matches = baidu_data.get("matches", [])
        if matches:
            st.subheader("📋 赛程 (百度体育)")
            for m in matches:
                status_color = "#10B981" if m["status"] == "进行中" else "#F59E0B" if "未开赛" in m.get("status", "") else "#6B7280"
                status_icon = "🟢" if m["status"] == "进行中" else "⚪" if "未开赛" in m.get("status", "") else "⏹"

                score_text = f"{m['home_score']} - {m['away_score']}" if m.get('home_score') not in (None, '-') else 'vs'
                st.markdown(f"""
                <div style="background:{THEME['card_bg']}; border-radius:8px; padding:10px 16px; margin:6px 0; display:flex; align-items:center; justify-content:space-between;">
                    <div>
                        <span style="color:{THEME['text_secondary']}; font-size:0.8rem;">{m['date']} {m['time']}</span>
                        <span style="color:{status_color}; font-size:0.75rem; margin-left:8px;">{status_icon} {m['status']}</span>
                    </div>
                    <div style="font-weight:600;">
                        {m['home']} <span style="color:{THEME['primary']};">{score_text}</span> {m['away']}
                    </div>
                    <div style="color:{THEME['text_secondary']}; font-size:0.8rem;">{m['stage']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("暂无赛程数据")

        # Link to Baidu
        url = scraper.get_team_url(team.fifa_code)
        if url:
            st.caption(f"[在百度体育查看 →]({url})")
    else:
        st.info(f"📡 百度体育暂未收录 {team.name_cn} 的数据。仅显示 Elo 分析。")

    st.divider()

    # === ELO ANALYSIS ===
    st.subheader("📈 Elo 分析")

    history = store.get_elo_history(team.id)
    if history:
        df = pd.DataFrame(history)
        df["updated_at"] = pd.to_datetime(df["updated_at"])
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["updated_at"], y=df["new_elo"],
            mode="lines+markers",
            line=dict(color=THEME["primary"], width=2),
            marker=dict(size=6, color=THEME["primary"]),
            name="Elo",
        ))
        fig.update_layout(
            template="plotly_dark", paper_bgcolor=THEME["bg_dark"],
            plot_bgcolor=THEME["card_bg"], font=dict(color=THEME["text_secondary"]),
            xaxis=dict(gridcolor=THEME["border"], title=""),
            yaxis=dict(gridcolor=THEME["border"], title="Elo 评分"),
            margin=dict(l=0, r=0, t=10, b=0), height=300, hovermode="x",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无 Elo 历史数据 (比赛尚未开始)")

    # Group comparison
    st.subheader(f"🏟️ 组 {team.group} 实力对比")
    group_teams = store.get_teams_by_group(team.group)
    if group_teams:
        sorted_teams = sorted(group_teams, key=lambda t: t.elo_rating, reverse=True)
        colors = [THEME["primary"] if t.name_cn == team.name_cn else THEME["text_secondary"] for t in sorted_teams]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=[t.name_cn for t in sorted_teams],
            y=[t.elo_rating for t in sorted_teams],
            marker_color=colors,
            text=[f"{t.elo_rating:.0f}" for t in sorted_teams],
            textposition="outside",
            textfont=dict(color=THEME["text_primary"]),
        ))
        fig2.update_layout(
            template="plotly_dark", paper_bgcolor=THEME["bg_dark"],
            plot_bgcolor=THEME["card_bg"], font=dict(color=THEME["text_secondary"]),
            xaxis=dict(gridcolor=THEME["border"], title=""),
            yaxis=dict(gridcolor=THEME["border"], title="Elo 评分"),
            margin=dict(l=0, r=0, t=10, b=0), height=300, showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    footer()


show()
