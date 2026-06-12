"""Authentication module for 2026 World Cup Prediction App"""
import base64
import streamlit as st
from pathlib import Path

# 内置账号
ACCOUNTS = {
    "cuihaizhong": "527928chz",
    "zhaosiqi": "527928zsq",
}

# 背景图片 base64 编码 (延迟加载)
_bg_base64: str | None = None


def _get_bg_base64() -> str:
    """Load and cache background image as base64"""
    global _bg_base64
    if _bg_base64 is None:
        image_path = Path(__file__).parent.parent / "image" / "3.jpg"
        if image_path.exists():
            with open(image_path, "rb") as f:
                _bg_base64 = base64.b64encode(f.read()).decode()
        else:
            _bg_base64 = ""
    return _bg_base64


def init_auth():
    """Initialize auth-related session state"""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None


def show_login():
    """Display centered login form with full-screen background image, no sidebar"""
    bg_b64 = _get_bg_base64()

    st.markdown(f"""
    <style>
    /* 隐藏侧边栏 */
    [data-testid="stSidebar"] {{ display: none !important; }}
    [data-testid="stSidebarCollapsedControl"] {{ display: none !important; }}

    /* 背景图 — 固定全屏 */
    .login-bg-img {{
        position: fixed;
        top: 0; left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        z-index: 0;
        opacity: 0.35;
        pointer-events: none;
    }}

    /* 内容在最上层 */
    .login-content {{
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
    }}

    /* 重置 Streamlit 容器背景 */
    .stApp {{ background: #0A0E1A !important; }}
    .stMainBlockContainer {{ background: transparent !important; }}
    .block-container {{ max-width: 100% !important; }}
    </style>

    <!-- 全屏背景图 -->
    <img class="login-bg-img" src="data:image/jpeg;base64,{bg_b64}" />

    <!-- 登录内容 -->
    <div class="login-content">
    """, unsafe_allow_html=True)

    # 登录卡片
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="
            background: rgba(19, 24, 50, 0.94);
            border: 1px solid rgba(42, 48, 80, 0.6);
            border-radius: 16px;
            padding: 40px 32px;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        ">
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align: center; margin-bottom: 24px;">
            <h1 style="font-size: 4rem; margin: 0;">🏆</h1>
            <h2 style="color: #0C4AD1; font-weight: 700; margin: 8px 0;">2026 世界杯预测</h2>
            <p style="color: #8892B0; font-size: 0.9rem; margin: 0;">请登录以查看赛事预测数据</p>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("👤 用户名", key="login_user", placeholder="请输入用户名")
        password = st.text_input("🔒 密码", type="password", key="login_pass", placeholder="请输入密码")

        if st.button("登 录", type="primary", use_container_width=True):
            if not username:
                st.error("请输入用户名")
            elif not password:
                st.error("请输入密码")
            elif username in ACCOUNTS and ACCOUNTS[username] == password:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.rerun()
            else:
                st.error("❌ 用户名或密码错误")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


def show_logout_button():
    """Display logout button and user info in sidebar"""
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 8px 0;">
            <span style="color: #8892B0; font-size: 0.85rem;">👤 当前用户</span><br>
            <span style="color: #0C4AD1; font-weight: 600; font-size: 1rem;">{st.session_state.get('username', '')}</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 退出登录", use_container_width=True, key="logout_btn"):
            st.session_state["authenticated"] = False
            st.session_state["username"] = None
            st.rerun()


def require_auth():
    """
    Require authentication before showing content.
    Stops execution and shows login if not authenticated.
    """
    init_auth()

    if not st.session_state.get("authenticated"):
        show_login()
        st.stop()

    return True
