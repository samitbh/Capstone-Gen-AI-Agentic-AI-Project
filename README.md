# Capstone-Gen-AI-Agentic-AI-Project

Project 

The goal of this capstone project is to develop a Generative AI–powered application that enables users to query enterprise documents using autonomous AI agents. The system uses Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and AgenticAI frameworks to retrieve relevant information, reason over it, and generate accurate, context-aware responses.

Project DescriptionThis project aims to build an AI agent–based knowledge and decision support system. The application allows users to upload documents in multiple formats (PDF, TXT, CSV, Excel) and ask natural language questions. The system retrieves relevant content using a vector database and generates grounded responses using an LLM. AI agents are used to plan the task, retrieve information, reason over the retrieved context, and validate the final output, demonstrating a full-fledged Generative AI and Agentic AI workflow.

Tasks for Learners
1.Set up the project foundation
 –Initialize the project repository, environment configuration, and basic application structure for the Generative AI system.
2.Design the user interaction layer
 –Create a simple interface or API that allows users to upload documents and ask natural language questions.
3.Implement document ingestion
 –Enable uploading and processing of enterprise documents in multiple formats such as PDF, TXT, CSV, or Excel.
4.Prepare data for semantic search
 –Convert processed document content into chunks suitable for embedding and retrieval.
5.Build a vector-based knowledge store
 –Generate embeddings and store them in a vector database to support semantic similarity search.
6.Implement intelligent document retrieval
 –Retrieve the most relevant document content based on user queries using similarity search.
7.Develop a Retrieval
-Augmented Generation pipeline
 –Combine retrieved document context with an LLM to generate accurate, grounded responses.
8.Implement agent-based reasoning
 –Create one or more AI agents that plan, retrieve, reason, and generate responses using available tools.
9.Add reliability and safety controls
 –Handle errors, validate inputs, and apply guardrails to reduce hallucinations and unsafe outputs.
10.Deploy and document the solution
 –Deploy the application and provide documentation explaining the architecture, workflow, and limitations.

 Submission Guidelines:
•Submit the complete source code and a documentation file in a Zip format.
•Documentation should explain system setup, architecture, agent roles, and deployment steps, along with limitations and challenges faced during development.  

# Agentic Enterprise RAG Engine (Streamlit Interface)

An enterprise-grade, Generative AI-powered knowledge and decision support application. This system leverages Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), and Agentic AI frameworks to ingest multi-format enterprise documentation, reason over parsed data, and provide grounded, human-verified responses.

---

## 🚀 Key Features

* **Multi-Format Ingestion**: Seamlessly extracts and cleans text from PDF, TXT, CSV, Excel, JSON, and YAML files.
* **Semantic Vector Storage**: Tokenizes content with overlapping sliding windows stored inside persistent `ChromaDB` indices.
* **LangGraph Multi-Agent Architecture**: Uses an isolated state network featuring dedicated **Planner**, **Retriever**, **Reasoning**, and **Validation** agents.
* **Groundedness Enforcement**: Integrated automated compliance loops cross-check final responses to reduce hallucinations.
* **Streamlit UI Panel**: Single-page web interface with responsive sidebar upload queues and diagnostic run tracers.

---

## 📂 Project Structure

```text
Capstone-Gen-AI-Agentic-AI-Project/
├── app/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── graph.py             # LangGraph workflow definitions
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py            # Pydantic configuration models
│   └── services/
│       ├── __init__.py
│       ├── ingestion.py         # Multi-format cleaning engine
│       └── vector_store.py      # ChromaDB interface
├── data/
│   └── static_data/             # Inbound landing repository
├── .env                         # Local runtime credentials (Secret)
├── .gitignore                   # Git exclusion configurations
├── Dockerfile                   # Deployment container manifest
├── DOCUMENTATION.md             # Technical submission document
├── main.py                      # Core Streamlit Web Application
└── requirements.txt             # Frozen dependency manifest
```

---

## 🛠️ Local Setup & Execution

### 1. Prerequisites
Ensure you have **Python 3.11** installed on your workstation.

### 2. Initialization & Environment Configuration
Clone the repository and spin up your virtual environment structure:

```bash
# Navigate to the workspace root
cd ~/Desktop/Capstone-Gen-AI-Agentic-AI-Project

# Activate the existing virtual environment (Git Bash syntax)
source venv/Scripts/activate

# Upgrade the pip package installer
python -m pip install --upgrade pip

# Install required external dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a file named `.env` in your root folder and define your OpenAI API parameters:

```env
OPENAI_API_KEY=your_actual_openai_api_key_here
CHROMADB_PATH=./data/chroma_db
COLLECTION_NAME=enterprise_knowledge
```

### 4. Running the Streamlit App
Fire up your local client application node with the following command:

```bash
streamlit run main.py
```
Your default browser will instantly spin open to `http://localhost:8501`.

---

## 🐳 Docker Deployment

To deploy this application within an isolated container ecosystem, execute these commands from the root directory:

```bash
# Build the application image 
docker build -t enterprise-rag-ui .

# Run the image container
docker run -d -p 8501:8501 --env-file .env enterprise-rag-ui
```

---

## 🤝 Project Submission Checklist

Prior to compressing the directory into the final submission file (`.zip`), verify that:
1. All changes have been committed and pushed to your **GitHub repository**.
2. The local `venv/` and `.env` files are **fully excluded** from tracking via `.gitignore`.
3. Your code works flawlessly when running `streamlit run main.py`.