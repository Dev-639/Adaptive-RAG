"""
Home page for Streamlit application interface.
"""

import logging
import uuid
import streamlit as st

try:
    from streamlit_app.utils.api_client import get_python_base_url
except ModuleNotFoundError:
    from utils.api_client import get_python_base_url

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
    filemode="a",
)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Adaptive RAG Assistant", layout="centered")

st.title("🤖 Adaptive RAG Assistant")
st.write("An intelligent Question-Answering assistant powered by LangChain and LangGraph.")

# Initialize session ID if not set
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())

if "username" not in st.session_state:
    st.session_state["username"] = "Guest User"

st.markdown("---")

st.subheader("Start Conversation")

session_input = st.text_input(
    "Session ID (optional)",
    value=st.session_state["session_id"],
    help="You can customize your session ID to resume past chat history."
)

username_input = st.text_input(
    "Your Name",
    value=st.session_state["username"]
)

if st.button("🚀 Launch Chat Interface", use_container_width=True):
    st.session_state["session_id"] = session_input.strip() or str(uuid.uuid4())
    st.session_state["username"] = username_input.strip() or "Guest User"
    st.switch_page("pages/chat.py")

with st.expander("⚙️ Backend Configuration"):
    python_url = get_python_base_url()
    st.code(f"PYTHON_BASE_URL: {python_url}")
    st.caption("To change the backend server URL on Streamlit Cloud, set `PYTHON_BASE_URL` in app Secrets.")
