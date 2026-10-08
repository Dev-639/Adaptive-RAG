"""
Home page for Streamlit authentication interface.
"""

import logging
import streamlit as st

try:
    from streamlit_app.utils.api_client import create_user, login_user, get_api_token, get_rust_base_url
except ModuleNotFoundError:
    from utils.api_client import create_user, login_user, get_api_token, get_rust_base_url

# Hide sidebar for cleaner look
hide_sidebar_style = """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a",
)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="LangGraph Chat - Login")

st.title("🔐 Welcome to LangGraph Assistant")

# Step 1: Fetch API token or set default fallback session
if "session_id" not in st.session_state:
    token = get_api_token()
    if token:
        st.session_state["session_id"] = token
        st.success("API token initialized.")
    else:
        st.session_state["session_id"] = "default-session"
        st.info("Auth service is offline or unreachable at default host. Continuing with default session.")

# Step 2: Option to bypass directly to chat
col_direct, col_auth = st.columns([1, 1])
with col_direct:
    if st.button("🚀 Proceed to Chat Directly", use_container_width=True):
        st.session_state["username"] = "Guest"
        st.switch_page("pages/chat.py")

st.markdown("---")

# Step 3: Render login/signup form
with st.form("auth_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    mode = st.radio("Choose action:", ["Login", "Create Account"])
    submit = st.form_submit_button("Submit")

# Step 4: Handle login/account creation
if submit:
    if not username or not password:
        st.error("Username and password required.")
    else:
        if mode == "Create Account":
            success = create_user(username, password, st.session_state["session_id"])
            if success:
                st.success("User created. Please log in.")
            else:
                st.error("User creation failed. Verify that your backend service is running.")
        else:
            response = login_user(username, password, st.session_state["session_id"])
            if response and response.get("jwt"):
                st.session_state["jwt_token"] = response["jwt"]
                st.session_state["username"] = username
                st.switch_page("pages/chat.py")
            else:
                st.error("Login failed. Could not authenticate with backend service.")

# Debug logs section
with st.expander("📜 Debug Logs"):
    try:
        with open("app.log", "r") as log_file:
            st.text(log_file.read())
    except FileNotFoundError:
        st.warning("Log file not found yet.")
