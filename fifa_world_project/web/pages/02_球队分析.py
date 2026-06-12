"""Team Analysis Page"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from web.theme import inject_theme
from web.auth import require_auth
from web.components import team_selector, footer
from config import DB_PATH

inject_theme()
from data.store import Store
from data.seed_data import seed_all
from engine.predictor import Predictor

# Initialize shared session state
if "store" not in st.session_state:
    store = Store(DB_PATH)
    store.init_db()
    if store.is_empty():
        seed_all(store)
    st.session_state.store = store
if "predictor" not in st.session_state:
    st.session_state.predictor = Predictor(seed=42)


def show():
    require_auth()

    with st.sidebar:
        st.markdown(f"<span style='color:#8892B0;font-size:0.85rem;'>👤 {st.session_state.get('username','')}</span>", unsafe_allow_html=True)
        if st.button("🚪 退出登录", key="logout_btn_02"):
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.rerun()

    store = st.session_state.store
    teams = store.get_all_teams()

    if not teams:
        st.warning("暂无球队数据")
        return

    st.subheader("📊 球队深度分析")

    team = team_selector(teams)
    if not team:
        footer()
        return

    # Team info cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Elo 评分", f"{team.elo_rating:.0f}")
    with col2:
        st.metric("🏅 FIFA 排名", f"#{team.fifa_rank}")
    with col3:
        group_teams = store.get_teams_by_group(team.group)
        elo_ranks = sorted([t.elo_rating for t in group_teams], reverse=True)
        group_rank = elo_ranks.index(team.elo_rating) + 1
        st.metric("📊 小组内 Elo 排名", f"#{group_rank}/4")
    with col4:
        st.metric("🏟️ 小组", f"组 {team.group}")

    st.divider()

    # Elo history chart
    st.subheader("📈 Elo 变化趋势")
    history = store.get_elo_history(team.id)

    if history:
        df = pd.DataFrame(history)
        df["updated_at"] = pd.to_datetime(df["updated_at"])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["updated_at"], y=df["new_elo"],
            mode="lines+markers",
            line=dict(color="#0C4AD1", width=2),
            marker=dict(size=6, color="#0C4AD1"),
            name="Elo",
            hovertemplate="%{y:.0f}<extra></extra>",
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0A0E1A",
            plot_bgcolor="#131832",
            font=dict(color="#8892B0"),
            xaxis=dict(gridcolor="#1E2340", title=""),
            yaxis=dict(gridcolor="#1E2340", title="Elo 评分"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=300,
            hovermode="x",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("暂无 Elo 历史数据 (比赛尚未开始)")

    # Group comparison chart
    st.subheader(f"🏟️ 组 {team.group} 实力对比")
    group_teams = store.get_teams_by_group(team.group)

    if group_teams:
        sorted_teams = sorted(group_teams, key=lambda t: t.elo_rating, reverse=True)
        colors = ["#0C4AD1" if t.name_cn == team.name_cn else "#8892B0" for t in sorted_teams]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=[t.name_cn for t in sorted_teams],
            y=[t.elo_rating for t in sorted_teams],
            marker_color=colors,
            text=[f"{t.elo_rating:.0f}" for t in sorted_teams],
            textposition="outside",
            textfont=dict(color="#FFFFFF"),
        ))
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0A0E1A",
            plot_bgcolor="#131832",
            font=dict(color="#8892B0"),
            xaxis=dict(gridcolor="#1E2340", title=""),
            yaxis=dict(gridcolor="#1E2340", title="Elo 评分"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=300,
            showlegend=False,
        )
        st.plotly_chart(fig2, use_container_width=True)

    footer()


show()
