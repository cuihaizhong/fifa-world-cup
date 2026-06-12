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
    html {{ font-size: 16px; }}
    body {{ font-size: 1rem; }}
    .stApp {{
        background-color: {THEME['bg_dark']};
    }}

    /* === 隐藏默认工具栏 === */
    [data-testid="stHeader"] {{ display: none !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    .stDeployButton {{ display: none !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}

    /* === 侧边栏：始终展开，隐藏收放按钮 === */
    [data-testid="stSidebar"] {{
        background-color: {THEME['card_bg']};
        border-right: 1px solid {THEME['border']};
    }}
    [data-testid="stSidebar"] * {{
        color: {THEME['text_primary']};
    }}
    /* 隐藏侧边栏收放按钮 (小箭头) */
    [data-testid="stSidebarCollapseButton"] {{ display: none !important; }}
    [data-testid="collapsedControl"] {{ display: none !important; }}
    /* 侧边栏导航字体加大 */
    [data-testid="stSidebar"] a {{
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }}
    [data-testid="stSidebar"] p {{
        font-size: 0.95rem !important;
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
        display: flex; gap: 20px; width: max-content;
        animation: carousel-scroll 80s linear infinite;
    }}
    .team-carousel-track:hover {{ animation-play-state: paused; }}
    @keyframes carousel-scroll {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-50%); }}
    }}
    .team-chip {{
        display: flex; flex-direction: column; align-items: center; gap: 8px;
        padding: 20px 28px; background: {THEME['card_bg']};
        border-radius: 16px; border: 2px solid {THEME['border']};
        text-decoration: none !important; min-width: 144px; transition: all 0.2s ease;
    }}
    .team-chip:hover {{
        border-color: {THEME['primary']}; background: #1a2045;
        transform: translateY(-2px); box-shadow: 0 4px 12px rgba(12,74,209,0.2);
    }}
    .team-chip-flag {{ font-size: 4rem; line-height: 1; }}
    .team-chip-name {{ color: {THEME['text_primary']}; font-size: 1.5rem; font-weight: 500; }}

    /* 首页居中 */
    .home-center {{
        display: flex; flex-direction: column; justify-content: center;
        align-items: center; min-height: 80vh; text-align: center;
    }}

    /* 页脚 */
    .footer {{
        text-align: center; color: {THEME['text_secondary']}; font-size: 0.8rem;
        padding: 20px 0; border-top: 1px solid {THEME['border']}; margin-top: 40px;
    }}

    /* ========== 手机端适配 ========== */
    @media (max-width: 768px) {{
        html {{ font-size: 14px; }}
        h1 {{ font-size: 1.5rem !important; }}
        h2 {{ font-size: 1.2rem !important; }}

        /* 侧边栏在手机上允许收起 */
        [data-testid="stSidebarCollapseButton"] {{ display: flex !important; }}
        [data-testid="collapsedControl"] {{ display: flex !important; }}

        /* 轮播缩小 */
        .team-chip {{
            padding: 10px 14px; min-width: 80px; border-radius: 10px; gap: 4px;
        }}
        .team-chip-flag {{ font-size: 2rem; }}
        .team-chip-name {{ font-size: 0.85rem; }}
        .team-carousel-track {{ gap: 10px; }}

        /* 首页居中 */
        .home-center {{ min-height: 50vh; padding: 0 8px; }}

        /* 卡片 */
        .match-card {{ padding: 12px; }}
        .stat-card {{ padding: 12px 8px; }}
        .stat-value {{ font-size: 1.4rem; }}

        /* 内容区 */
        .block-container, .stMainBlockContainer, .main {{
            padding: 0.5rem 0.8rem !important;
        }}

        /* 按钮加大触控区 */
        .stButton > button {{
            min-height: 44px; font-size: 1rem;
        }}

        /* 表格横向滚动 */
        .stDataFrame {{ overflow-x: auto; }}

        /* 列竖向堆叠 */
        [data-testid="column"] {{
            flex: 1 1 100% !important;
        }}
    }}

    @media (max-width: 480px) {{
        html {{ font-size: 13px; }}
        .team-chip {{
            padding: 8px 10px; min-width: 64px; gap: 2px;
        }}
        .team-chip-flag {{ font-size: 1.5rem; }}
        .team-chip-name {{ font-size: 0.7rem; }}
        .team-carousel-track {{ gap: 6px; }}
        .home-center {{ min-height: 40vh; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
