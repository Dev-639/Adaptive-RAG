"""
API client for communicating with backend services.
"""

import logging
import os
import requests

logger = logging.getLogger(__name__)


def get_rust_base_url() -> str:
    """Get the Rust backend base URL from environment or Streamlit secrets."""
    url = os.getenv("RUST_BASE_URL")
    if not url:
        try:
            import streamlit as st
            if hasattr(st, "secrets") and "RUST_BASE_URL" in st.secrets:
                url = st.secrets["RUST_BASE_URL"]
        except Exception:
            pass
    return url or "http://localhost:8080/api"


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


def create_user(username: str, password: str, api_token: str) -> bool:
    """
    Create a new user account.

    Args:
        username: Username for the new account.
        password: Password for the new account.
        api_token: API token for authentication.

    Returns:
        True if user creation succeeds, False otherwise.
    """
    rust_url = get_rust_base_url()
    headers = {
        "X-API-TOKEN": api_token,
        "Content-Type": "application/json"
    }
    logger.info("API Token received: %s", api_token)

    try:
        response = requests.post(
            f"{rust_url}/create_user",
            json={"username": username, "password": password},
            headers=headers,
            timeout=10
        )

        logger.info("Calling /create_user, status code: %s", response.status_code)

        if response.status_code == 200:
            try:
                logger.debug("Create user response: %s", response.json())
            except ValueError:
                logger.warning("Create user returned non-JSON response")
            return True
        else:
            logger.error(
                "Create user failed: %s - %s",
                response.status_code,
                response.text
            )
            return False

    except requests.RequestException as e:
        logger.exception("Request to /create_user failed: %s", e)
        return False


def login_user(username: str, password: str, api_token: str) -> dict:
    """
    Authenticate user login.

    Args:
        username: Username to log in.
        password: Password for the user.
        api_token: API token for authentication.

    Returns:
        Response dictionary with JWT token if successful, None otherwise.
    """
    rust_url = get_rust_base_url()
    headers = {
        "X-API-TOKEN": api_token,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            f"{rust_url}/login",
            json={"username": username, "password": password},
            headers=headers,
            timeout=10
        )
        logger.info("Calling /login, status code: %s", response.status_code)

        if response.status_code == 200:
            return response.json()
    except requests.RequestException as e:
        logger.error("Request to /login failed: %s", e)

    return None


def get_api_token() -> str:
    """
    Get an API token for authentication.

    Returns:
        API token string if successful, None otherwise.
    """
    rust_url = get_rust_base_url()
    try:
        response = requests.post(f"{rust_url}/init", timeout=5)
        logger.info("Calling /init, status code: %s", response.status_code)

        if response.status_code == 200:
            return response.json().get("api_token")
    except requests.RequestException as e:
        logger.warning("Connection to auth service at %s failed: %s", rust_url, e)

    return None


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
    print(f"[query_backend] Calling: {url}")

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
        return f"Error connecting to RAG backend service at {python_url}: {str(e)}"


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
            print(response)

            if response.status_code == 200:
                return True
        except requests.RequestException as e:
            logger.error("Document upload failed: %s", e)

    return False
