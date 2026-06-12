"""Authentication module for 2026 World Cup Prediction App"""
import streamlit as st

# 内置账号
ACCOUNTS = {
    "cuihaizhong": "527928chz",
    "zhaosiqi": "527928zsq",
}


def init_auth():
    """Initialize auth state — 优先从 URL query param 恢复登录状态（防刷新丢失）"""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "username" not in st.session_state:
        st.session_state["username"] = None

    # 从 URL query param 恢复登录 (应对页面刷新)
    if not st.session_state["authenticated"] and "u" in st.query_params:
        saved_user = str(st.query_params["u"])
        if saved_user and saved_user in ACCOUNTS:
            st.session_state["authenticated"] = True
            st.session_state["username"] = saved_user


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
                # 写入 URL 参数防止刷新丢失登录
                st.query_params["u"] = username
                st.rerun()
            else:
                st.error("❌ 用户名或密码错误")


def do_logout():
    """Clear auth state and URL param"""
    st.session_state["authenticated"] = False
    st.session_state["username"] = None
    st.query_params.clear()
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
