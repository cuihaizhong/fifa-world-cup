"""Dark sports theme CSS injection"""
import streamlit as st
from config import THEME


def inject_theme():
    """Inject custom dark theme into Streamlit"""
    css = f"""
    <style>
    /* === 全局：所有文字默认白色 === */
    html, body, .stApp, .stMarkdown, .stMarkdown * {{
        color: {THEME['text_primary']};
    }}
    .stApp {{
        background-color: {THEME['bg_dark']};
    }}

    /* === 隐藏默认工具栏 === */
    header[data-testid="stHeader"] {{ display: none !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    .stDeployButton {{ display: none !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}

    /* === 侧边栏 === */
    [data-testid="stSidebar"] {{
        background-color: {THEME['card_bg']};
        border-right: 1px solid {THEME['border']};
    }}
    [data-testid="stSidebar"] * {{
        color: {THEME['text_primary']};
    }}

    /* === 主区域 === */
    .block-container, .stMainBlockContainer, .main {{
        background-color: {THEME['bg_dark']};
        padding-top: 1.5rem;
    }}

    /* === 标题 === */
    h1, h2, h3, h4 {{ color: {THEME['text_primary']} !important; }}
    h1 {{ font-size: 2rem !important; font-weight: 700 !important; }}

    /* === 表单组件 === */
    .stSelectbox label, .stDateInput label, .stTextInput label,
    [data-testid="stWidgetLabel"] {{
        color: {THEME['text_secondary']} !important;
    }}
    .stSelectbox [role="combobox"], .stDateInput input {{
        background: {THEME['card_bg']} !important;
        color: {THEME['text_primary']} !important;
        border-color: {THEME['border']} !important;
    }}

    /* === Metric === */
    [data-testid="stMetricValue"] {{ color: {THEME['text_primary']} !important; }}
    [data-testid="stMetricLabel"] {{ color: {THEME['text_secondary']} !important; }}

    /* === DataFrame === */
    .stDataFrame, [data-testid="stTable"] {{
        background: {THEME['card_bg']} !important;
    }}
    .stDataFrame * {{ color: {THEME['text_primary']} !important; }}

    /* === 按钮 === */
    .stButton > button {{
        background: {THEME['primary']} !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }}
    .stButton > button:hover {{
        background: #3B82F6 !important;
    }}

    /* === Alert / Info / Warning === */
    .stAlert {{ border-color: {THEME['border']} !important; }}
    .stAlert * {{ color: {THEME['text_primary']} !important; }}

    /* === 分割线 === */
    hr {{ border-color: {THEME['border']} !important; }}

    /* === Tab 标签 === */
    button[data-baseweb="tab"] {{ color: {THEME['text_secondary']} !important; }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: {THEME['primary']} !important;
        border-bottom-color: {THEME['primary']} !important;
    }}

    /* === 展开器 === */
    .streamlit-expanderHeader {{
        color: {THEME['text_primary']} !important;
        background: {THEME['card_bg']} !important;
    }}

    /* ========== 自定义组件 ========== */

    /* 比赛卡片 */
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

    /* 统计卡片 */
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

    /* 进度条 */
    .progress-container {{
        display: flex; height: 8px; border-radius: 4px;
        overflow: hidden; background: #1E2340; margin: 12px 0 8px 0;
    }}
    .progress-win {{ background: {THEME['win']}; }}
    .progress-draw {{ background: {THEME['draw']}; }}
    .progress-lose {{ background: {THEME['lose']}; }}

    /* 百分比标签 */
    .pct-label {{ display: flex; justify-content: space-between; font-size: 0.85rem; }}
    .pct-label .win {{ color: {THEME['win']}; font-weight: 600; }}
    .pct-label .draw {{ color: {THEME['draw']}; font-weight: 600; }}
    .pct-label .lose {{ color: {THEME['lose']}; font-weight: 600; }}

    /* 比分预测 */
    .score-prediction {{
        font-size: 1.1rem; font-weight: 600;
        color: {THEME['primary']}; text-align: center; margin-top: 8px;
    }}

    /* 置信度 */
    .confidence-tag {{ display: inline-block; padding: 2px 10px; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }}
    .confidence-high {{ background: rgba(16,185,129,0.2); color: {THEME['win']}; }}
    .confidence-mid {{ background: rgba(245,158,11,0.2); color: {THEME['draw']}; }}
    .confidence-low {{ background: rgba(239,68,68,0.2); color: {THEME['lose']}; }}

    /* 球队轮播 */
    .team-carousel-wrapper {{
        overflow: hidden; padding: 12px 0; margin: 16px 0;
        mask-image: linear-gradient(90deg, transparent, #000 3%, #000 97%, transparent);
    }}
    .team-carousel-track {{
        display: flex; gap: 10px; width: max-content;
        animation: carousel-scroll 80s linear infinite;
    }}
    .team-carousel-track:hover {{ animation-play-state: paused; }}
    @keyframes carousel-scroll {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-50%); }}
    }}
    .team-chip {{
        display: flex; flex-direction: column; align-items: center; gap: 4px;
        padding: 10px 14px; background: {THEME['card_bg']};
        border-radius: 12px; border: 1px solid {THEME['border']};
        text-decoration: none !important; min-width: 72px; transition: all 0.2s ease;
    }}
    .team-chip:hover {{
        border-color: {THEME['primary']}; background: #1a2045;
        transform: translateY(-2px); box-shadow: 0 4px 12px rgba(12,74,209,0.2);
    }}
    .team-chip-flag {{ font-size: 2rem; line-height: 1; }}
    .team-chip-name {{ color: {THEME['text_primary']}; font-size: 0.75rem; font-weight: 500; }}

    /* 页脚 */
    .footer {{
        text-align: center; color: {THEME['text_secondary']}; font-size: 0.8rem;
        padding: 20px 0; border-top: 1px solid {THEME['border']}; margin-top: 40px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
