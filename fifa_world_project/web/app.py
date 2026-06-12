"""2026 World Cup Prediction — Streamlit main entry"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import streamlit.components.v1 as components
from datetime import date, datetime

from config import DB_PATH
from web.theme import inject_theme
from web.auth import require_auth, do_logout
from data.store import Store
from data.seed_data import seed_all, FLAG_MAP
from engine.predictor import Predictor


def render_home():
    """首页：轮播 + 赛事入口，上下居中。轮播用 component 避免页面跳转"""
    store = st.session_state.store
    all_teams = [t for t in store.get_all_teams() if t.id != 0]

    # 构建 chip HTML (两倍实现无缝循环)
    chips = []
    for t in all_teams:
        flag = FLAG_MAP.get(t.fifa_code, "")
        chips.append(
            f'<div class="team-chip" onclick="selectTeam(\'{t.fifa_code}\')">'
            f'<span class="team-chip-flag">{flag}</span>'
            f'<span class="team-chip-name">{t.name_cn}</span>'
            f'</div>'
        )
    track_html = "".join(chips) + "".join(chips)

    st.markdown("""
    <div class="home-center">
        <h1 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 4px;">🏆 2026 世界杯预测中心</h1>
        <p style="color: #8892B0; font-size: 0.9rem; margin-bottom: 24px;">基于 Elo 评分 + 泊松分布的数学预测模型 · 数据驱动 · 仅供参考</p>
    </div>
    """, unsafe_allow_html=True)

    # 轮播用自定义组件 (iframe)，点击通过 postMessage 传回，不触发页面重载
    selected = components.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: transparent; overflow: hidden; font-family: sans-serif; }}
    .team-carousel-wrapper {{
        overflow: hidden; padding: 12px 0; margin: 8px 0;
        mask-image: linear-gradient(90deg, transparent, #000 3%, #000 97%, transparent);
        -webkit-mask-image: linear-gradient(90deg, transparent, #000 3%, #000 97%, transparent);
    }}
    .team-carousel-track {{
        display: flex; gap: 20px; width: max-content;
        animation: scroll 80s linear infinite;
    }}
    .team-carousel-track:hover {{ animation-play-state: paused; }}
    @keyframes scroll {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-50%); }}
    }}
    .team-chip {{
        display: flex; flex-direction: column; align-items: center; gap: 8px;
        padding: 20px 28px; background: #131832;
        border-radius: 16px; border: 2px solid #2A3050;
        cursor: pointer; min-width: 144px; transition: all 0.2s ease;
    }}
    .team-chip:hover {{
        border-color: #0C4AD1; background: #1a2045;
        transform: translateY(-2px); box-shadow: 0 4px 12px rgba(12,74,209,0.2);
    }}
    .team-chip-flag {{ font-size: 4rem; line-height: 1; }}
    .team-chip-name {{ color: #fff; font-size: 1.5rem; font-weight: 500; }}
    </style>
    </head>
    <body>
    <div class="team-carousel-wrapper">
        <div class="team-carousel-track">{track_html}</div>
    </div>
    <script>
    function selectTeam(code) {{
        window.parent.postMessage({{
            isStreamlitMessage: true,
            type: 'streamlit:setComponentValue',
            value: code
        }}, '*');
    }}
    </script>
    </body>
    </html>
    """, height=200)

    # 处理球队选择 (用 _last 去重防止 component 旧值重复触发)
    if selected and selected != st.session_state.get("_last_carousel_sel"):
        st.session_state["_last_carousel_sel"] = selected
        st.session_state["selected_team"] = selected
        st.rerun()


def main():
    st.set_page_config(
        page_title="2026 世界杯预测",
        page_icon="🏆",
        layout="wide",
        initial_sidebar_state="expanded",
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

    # Sidebar (所有侧边栏内容合并在一起)
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

    # 检查球队详情请求 (session state 优先，query param 作后备)
    team_code = None

    # 从 session state (component 点击)
    if "selected_team" in st.session_state and st.session_state["selected_team"]:
        team_code = str(st.session_state["selected_team"])
        st.session_state["selected_team"] = None

    # 从 URL query param
    if not team_code and "team" in st.query_params:
        raw = st.query_params["team"]
        team_code = str(raw) if raw else None

    if team_code:
        from web.detail_view import show_team_detail
        store = st.session_state.store
        code = str(team_code).upper()
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
