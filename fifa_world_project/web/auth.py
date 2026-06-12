"""Authentication module for 2026 World Cup Prediction App"""
import streamlit as st

# 内置账号
ACCOUNTS = {
    "cuihaizhong": "527928chz",
    "zhaosiqi": "527928zsq",
}


def init_auth():
    """Initialize auth-related session state"""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None


def show_login():
    """Display centered login form"""
    # 留白
    for _ in range(3):
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 28px;">
            <h1 style="font-size: 4.5rem; margin: 0;">🏆</h1>
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
