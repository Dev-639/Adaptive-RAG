import uuid
import sys
import os

import streamlit as st

# Ensure project root is on path for src.* imports
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

st.set_page_config(page_title="Adaptive RAG - Assistant", page_icon="🤖", layout="wide")

st.title("🤖 Welcome to Adaptive RAG Assistant")
st.markdown("""
Adaptive RAG is an agentic AI system that dynamically routes your questions to:
- **Vector Documents**: Answers questions from your uploaded PDFs and TXT files.
- **General LLM**: Provides general knowledge answers.
- **Web Search**: Conducts real-time web searches using Tavily when required.
""")

# Initialize session_id
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())[:8]

st.success(f"Session Active (ID: {st.session_state['session_id']})")

if st.button("💬 Open Chat Assistant", type="primary", use_container_width=True):
    st.switch_page("pages/chat.py")
