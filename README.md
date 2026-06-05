# Capstone-Gen-AI-Agentic-AI-Project

## 🎯 Capstone Project Objective
The goal of this capstone project is to develop a Generative AI–powered application that enables users to query enterprise documents using autonomous AI agents. The system uses Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and Agentic AI frameworks to retrieve relevant information, reason over it, and generate accurate, context-aware responses.

### ✅ Completed Tasks Checklist
*   [x] **Task 1**: Initialized modular project architecture and self-validating Pydantic core settings.
*   [x] **Task 2**: Built an enterprise wide-viewport web application using the Streamlit dashboard layout.
*   [x] **Task 3**: Built an error-trapped format parser engine handling PDF, TXT, CSV, XLSX, JSON, and YAML formats.
*   [x] **Task 4**: Implemented overlapping chunk splitters (1000 block size / 150 overlap character windows).
*   [x] **Task 5**: Structured persistent on-disk database indexing using ChromaDB and Google's updated `gemini-embedding-001` model.
*   [x] **Task 6**: Developed high-recall vector cosine similarity search APIs (`k=3`).
*   [x] **Task 7**: Connected context prompts safely to Google's optimized `gemini-2.5-flash-lite` core LLM.
*   [x] **Task 8**: Structured sequential agent graphs using LangGraph (**Planner**, **Retriever**, **Reasoning**, **Validator**).
*   [x] **Task 9**: Added a **Max Retries Ceiling Limit (3 cycles)** and a **Fallback End Node** to stop infinite loops.
*   [x] **Task 10**: Containerized the workspace using an isolated Docker configuration and compiled a full report.

---

## 🚀 Key Technical Enhancements

*   **Cyclic Self-Correction Loop**: The Validator Agent automatically intercepts ungrounded outputs and loops the state back to the Retriever to pull fresh context snippets.
*   **Token Drainage Guardrails**: Enforces a strict 3-attempt ceiling counter on the validation loop. If an agent cannot verify its answer after 3 attempts, it routes to a fallback node to abort gracefully and save your API budget.
*   **Memory Optimization**: The Streamlit user interface uses a defensive sliding-window limit to prevent page performance lag over long chat sessions.
*   **Langfuse Live Telemetry**: Streamlit connects directly to the Langfuse Japan Cloud cluster via callback hooks...
*   **Free-Tier API Quota Throttling**: Implements a paced batch-ingestion loop inside the vector storage layer (5 chunks per batch with a 1.5-second cooldown) to balance Requests-Per-Minute (RPM) and avoid 429 Quota Exhaustion errors on large file parse streams.

---

## 📂 Project Tree Structure

```text
Capstone-Gen-AI-Agentic-AI-Project/
├── app/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   └── graph.py             # LangGraph workflows and retry ceiling limits
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py            # Pydantic environment configuration mappings
│   └── services/
│       ├── __init__.py
│       ├── ingestion.py         # Multi-format document parser engine
│       └── vector_store.py      # ChromaDB interface and Google embeddings
├── data/
│   └── chroma_db/               # On-disk persistent database storage directory
├── .dockerignore                # Container copy exclusion map
├── .env                         # Local runtime credentials (Secret)
├── .gitignore                   # Git exclusion manifest list
├── Dockerfile                   # Isolated production app containerization setup
├── DOCUMENTATION.md             # Detailed capstone final technical report
├── main.py                      # Streamlit application portal hub entry point
└── requirements.txt             # Conflict-free, frozen package dependencies
```

---

## 🛠️ Local Setup & Execution

### 1. Installation
Ensure you have **Python 3.11** or **Python 3.12** running. Activate your virtual environment and run the installation script:
```bash
source venv/Scripts/activate
python -m pip install --upgrade pip
pip install --force-reinstall -r requirements.txt
```

### 2. Run Sanity Environment Test
Before launching the UI, confirm your environment, Pydantic libraries, and Langfuse callback handlers are perfectly aligned:
```bash
# Verifies that Pydantic AppConfig loads your environment variables correctly:
python -c "from app.core.config import settings; print('Loaded API Key:', settings.GOOGLE_API_KEY[:8] + '...')"
```

### 3. Launch App Panel
```bash
streamlit run main.py
```

---

## 🐳 Docker Container Deployment

### 1. Verification & Initialization Guardrails
Before running any containerization steps, ensure that **Docker Desktop** is open and actively running on your host machine. Look for the solid green status bar indicator ("Engine Running") in the bottom corner of your Docker UI before proceeding.

### 2. Compile Image Layers
Compile your code and package manifests into an isolated image asset (ensure you include the trailing period):
```bash
docker build -t enterprise-agentic-rag-engine .
```

### 3. Launch the Active Production Container
Spin up the live runtime container instance, explicitly feeding your local secret keys map from your `.env` file:
```bash
docker run -d -p 8501:8501 --env-file .env --name rag-running-app enterprise-agentic-rag-engine
```
*Access the live application panel interface at: **http://localhost:8501***

### 4. Session Tear-Down & Resource Cleanup (Mandatory)
Once your evaluation session is complete, cleanly stop the server process and remove the ephemeral container layer to free up port `8501` for next use. This preserves your compiled image cache blueprint without leaving ghost processes running in memory:
```bash
# Gracefully halt the server engine
docker stop rag-running-app

# Cleanly remove the execution instance layer
docker rm rag-running-app
```

---

## 🤝 Project Submission Packaging

To bundle the finished, conflict-free project workspace into your final assignment package while completely skipping heavy local development caches and folder states, run this command in **Git Bash**:

```bash
zip -r Capstone-Gen-AI-Agentic-AI-Project.zip . -x "venv/*" "ENV/*" "data/chroma_db/*" ".git/*" "*/__pycache__/*" "__pycache__/*" ".DS_Store" "Thumbs.db"
```
