"""Dark sports theme CSS injection"""
import streamlit as st
from config import THEME


def inject_theme():
    """Inject custom dark theme into Streamlit"""
    css = f"""
    <style>
    .stApp {{
        background-color: {THEME['bg_dark']};
        color: {THEME['text_primary']};
    }}
    .stMainBlockContainer {{
        padding-top: 1rem;
    }}
    [data-testid="stSidebar"] {{
        background-color: {THEME['card_bg']};
        border-right: 1px solid {THEME['border']};
    }}
    h1, h2, h3 {{
        color: {THEME['text_primary']} !important;
    }}
    h1 {{
        font-size: 2rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }}
    .match-card {{
        background: linear-gradient(135deg, {THEME['card_bg']}, #0F1428);
        border-left: 4px solid {THEME['primary']};
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        transition: all 0.2s ease;
    }}
    .match-card:hover {{
        border-left-color: #3B82F6;
        box-shadow: 0 4px 20px rgba(12, 74, 209, 0.15);
        transform: translateX(2px);
    }}
    .stat-card {{
        background: {THEME['card_bg']};
        border-radius: 12px;
        padding: 20px 16px;
        text-align: center;
        border: 1px solid {THEME['border']};
    }}
    .stat-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {THEME['primary']};
        line-height: 1.2;
    }}
    .stat-label {{
        font-size: 0.85rem;
        color: {THEME['text_secondary']};
        margin-top: 4px;
    }}
    .progress-container {{
        display: flex;
        height: 8px;
        border-radius: 4px;
        overflow: hidden;
        background: #1E2340;
        margin: 12px 0 8px 0;
    }}
    .progress-win {{ background: {THEME['win']}; transition: width 0.3s ease; }}
    .progress-draw {{ background: {THEME['draw']}; transition: width 0.3s ease; }}
    .progress-lose {{ background: {THEME['lose']}; transition: width 0.3s ease; }}
    .pct-label {{
        display: flex;
        justify-content: space-between;
        font-size: 0.85rem;
        color: {THEME['text_secondary']};
    }}
    .pct-label .win {{ color: {THEME['win']}; font-weight: 600; }}
    .pct-label .draw {{ color: {THEME['draw']}; font-weight: 600; }}
    .pct-label .lose {{ color: {THEME['lose']}; font-weight: 600; }}
    .score-prediction {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {THEME['primary']};
        text-align: center;
        margin-top: 8px;
    }}
    .confidence-tag {{
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }}
    .confidence-high {{ background: rgba(16, 185, 129, 0.15); color: {THEME['win']}; }}
    .confidence-mid {{ background: rgba(245, 158, 11, 0.15); color: {THEME['draw']}; }}
    .confidence-low {{ background: rgba(239, 68, 68, 0.15); color: {THEME['lose']}; }}
    .stButton > button {{
        background: {THEME['primary']} !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
    }}
    .stButton > button:hover {{
        background: #3B82F6 !important;
        box-shadow: 0 4px 12px rgba(12, 74, 209, 0.3) !important;
    }}
    .footer {{
        text-align: center;
        color: {THEME['text_secondary']};
        font-size: 0.8rem;
        padding: 20px 0;
        border-top: 1px solid {THEME['border']};
        margin-top: 40px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
