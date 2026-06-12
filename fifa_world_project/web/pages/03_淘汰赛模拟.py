"""Knockout Simulation Page"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from collections import Counter
from web.theme import inject_theme
from web.components import footer
from engine.elo import EloEngine

inject_theme()
from config import DB_PATH
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


def simulate_knockout_match(team_a, team_b, elo: EloEngine, rng: np.random.RandomState):
    """Simulate one knockout match, return winner"""
    if team_a is None:
        return team_b
    if team_b is None:
        return team_a

    elo_a = elo.get_effective_elo(team_a.elo_rating, is_home=False)
    elo_b = elo.get_effective_elo(team_b.elo_rating, is_home=False)
    expected_a = elo.expected_win_rate(elo_a, elo_b)

    return team_a if rng.random() < expected_a else team_b


def run_tournament_simulation(teams, elo, rng, n_sims=1000):
    """Run full tournament simulation N times, return win counts"""
    win_counts = Counter()

    for _ in range(n_sims):
        shuffled = teams.copy()
        rng.shuffle(shuffled)
        round_teams = shuffled

        while len(round_teams) > 1:
            next_round = []
            for i in range(0, len(round_teams), 2):
                winner = simulate_knockout_match(
                    round_teams[i],
                    round_teams[i + 1] if i + 1 < len(round_teams) else None,
                    elo, rng
                )
                next_round.append(winner)
            round_teams = next_round

        if round_teams:
            win_counts[round_teams[0].name_cn] += 1

    return win_counts


def show():
    store = st.session_state.store

    st.subheader("🏆 淘汰赛模拟器")
    st.markdown("""
    <p style="color: #8892B0; font-size: 0.85rem; margin-bottom: 20px;">
        基于当前 Elo 评分，模拟淘汰赛 1000 次，统计各球队夺冠概率。<br>
        小组赛结束后，将使用实际对阵表替换随机抽签。
    </p>
    """, unsafe_allow_html=True)

    all_teams = store.get_all_teams()

    if not all_teams:
        st.warning("暂无球队数据")
        return

    # Filter out TBD placeholder (id=0) and take top 32 by Elo
    real_teams = [t for t in all_teams if t.id != 0]
    top32 = sorted(real_teams, key=lambda t: t.elo_rating, reverse=True)[:32]

    if st.button("🎲 一键模拟淘汰赛 (1000次)", type="primary", use_container_width=True):
        with st.spinner("正在进行 1000 次淘汰赛模拟..."):
            elo = EloEngine()
            rng = np.random.RandomState(42)
            win_counts = run_tournament_simulation(top32, elo, rng, n_sims=1000)

        st.subheader("👑 夺冠概率 TOP 20")

        df = pd.DataFrame([
            {"球队": team, "夺冠概率%": round(count / 10, 1)}
            for team, count in win_counts.most_common(20)
        ])

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df["球队"][::-1],
            x=df["夺冠概率%"][::-1],
            orientation="h",
            marker=dict(
                color=df["夺冠概率%"][::-1],
                colorscale=[[0, "#EF4444"], [0.5, "#F59E0B"], [1, "#10B981"]],
                showscale=False,
            ),
            text=[f"{v}%" for v in df["夺冠概率%"][::-1]],
            textposition="outside",
            textfont=dict(color="#FFFFFF"),
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0A0E1A",
            plot_bgcolor="#131832",
            font=dict(color="#8892B0"),
            xaxis=dict(gridcolor="#1E2340", title="夺冠概率 (%)"),
            yaxis=dict(gridcolor="#1E2340", title=""),
            margin=dict(l=0, r=40, t=10, b=0),
            height=500,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

        # Top 16 probability cards
        st.subheader("📋 前 16 名球队晋级概率")
        cols = st.columns(5)
        for i, (team_name, win_count) in enumerate(win_counts.most_common(16)):
            with cols[i % 5]:
                st.markdown(f"""
                <div class="stat-card" style="padding: 12px; margin-bottom: 8px;">
                    <div style="font-weight: 600; font-size: 0.95rem;">{team_name}</div>
                    <div style="font-size: 1.5rem; color: #0C4AD1; margin: 4px 0;">{win_count / 10:.1f}%</div>
                    <div style="font-size: 0.7rem; color: #8892B0;">夺冠概率</div>
                </div>
                """, unsafe_allow_html=True)

        st.caption("💡 模拟基于前 32 Elo 排名球队随机对阵，共 1000 次迭代。")

    else:
        st.info("👆 点击上方按钮开始模拟")
        st.subheader("📊 当前 Elo TOP 10")

        top10 = top32[:10]
        df_top = pd.DataFrame([
            {"排名": i + 1, "球队": t.name_cn, "Elo": t.elo_rating, "FIFA排名": t.fifa_rank}
            for i, t in enumerate(top10)
        ])
        st.dataframe(df_top, hide_index=True, use_container_width=True)

    footer()


show()
