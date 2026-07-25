"""
Direct RAG client - calls RAG functions directly instead of via HTTP.
Used for Streamlit Cloud deployment where no separate FastAPI server is available.
"""

import sys
import os
import io
import tempfile

# Ensure the project root is on sys.path so `src.*` imports work
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Force UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Load environment / config before any LangChain imports
from src.core.config import settings  # noqa: E402

from langchain_core.messages import HumanMessage, AIMessage  # noqa: E402
from src.memory.chathistory_in_memory import ChatInMemoryHistory  # noqa: E402
from src.rag.graph_builder import builder  # noqa: E402
from src.rag.document_upload import documents as _upload_documents  # noqa: E402


def query_backend(query: str, session_id: str) -> str:
    """
    Invoke the RAG graph directly (no HTTP).

    Args:
        query: The user's question.
        session_id: Unique session identifier.

    Returns:
        The assistant's response text, or an error message.
    """
    try:
        chat_history = ChatInMemoryHistory.get_session_history(session_id)
        chat_history.add_message(HumanMessage(content=query))

        messages = chat_history.messages
        result = builder.invoke({"messages": messages})
        output_text = result["messages"][-1].content

        chat_history.add_message(AIMessage(content=output_text))
        return output_text
    except Exception as e:
        return f"Error: {e}"


def document_upload_rag(file, description: str) -> bool:
    """
    Process and index a document directly (no HTTP).

    Args:
        file: Streamlit UploadedFile object.
        description: User-provided document description.

    Returns:
        True if upload and indexing succeeded, False otherwise.
    """
    try:
        from fastapi import UploadFile as FastAPIUploadFile

        # Wrap the Streamlit UploadedFile in a FastAPI-compatible UploadFile
        file.seek(0)
        file_bytes = file.read()
        file.seek(0)

        upload_file = FastAPIUploadFile(
            filename=file.name,
            file=io.BytesIO(file_bytes),
        )

        result = _upload_documents(description, upload_file)
        return bool(result)
    except Exception as e:
        print(f"Document upload error: {e}")
        return False
