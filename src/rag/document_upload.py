"""
Document upload and processing module.
"""

import os
import tempfile

from fastapi import UploadFile, File
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.retriever_setup import retriever_chain
from src.tools.common_tools import enhance_description_with_llm


def documents(description: str, file: UploadFile = File(...)):
    """
    Process and upload a document for RAG.

    Validates file type, loads content, enhances description, chunks documents,
    and stores them in the vector database.

    Args:
        description: User-provided document description.
        file: The uploaded file (PDF or TXT).

    Returns:
        Boolean indicating success of the upload process.

    Raises:
        HTTPException: If file type is not supported or loading fails.
    """
    filename = file.filename
    print(filename)
    if not filename.endswith(".pdf") and not filename.endswith(".txt"):
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported"
        )

    file_bytes = file.file.read()

    ext = os.path.splitext(filename)[1]
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    tmp_path = tmp_file.name
    tmp_file.write(file_bytes)
    tmp_file.close()  # Close file handle so PyPDFLoader can open it on Windows

    try:
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(tmp_path)
        else:
            loader = TextLoader(tmp_path, encoding="utf-8")

        docs = loader.load()
    except Exception as e:
        from fastapi import HTTPException
        print(f"Document upload error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error loading file: {e}"
        )
    finally:
        if os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    # Enhance description using LLM
    description_llm = enhance_description_with_llm(description)

    # Save enhanced description
    with open("description.txt", "w", encoding="utf-8") as f:
        f.write(description_llm)

    with open("description.txt", "r", encoding="utf-8") as f:
        desc_preview = f.read()
        print(f"Document description saved successfully (length: {len(desc_preview)} chars)")

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(docs)

    return retriever_chain(chunks)




