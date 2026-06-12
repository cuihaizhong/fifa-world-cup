"""2026 World Cup Prediction — Streamlit main entry"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import date, datetime

from config import DB_PATH
from web.theme import inject_theme
from web.auth import require_auth, do_logout
from data.store import Store
from data.seed_data import seed_all, FLAG_MAP
from engine.predictor import Predictor


def render_home():
    """首页：标题 + 国旗轮播 (纯CSS，无iframe)"""
    store = st.session_state.store
    all_teams = [t for t in store.get_all_teams() if t.id != 0]

    # 保留 auth 参数在链接中，防止刷新丢登录
    u_param = st.session_state.get("username", "")

    # 构建轮播 chip
    chips = []
    for t in all_teams:
        flag = FLAG_MAP.get(t.fifa_code, "")
        href = f"/?team={t.fifa_code}&u={u_param}" if u_param else f"/?team={t.fifa_code}"
        chips.append(
            f'<a href="{href}" target="_self" class="team-chip">'
            f'<span class="team-chip-flag">{flag}</span>'
            f'<span class="team-chip-name">{t.name_cn}</span>'
            f'</a>'
        )
    track_html = "".join(chips) + "".join(chips)

    st.markdown(f"""
    <div class="home-center">
        <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 4px;">🏆 2026 世界杯预测中心</h1>
        <p style="color: #8892B0; font-size: 0.9rem; margin-bottom: 24px;">基于 Elo 评分 + 泊松分布的数学预测模型 · 数据驱动 · 仅供参考</p>
        <div class="team-carousel-wrapper"><div class="team-carousel-track">{track_html}</div></div>
    </div>
    """, unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="2026 世界杯预测",
        page_icon="🏆",
        layout="wide",
        initial_sidebar_state="auto",
    )

    inject_theme()

    # Init database
    if "store" not in st.session_state:
        store = Store(DB_PATH)
        store.init_db()
        if store.is_empty():
            seed_all(store)
        st.session_state.store = store

    # Init predictor
    if "predictor" not in st.session_state:
        st.session_state.predictor = Predictor(seed=42)

    # === Auth gate ===
    require_auth()

    # Sidebar
    with st.sidebar:
        # 用户信息 + 退出
        st.markdown(f"""
        <div style="padding: 8px 0 16px 0;">
            <span style="color: #8892B0; font-size: 0.85rem;">👤 当前用户</span><br>
            <span style="color: #0C4AD1; font-weight: 600; font-size: 1rem;">{st.session_state.get('username', '')}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 退出登录", use_container_width=True, key="logout_btn"):
            do_logout()

        st.divider()

        st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1 style="font-size: 2.5rem; margin: 0;">🏆</h1>
            <h2 style="font-size: 1.2rem; margin: 8px 0; color: #0C4AD1;">2026 世界杯预测</h2>
            <p style="font-size: 0.75rem; color: #8892B0;">加拿大 · 墨西哥 · 美国</p>
        </div>
        """, unsafe_allow_html=True)

        store = st.session_state.store
        team_count = len(store.get_all_teams())
        match_count = len(store.get_all_matches())
        upcoming = len(store.get_upcoming_matches())

        st.markdown(f"""
        <div style="font-size: 0.8rem; color: #8892B0; line-height: 1.8;">
            📊 球队: <b style="color: #fff;">{team_count}</b> 支<br>
            📅 比赛: <b style="color: #fff;">{match_count}</b> 场<br>
            ⏳ 待赛: <b style="color: #0C4AD1;">{upcoming}</b> 场
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown(f'<div style="font-size: 0.7rem; color: #8892B0;">🕐 数据更新: {datetime.now().strftime("%m/%d %H:%M")}<br>📡 API 状态: 离线模式</div>', unsafe_allow_html=True)

    # 球队详情请求 (session_state 优先，query param 兜底)
    team_code = None

    # 方式1: selectbox 触发 (session_state)
    raw = st.session_state.get("selected_team")
    if raw and isinstance(raw, str):
        team_code = raw
        st.session_state["selected_team"] = None

    # 方式2: 轮播链接 (query param)
    if not team_code and "team" in st.query_params:
        val = st.query_params["team"]
        if val and isinstance(val, str) and len(val) == 3:
            team_code = val

    if team_code:
        from web.detail_view import show_team_detail
        store = st.session_state.store
        code = team_code.upper()
        team = store.get_team_by_code(code)
        if team:
            show_team_detail(team)
        else:
            st.warning(f"未找到球队: {team_code}")
            render_home()
    else:
        render_home()


if __name__ == "__main__":
    main()
