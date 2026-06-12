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
    /* 隐藏 Streamlit 默认顶部工具栏(白色横条) */
    header[data-testid="stHeader"] {{
        display: none !important;
    }}
    [data-testid="stToolbar"] {{
        display: none !important;
    }}
    /* === Streamlit 原生组件 === */
    .stSelectbox label, .stDateInput label, .stTextInput label {{
        color: {THEME['text_secondary']} !important;
        font-size: 0.85rem !important;
    }}
    .stSelectbox [data-baseweb="select"], .stDateInput input {{
        background-color: {THEME['card_bg']} !important;
        color: {THEME['text_primary']} !important;
        border-color: {THEME['border']} !important;
    }}
    /* Metric 组件 */
    [data-testid="stMetricValue"] {{
        color: {THEME['text_primary']} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {THEME['text_secondary']} !important;
    }}
    /* DataFrame 表格 */
    [data-testid="stDataFrame"] {{
        background-color: {THEME['card_bg']} !important;
        color: {THEME['text_primary']} !important;
    }}
    [data-testid="stDataFrame"] th {{
        color: {THEME['text_secondary']} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stDataFrame"] td {{
        color: {THEME['text_primary']} !important;
    }}
    /* 展开器 Expander */
    .streamlit-expanderHeader {{
        color: {THEME['text_primary']} !important;
        background: {THEME['card_bg']} !important;
        border-radius: 8px !important;
    }}
    .streamlit-expanderContent {{
        background: {THEME['card_bg']} !important;
        color: {THEME['text_primary']} !important;
    }}
    /* Info/Warning/Success boxes */
    .stAlert {{
        background-color: {THEME['card_bg']} !important;
        color: {THEME['text_primary']} !important;
        border-color: {THEME['border']} !important;
    }}
    /* 分割线 */
    hr, .stDivider {{
        border-color: {THEME['border']} !important;
    }}
    /* Caption 和 small 文字 */
    .stCaption, small, .small {{
        color: {THEME['text_secondary']} !important;
    }}
    /* Tab 标签 */
    button[data-baseweb="tab"] {{
        color: {THEME['text_secondary']} !important;
        background: transparent !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {THEME['primary']} !important;
        border-bottom-color: {THEME['primary']} !important;
    }}
    .stDeployButton {{
        display: none !important;
    }}
    /* 主区域背景全覆盖，消除白色空白 */
    section[data-testid="stSidebar"] + div {{
        background-color: {THEME['bg_dark']} !important;
    }}
    .main {{
        background-color: {THEME['bg_dark']};
    }}
    .block-container {{
        padding-top: 2rem;
        background-color: {THEME['bg_dark']};
    }}
    .stMainBlockContainer {{
        padding-top: 1rem;
    }}
    /* 主菜单和页脚 */
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
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
    /* === 球队轮播 === */
    .team-carousel-wrapper {{
        overflow: hidden;
        padding: 12px 0;
        margin: 16px 0;
        -webkit-mask-image: linear-gradient(90deg, transparent, #000 3%, #000 97%, transparent);
        mask-image: linear-gradient(90deg, transparent, #000 3%, #000 97%, transparent);
    }}
    .team-carousel-track {{
        display: flex;
        gap: 10px;
        width: max-content;
        animation: carousel-scroll 80s linear infinite;
    }}
    .team-carousel-track:hover {{
        animation-play-state: paused;
    }}
    @keyframes carousel-scroll {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-50%); }}
    }}
    .team-chip {{
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        padding: 10px 14px;
        background: {THEME['card_bg']};
        border-radius: 12px;
        border: 1px solid {THEME['border']};
        text-decoration: none !important;
        min-width: 72px;
        transition: all 0.2s ease;
        cursor: pointer;
    }}
    .team-chip:hover {{
        border-color: {THEME['primary']};
        background: #1a2045;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(12, 74, 209, 0.2);
    }}
    .team-chip-flag {{
        font-size: 2rem;
        line-height: 1;
    }}
    .team-chip-name {{
        color: {THEME['text_secondary']};
        font-size: 0.72rem;
        font-weight: 500;
        white-space: nowrap;
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
