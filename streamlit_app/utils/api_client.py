"""
API client for communicating with the Python FastAPI backend service.
"""

import logging
import os
import requests

logger = logging.getLogger(__name__)


def get_python_base_url() -> str:
    """Get the Python backend base URL from environment or Streamlit secrets."""
    url = os.getenv("PYTHON_BASE_URL")
    if not url:
        try:
            import streamlit as st
            if hasattr(st, "secrets") and "PYTHON_BASE_URL" in st.secrets:
                url = st.secrets["PYTHON_BASE_URL"]
        except Exception:
            pass
    return url or "http://127.0.0.1:8000"


def query_backend(query: str, session_id: str) -> str:
    """
    Send a query to the RAG backend.

    Args:
        query: The user's query text.
        session_id: Session identifier for tracking conversation.

    Returns:
        Response text from the backend or error message.
    """
    python_url = get_python_base_url()
    url = f"{python_url}/rag/query"

    try:
        response = requests.post(
            url,
            json={"query": query, "session_id": session_id},
            allow_redirects=False,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()["result"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.RequestException as e:
        logger.error("Query backend failed: %s", e)
        return f"Error connecting to backend service at {python_url}: {str(e)}"


def document_upload_rag(file, description: str) -> bool:
    """
    Upload a document to the RAG system.

    Args:
        file: File object to upload.
        description: Description of the document.

    Returns:
        True if upload succeeds, False otherwise.
    """
    python_url = get_python_base_url()
    headers = {
        "X-Description": description
    }
    url = f"{python_url}/rag/documents/upload"

    if file:
        try:
            files = {"file": (file.name, file, file.type)}
            response = requests.post(url, files=files, headers=headers, timeout=60)

            if response.status_code == 200:
                return True
        except requests.RequestException as e:
            logger.error("Document upload failed: %s", e)

    return False
