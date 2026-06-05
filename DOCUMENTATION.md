# Technical Submission Documentation
## System Architecture, Multi-Agent Operations & Evaluation Report

**Project Name:** Capstone-Gen-AI-Agentic-AI-Project  
**Course Context:** Generative AI & Agentic AI Capstone Project  
**Target Environment:** Docker Containerized / Local Streamlit Deployment  

---

## 🏗️ 1. System Architecture Overview

This application implements an enterprise-grade Retrieval-Augmented Generation (RAG) system orchestrated by an advanced multi-agent state network. The primary objective is to allow users to securely ingest diverse enterprise documentation and query it using autonomous AI agents that reason, fact-check, and self-correct within strict token and loop boundaries.

### Component Map & Data Lifecycles
1. **User Interface Layer (`main.py`)**: A Streamlit web application running a sliding-window message limit to prevent browser lag, handling file upload streams, conversational history, and interactive agent diagnostic tracers.
2. **Configuration Engine (`app/core/config.py`)**: A self-validating environment broker built with Pydantic Settings (`v2.13.4`) that handles local paths and cloud analytics keys from `.env`.
3. **Multi-Format Ingestion Processor (`app/services/ingestion.py`)**: A modular data parsing hub leveraging `PyPDF2` and `pandas` to isolate text matrices from PDF, TXT, CSV, XLSX, JSON, and YAML formats.
4. **Vector Storage Layer (`app/services/vector_store.py`)**: Houses the text chunker splitter (1000 size, 150 overlap) and interfaces persistently with local `ChromaDB` storage utilizing Google's modern `gemini-embedding-001` framework (3072 dimensions).
5. **Multi-Agent Orchestration Graph (`app/agents/graph.py`)**: A compiled cyclic state router built on top of LangGraph (`v0.2.x`+ ecosystem) containing explicit edge dictionary mapping parameters and a deterministic fallback mechanism to intercept infinite loops.

---

## 🤖 2. Autonomous Agent Roles & Bounded State Workflows

The framework relies on a centralized state dictionary layout (`AgentState`) passed sequentially between specialized AI processing nodes. Every reasoning step is driven by **Google Gemini-2.5-Flash-Lite** with temperature settings locked at `0.0` to force factual correctness.

```text
       +--------------------------------------------+

       |             [ START: USER QUERY ]          |
       +--------------------------------------------+

                             |
                             v
                     [ PLANNER AGENT ]
                             |
                             v
               +---> [ RETRIEVER AGENT ] (retry_count + 1)

               |             |
               |             v

               |     [ REASONING AGENT ]
               |             |
               |             v

               |     [ VALIDATOR AGENT ]
               |             |
               +--- (If Response INVALID & retries < 3)

                             |
                (If Response INVALID & retries >= 3)
                             |
                             v
                  [ FALLBACK END NODE ] 
                     (Graceful Warning)
                             |
                             v
                        [ END STATE ]
```

### Detailed Agent Network Matrix

*   **Planner Agent (`planner_node`)**: Receives the raw user input, removes conversational fluff, and formulates precise target keywords optimized for vector search. It resets the `retry_count` back-end baseline key to `0` at the start of every new conversation query.
*   **Retriever Agent (`retriever_node`)**: Queries the local ChromaDB index using the planner's keywords to isolate the top 3 matching text context fragments (`k=3`). Every time this node is entered from a validation failure, it increments `retry_count` by `+1`.
*   **Reasoning Agent (`reasoning_node`)**: Reviews the text snippets to synthesize a grounded, ultra-short answer restricted to 1-3 sentences and under 50 words. If the documents are completely missing the answer, it prints an immediate fallback escape sequence: `"Context Insufficient"`.
*   **Validator Agent (`validator_node`)**: Audits the draft answer against the raw context files. If it finds ungrounded assertions, it flags the state pass marker as `False`. If it encounters `"Context Insufficient"`, it flags it as `True` to bypass unnecessary database loops.
*   **Fallback End Node (`fallback_end_node`)**: An emergency exit node. If an answer fails validation 3 times in a row, the graph stops execution and cleanly appends a compliance warning note to the response string.

### Bounded Router Condition (`router_condition`)
Your LangGraph engine calls this routing function automatically upon exiting the validator. If an answer is marked `INVALID`, it checks the `retry_count`. If the loop count is below 3, it routes the state back to the retriever to self-correct. If it hits or exceeds 3, it diverts the path straight to the fallback node to abort execution and protect your API budget.

---

## 🛠️ 3. System Configuration & Setup Instructions

### 1. Environment Configurations (`.env`)
Create an environment file named `.env` in the project root folder directory:
```env
GOOGLE_API_KEY=AIzaSyYourActualGoogleGeminiKeyHere
CHROMADB_PATH=./data/chroma_db
COLLECTION_NAME=enterprise_knowledge
LANGFUSE_SECRET_KEY=sk-lf-your-actual-secret-key
LANGFUSE_PUBLIC_KEY=pk-lf-your-actual-public-key
LANGFUSE_HOST==https://jp.cloud.langfuse.com  # Configured for region-specific Langfuse Japan Cloud telemetry
```

### 2. Local Terminal Execution (Git Bash Syntax)
```bash
# Activate virtual environment
source venv/Scripts/activate

# Install synchronized, conflict-free manifest packages
pip install --force-reinstall -r requirements.txt

# Launch presentation viewport interface
streamlit run main.py
```

---

## 🐳 4. Docker Deployment Strategy & Environment Lifecycles

To guarantee platform isolation and strict execution repeatability across heterogeneous dev environments, the application is fully containerized under a multi-layer Docker architecture layout. 

### Operational Workflow Controls

1. **Host Daemon Requirement**: The local deployment requires **Docker Desktop** to be fully initialized and running on the host system to establish the named pipe connection interface (`npipe:////./pipe/dockerDesktopLinuxEngine`).
2. **Build and Instantiation**: Application packages and source files are compiled into a cached image layer via the `docker build` command. Running containers are bound to port `8501` and fed project environment keys dynamically using the `--env-file .env` flag constraint.
3. **Session Demolition Guidelines**: To maintain proper network state hygiene, evaluators must cleanly decommission the active container footprint upon session termination. Executing the sequence below safely tears down the runtime instance container while leaving the master compiled package image intact:
```bash
docker stop rag-running-app
docker rm rag-running-app
```

---

## ⚠️ 5. Technical Challenges Faced & Resolutions

1.  **Infinite Token Drainage Loop**: Cyclic multi-agent self-correction maps are excellent for fixing hallucinations, but they risk looping endlessly if a user query cannot be answered by the text corpus. This was resolved by designing an explicit `retry_count` integer variable in the LangGraph global state schema and adding a hard ceiling threshold of 3 attempts inside the traffic router.
2.  **429 Resource Quota Exhaustion (Free-Tier Rate Limits)**: Heavy multi-row spreadsheet conversions and large enterprise PDFs overloaded Google AI Studio's Free-Tier ceiling (100 Requests Per Minute / 1,500 Tokens Per Minute limit). This was completely resolved by converting the ingestion engine into a regulated batch processing network (`batch_size=5`), utilizing native Python time-delay loops (`time.sleep(1.5)`) between chunk deliveries to ensure high-volume documents slide safely under API limits.
3.  **Vector DB Chonological Duplication**: Reloading files or updating older system documents appended duplicate vector blocks to ChromaDB, corrupting context windows (`k=3`) with redundant inputs. This was solved by integrating a local **MD5 Hash Checksum Fingerprint Engine** into `vector_store.py`. The service hashes incoming text profiles, automatically skips exact content matches, and explicitly executes `self.db.delete()` to clear stale chunks before loading updated versions.
4.  **LangGraph 0.2/LangChain-Core Dependency Mismatch**: Explicitly forcing older dependencies (`langchain-core<0.2.0`) clashed with newer LangGraph packages that required a security patch parameter (`allowed_objects`). This caused a terminal boot crash (`TypeError: Reviver.__init__()`). This was resolved by lifting the legacy locks and migrating the repository layout forward to `langchain-core>=0.2.43`, updating the conditional edge routers to utilize structured routing dictionaries (`{END: END, "retriever": "retriever"}`).

## 🛡️ 6. Zero-Cost Security & Guardrail Compliance Matrix

The system implements a multi-tier defense architecture to enforce data integrity, key security, and runtime isolation with zero financial overhead:

*   **Infrastructure Isolation**: The Docker deployment engine drops system root permissions via `USER appuser`, sandboxing package execution processes away from the host kernel.
*   **API Exhaustion Mitigation**: Loop counters inside `graph.py` throttle the conditional self-correction engine to 3 execution cycles maximum, blocking infinite token drainage loops.
*   **Data Ingestion Integrity Gateway**: Strict allow-list extension parsers in `ingestion.py` trap unmapped binary assets, avoiding dangerous payload decoding crashes.
*   **Environment Security Mappings**: Cryptographic secret credentials (`GOOGLE_API_KEY`) are decoupled from source modules using Pydantic validation brokers, preventing credential leaks during code commits.
