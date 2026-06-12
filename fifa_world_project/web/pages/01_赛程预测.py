"""Schedule & Prediction Page"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
from datetime import date, timedelta, datetime
from web.theme import inject_theme
from web.auth import require_auth
from web.components import match_card, stat_cards, footer
from engine.predictor import Predictor
from config import DB_PATH

inject_theme()
from data.store import Store
from data.seed_data import seed_all

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

    # 侧边栏：用户 + 退出
    with st.sidebar:
        st.markdown(f"<span style='color:#8892B0;font-size:0.85rem;'>👤 {st.session_state.get('username','')}</span>", unsafe_allow_html=True)
        if st.button("🚪 退出登录", key="logout_btn_01"):
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.rerun()

    store = st.session_state.store
    predictor: Predictor = st.session_state.predictor

    # Date picker
    col1, col2 = st.columns([1, 2])
    with col1:
        selected_date = st.date_input(
            "📅 选择日期",
            value=date.today(),
            min_value=date(2026, 6, 11),
            max_value=date(2026, 7, 19),
        )

    # Stats
    all_matches = store.get_all_matches()
    today_matches = store.get_matches_by_date(selected_date)
    predicted = [m for m in all_matches if m.prediction is not None]

    stat_cards(
        today_count=len(today_matches),
        predicted_count=len(predicted),
        total_count=len(all_matches),
    )

    st.divider()

    if not today_matches:
        st.info(f"📭 {selected_date.strftime('%m月%d日')} 当天没有安排比赛")
        footer()
        return

    st.subheader(f"📋 {selected_date.strftime('%m月%d日')} 比赛 ({len(today_matches)} 场)")

    # Generate predictions for each match
    for match in today_matches:
        if match.home_team and match.away_team:
            if match.prediction is None:
                pred = predictor.predict(match.home_team, match.away_team, match)
                store.save_prediction(match.id, pred)
                match.prediction = pred
            match_card(match)

    footer()


show()
