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

    /* === 顶部工具栏：深色适配，不隐藏 === */
    [data-testid="stHeader"] {{
        background-color: {THEME['bg_dark']};
    }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    .stDeployButton {{ display: none !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}

    /* === 侧边栏基础样式 === */
    section[data-testid="stSidebar"] {{
        background-color: {THEME['card_bg']};
        border-right: 1px solid {THEME['border']};
    }}
    [data-testid="stSidebar"] * {{
        color: {THEME['text_primary']};
    }}
    /* 侧边栏导航字体加大 */
    [data-testid="stSidebar"] a {{
        font-size: 1.05rem !important;
        font-weight: 500 !important;
    }}
    [data-testid="stSidebar"] p {{
        font-size: 0.95rem !important;
    }}

    /* === 桌面端(≥769px)：侧边栏固定300px常开，不可收起 === */
    @media (min-width: 769px) {{
        section[data-testid="stSidebar"] {{
            width: 300px !important;
            min-width: 300px !important;
            max-width: 300px !important;
            transform: none !important;
            transition: none !important;
        }}
        [data-testid="stSidebarCollapseButton"] {{
            display: none !important;
        }}
        [data-testid="collapsedControl"] {{
            display: none !important;
        }}
    }}

    /* 登录页：隐藏侧边栏 */
    .login-page section[data-testid="stSidebar"] {{
        display: none !important;
        width: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
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

    /* === DataFrame / 表格 === */
    .stDataFrame, [data-testid="stTable"], .stTable {{
        background: {THEME['card_bg']} !important;
    }}
    .stDataFrame * {{ color: {THEME['text_primary']} !important; }}
    [data-testid="stTable"] table, .stTable table {{
        background: {THEME['card_bg']} !important;
    }}
    [data-testid="stTable"] th, .stTable th {{
        background: {THEME['bg_dark']} !important;
        color: {THEME['text_primary']} !important;
        border-color: {THEME['border']} !important;
    }}
    [data-testid="stTable"] td, .stTable td {{
        background: {THEME['card_bg']} !important;
        color: {THEME['text_secondary']} !important;
        border-color: {THEME['border']} !important;
    }}
    [data-testid="stTable"] tr:nth-child(even) td, .stTable tr:nth-child(even) td {{
        background: #161c3a !important;
    }}
    /* DataFrame 内部全量覆盖 */
    [data-testid="stDataFrame"] div[role="grid"] {{
        background: {THEME['card_bg']} !important;
    }}
    [data-testid="stDataFrame"] [data-testid="stDataFrameResizable"] {{
        background: {THEME['card_bg']} !important;
    }}

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

    /* ================================================================
       手机端 & 平板适配
       ================================================================ */

    /* ---------- 平板竖屏 / 小屏笔记本 (≤1024px) ---------- */
    @media (max-width: 1024px) {{
        /* 列基本堆叠，但 4 列可保留 2 列 */
        [data-testid="column"] {{
            flex: 1 1 50% !important;
            min-width: 280px;
        }}

        .block-container, .stMainBlockContainer, .main {{
            padding: 0.8rem 1rem !important;
        }}
    }}

    /* ---------- 手机横屏 / 小平板 (≤768px) ---------- */
    @media (max-width: 768px) {{
        html {{ font-size: 15px; }}
        body {{ font-size: 0.95rem; }}

        /* ---- 标题 ---- */
        h1 {{ font-size: 1.5rem !important; }}
        h2 {{ font-size: 1.2rem !important; }}
        h3 {{ font-size: 1rem !important; }}

        /* 侧边栏手机端允许收起(不阻止transform/transition，让Streamlit动画正常工作) */
        section[data-testid="stSidebar"] {{
            width: auto !important;
            min-width: auto !important;
            max-width: 280px !important;
        }}
        /* 收起/展开按钮手机端可见 */
        [data-testid="stSidebarCollapseButton"] {{
            display: flex !important;
        }}
        [data-testid="collapsedControl"] {{
            display: flex !important;
        }}

        /* ---- 内容区 ---- */
        .block-container, .stMainBlockContainer, .main {{
            padding: 0.4rem 0.6rem !important;
        }}

        /* ---- 列全部竖向堆叠 ---- */
        [data-testid="column"] {{
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }}
        /* 列之间减小间距 */
        [data-testid="column"] + [data-testid="column"] {{
            margin-top: 0.5rem;
        }}

        /* ---- 首页 ---- */
        .home-center {{
            min-height: 60vh; padding: 0 4px;
        }}
        .home-center h1 {{
            font-size: 1.4rem !important;
        }}

        /* ---- 轮播 ---- */
        .team-carousel-wrapper {{
            padding: 8px 0; margin: 10px 0;
        }}
        .team-carousel-track {{ gap: 8px; }}
        .team-chip {{
            padding: 10px 14px; min-width: 80px; border-radius: 12px; gap: 4px;
            border-width: 1.5px;
        }}
        .team-chip-flag {{ font-size: 2rem; }}
        .team-chip-name {{ font-size: 0.85rem; }}

        /* ---- 卡片 ---- */
        .match-card {{
            padding: 12px 10px; margin: 8px 0;
        }}
        .match-card [style*="flex: 1"] {{
            font-size: 0.9rem !important;
        }}
        .stat-card {{
            padding: 12px 6px; margin-bottom: 6px;
        }}
        .stat-value {{ font-size: 1.4rem; }}

        /* ---- 进度条 ---- */
        .progress-container {{ height: 6px; margin: 8px 0 6px 0; }}

        /* ---- 按钮：全宽 + 大触控区 ---- */
        .stButton > button {{
            width: 100% !important;
            min-height: 44px; font-size: 1rem; border-radius: 10px;
        }}

        /* ---- 下拉框 ---- */
        .stSelectbox [role="combobox"] {{
            font-size: 0.95rem; min-height: 40px;
        }}

        /* ---- 表格 / DataFrame ---- */
        .stDataFrame, [data-testid="stTable"], .stTable {{
            overflow-x: auto; -webkit-overflow-scrolling: touch;
        }}
        [data-testid="stTable"] th, .stTable th {{
            font-size: 0.8rem; padding: 6px 8px;
        }}
        [data-testid="stTable"] td, .stTable td {{
            font-size: 0.78rem; padding: 5px 8px;
        }}

        /* ---- Metric ---- */
        [data-testid="stMetricValue"] {{
            font-size: 1.3rem !important;
        }}

        /* ---- Tab 标签：可横向滚动 ---- */
        [data-testid="stTabs"] {{
            overflow-x: auto; -webkit-overflow-scrolling: touch;
            flex-wrap: nowrap;
        }}
        button[data-baseweb="tab"] {{
            font-size: 0.85rem; padding: 6px 12px; white-space: nowrap;
            flex-shrink: 0;
        }}

        /* ---- 展开器 ---- */
        .streamlit-expanderHeader {{
            font-size: 0.9rem; padding: 10px 12px;
        }}

        /* ---- 详情页 Header (国旗+队名+链接) ---- */
        /* 第一个 column 国旗缩小 */
        .stColumn:first-child [style*="font-size:5rem"] {{
            font-size: 3rem !important;
        }}

        /* ---- 分割线 ---- */
        hr {{ margin: 12px 0; }}

        /* ---- 页脚 ---- */
        .footer {{
            font-size: 0.7rem; padding: 12px 0; margin-top: 20px;
        }}

        /* ---- 详情页赛程卡片：竖向排列 ---- */
        .detail-match-row {{
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 6px; padding: 10px 12px !important;
        }}
        .detail-match-date {{
            min-width: auto !important;
            display: flex; gap: 8px; align-items: baseline;
        }}
        .detail-match-teams {{
            text-align: left !important; font-size: 0.9rem;
        }}
        .detail-match-info {{
            min-width: auto !important; text-align: left !important;
            display: flex; gap: 12px;
        }}
    }}

    /* ---------- 小屏手机 (≤480px) ---------- */
    @media (max-width: 480px) {{
        html {{ font-size: 14px; }}
        body {{ font-size: 0.9rem; }}

        h1 {{ font-size: 1.3rem !important; }}

        /* ---- 首页标题缩小 ---- */
        .home-center h1 {{
            font-size: 1.2rem !important;
        }}

        /* ---- 轮播 ---- */
        .team-carousel-track {{ gap: 5px; }}
        .team-chip {{
            padding: 8px 10px; min-width: 64px; border-radius: 10px; gap: 2px;
        }}
        .team-chip-flag {{ font-size: 1.5rem; }}
        .team-chip-name {{ font-size: 0.7rem; }}

        /* ---- 首页高度 ---- */
        .home-center {{ min-height: 45vh; }}

        /* ---- 卡片 ---- */
        .match-card {{ padding: 10px 8px; }}
        .stat-card {{ padding: 10px 4px; }}

        /* ---- 按钮 ---- */
        .stButton > button {{
            min-height: 42px; font-size: 0.95rem;
        }}

        /* ---- Metric ---- */
        [data-testid="stMetricValue"] {{
            font-size: 1.1rem !important;
        }}
        [data-testid="stMetricLabel"] {{
            font-size: 0.7rem !important;
        }}

        /* ---- Tab 标签 ---- */
        button[data-baseweb="tab"] {{
            font-size: 0.78rem; padding: 5px 10px;
        }}

        /* ---- 详情国旗 ---- */
        .stColumn:first-child [style*="font-size:5rem"] {{
            font-size: 2.5rem !important;
        }}

        /* ---- 侧边栏：允许收起 ---- */
        section[data-testid="stSidebar"] {{
            width: auto !important;
            min-width: auto !important;
            max-width: 240px !important;
        }}
        [data-testid="stSidebarCollapseButton"] {{
            display: flex !important;
        }}
        [data-testid="collapsedControl"] {{
            display: flex !important;
        }}

        /* ---- 内容区 ---- */
        .block-container, .stMainBlockContainer, .main {{
            padding: 0.3rem 0.5rem !important;
        }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(css, unsafe_allow_html=True)
