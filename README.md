# Adaptive RAG System

An intelligent question-answering application that automatically determines the best source of information to answer user queries. The system intelligently chooses between stored internal documents, web search results, and general knowledge.

---

## Overview

The Adaptive RAG System improves retrieval-augmented generation by assessing user queries and selecting the most appropriate data source. If relevant internal documents are available, the system retrieves them to craft an answer. If internal documents do not contain sufficient information, the system performs a web search to provide an accurate response.

The application includes both a REST API built with FastAPI and an interactive web interface built with Streamlit.

---

## Key Features

* Dynamic Query Routing: Automatically directs questions to document search, web search, or direct response generation based on topic relevance.
* Document Indexing: Supports uploading and indexing text documents into a vector database for semantic search.
* Fact Verification: Evaluates retrieved information for relevance before presenting the final answer to the user.
* Session Management: Saves chat history and user interactions in a MongoDB database for continuous conversation tracking.
* Web Interface: Provides a user-friendly browser dashboard for uploading files and chatting with the system.
* REST API: Offers standard HTTP endpoints to integrate retrieval and generation capabilities into other applications.

---

## System Architecture

1. Query Intake: The user submits a question through the web interface or API.
2. Routing Logic: The system evaluates the query to identify if it relates to uploaded documents, general knowledge, or requires live web data.
3. Information Retrieval:
   * Document Route: Searches the vector database for matching text chunks.
   * Search Route: Queries web search APIs for up-to-date web information.
   * General Route: Formulates an answer directly using language model capabilities.
4. Response Generation and Grading: The language model produces an answer based on retrieved context, ensuring the answer directly addresses the user query.
5. Response Output: The formatted answer is returned to the user and saved to the chat history.

---

## Project Structure

* `src/api`: REST API endpoints and request handlers.
* `src/config`: Application settings and prompt configurations.
* `src/core`: Core configuration loaders and logging utilities.
* `src/db`: Database client connections for chat history storage.
* `src/llms`: Model integrations and helper functions.
* `src/memory`: Chat history tracking implementations.
* `src/models`: Data models and schema definitions.
* `src/rag`: Retrieval graph logic, node workflows, and document processing.
* `src/tools`: Search tools and external service connectors.
* `streamlit_app`: Streamlit user interface components and pages.

---

## Installation and Setup

### Prerequisites

* Python 3.10 or higher
* MongoDB instance (local or cloud)
* Qdrant database instance (or local vector database setup)
* OpenAI API Key
* Tavily API Key (for web search capabilities)

### Step 1: Clone Repository

```bash
git clone https://github.com/Dev-639/Adaptive-RAG.git
cd Adaptive-RAG
```

### Step 2: Virtual Environment Setup

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Create a `.env` file in the root directory with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
MONGODB_URI=your_mongodb_connection_string
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

---

## Running the Application

### Running the REST API Server

```bash
uvicorn src.main:app --reload --port 8000
```

The API documentation will be accessible at `http://localhost:8000/docs`.

### Running the Web Interface

```bash
streamlit run streamlit_app/home.py
```

The Streamlit web interface will open in your browser at `http://localhost:8501`.

---

## License

This project is open-source and available under the MIT License.

---

## Author

Dev
* GitHub: [Dev-639](https://github.com/Dev-639)
