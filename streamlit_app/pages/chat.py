import uuid
import streamlit as st

import sys
import os

# Ensure project root is on path for src.* imports
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

try:
    from utils.api_client import query_backend, document_upload_rag
except ImportError:
    from streamlit_app.utils.api_client import query_backend, document_upload_rag

# Configure page settings
st.set_page_config(
    page_title="Adaptive RAG Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ensure session_id is active
if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid.uuid4())[:8]

# Header
col1, col2 = st.columns([10, 2])
with col1:
    st.title("💬 Adaptive RAG Assistant")
with col2:
    st.write("")
    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("home.py")

# Document upload section in sidebar
with st.sidebar:
    st.header("📂 Upload Documents")

    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

    file_description = None
    if uploaded_file:
        file_description = st.text_input(
            "📄 Describe your document (required)",
            max_chars=300,
            placeholder="E.g. LangGraph tutorial with workflows and code examples"
        )

        if "uploaded_files" not in st.session_state:
            st.session_state.uploaded_files = {}

        file_key = f"{uploaded_file.name}_{file_description}"

        if file_description:
            if file_key not in st.session_state.uploaded_files:
                # Upload file if not already uploaded
                with st.spinner("Processing & Indexing Document..."):
                    success = document_upload_rag(uploaded_file, file_description)
                if success:
                    st.success(f"Uploaded & Indexed: {uploaded_file.name}")
                    st.session_state.uploaded_files[file_key] = True
                else:
                    st.error(f"Document Upload Failed: {uploaded_file.name}")
            else:
                st.info(f"Indexed: {uploaded_file.name}")
        else:
            st.warning("Please describe your document before uploading.")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display existing chat history
for role, text in st.session_state.chat_history:
    st.chat_message(role).write(text)

# User input
user_input = st.chat_input("Ask any question...")

# Process user input and get response
if user_input:
    st.session_state.chat_history.append(("user", user_input))
    st.chat_message("user").write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = query_backend(user_input, st.session_state["session_id"])
            st.write(response)

    st.session_state.chat_history.append(("assistant", response))
    st.rerun()
