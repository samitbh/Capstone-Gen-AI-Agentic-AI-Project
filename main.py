# This is the main entry point for the Streamlit application. It sets up the user interface, handles file uploads for document ingestion, and manages the conversational flow for querying the knowledge base using a multi-agent system.
import streamlit as st
from langfuse.callback import CallbackHandler

# Import the centralized core parameters and configuration models
from app.core.config import settings
# Import the core services and agent graph workflow
from app.services.ingestion import DocumentIngestionService
# The VectorStoreService manages all interactions with the ChromaDB vector database, including embedding generation and similarity search.
from app.services.vector_store import VectorStoreService
# The agent_graph is the compiled multi-agent workflow that orchestrates the interactions between the Planner, Retriever, Reasoning, and Validator agents.
from app.agents.graph import agent_graph

# 1. APPLICATION VIEWPORT AND BRANDING LAYOUT
st.set_page_config(page_title="Agentic Knowledge Hub", layout="wide")
st.title("🤖 Enterprise Agentic RAG Control Panel")

# 2. CACHE INTERACTION OBJECTS WITHIN THE APP SESSION STATE
# Streamlit clears modules on click events. Sessions preserve backend buffers.
if "ingestion_service" not in st.session_state:
    st.session_state.ingestion_service = DocumentIngestionService()
if "vector_service" not in st.session_state:
    st.session_state.vector_service = VectorStoreService()
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 3. INITIALIZE THE LIVE LANGFUSE PERFORMANCE TELEMETRY CALLBACK MONITOR
# Collects active agent node execution states and logs token metrics to your Japan Cloud workspace panel.


@st.cache_resource
def get_langfuse_handler():
    return CallbackHandler(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        host=settings.LANGFUSE_HOST
    )


try:
    langfuse_handler = get_langfuse_handler()
    callbacks = [langfuse_handler]
except Exception:
    st.sidebar.warning("⚠️ Telemetry panel offline. Continuing locally.")
    callbacks = []


# 4. DIRECTORY SIDEBAR DATA INGESTION ENGINE
with st.sidebar:
    st.header("📥 Ingestion Center")
    st.caption("Supports: PDF, TXT, CSV, XLSX, JSON, YAML")

    # Mount files direct to clean browser buffer arrays
    uploaded_files = st.file_uploader(
        "Upload Enterprise Assets",
        type=["pdf", "txt", "csv", "xlsx", "json", "yaml", "yml"],
        accept_multiple_files=True
    )

    # Trigger parsing logic on execution call

    if st.button("Index Documents into ChromaDB", use_container_width=True) and uploaded_files:
        for target_file in uploaded_files:
            with st.spinner(f"Ingesting {target_file.name}..."):
                try:
                    file_payload = target_file.read()

                    # Unpack both the text contents and the unique MD5 content signature
                    cleaned_txt, version_hash = st.session_state.ingestion_service.ingest_stream(
                        file_payload, target_file.name
                    )

                    is_duplicate, old_hash = st.session_state.vector_service.check_existing_document(
                        target_file.name)
                    if is_duplicate:
                        if old_hash == version_hash:
                            st.sidebar.warning(
                                f"ℹ️ {target_file.name} matches current index. Skipping.")
                            continue
                        else:
                            st.sidebar.info(
                                f"🔄 Version change detected. Updating {target_file.name}...")
                            st.session_state.vector_service.delete_document_vectors(
                                target_file.name)

                    st.session_state.vector_service.process_and_store(
                        cleaned_txt, {"source_file": target_file.name, "version_hash": version_hash})
                    st.sidebar.success(
                        f"✓ {target_file.name} successfully updated.")
                except Exception as error:
                    st.sidebar.error(
                        f"Error processing {target_file.name}: {str(error)}")

    st.divider()
    st.caption("🔒 Status: **Google AI Studio Free Tier Active**")

# 5. RENDERING CONVERSATIONAL HISTORY CORE LOOKUPS
for chat_node in st.session_state.chat_history:
    with st.chat_message(chat_node["role"]):
        st.markdown(chat_node["content"])

# 6. ENTERPRISE QUERY MULTI-AGENT STATE GRAPH TRIGGER
if user_query := st.chat_input("Query your knowledge base assets..."):
    st.session_state.chat_history.append(
        {"role": "user", "content": user_query})

    # SLIDING WINDOW: Keep only the last 10 messages to prevent local browser UI lag
    if len(st.session_state.chat_history) > 10:
        st.session_state.chat_history = st.session_state.chat_history[-10:]

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Multi-Agent network analyzing operational tasks..."):
            # Set up the base state parameters for LangGraph evaluation including the fallback ceiling counter
            initial_state = {
                "query": user_query,
                "plan": [],
                "context": [],
                "response": "",
                "isValidated": False,
                "retry_count": 0
            }
            try:
                # Trigger the LangGraph Multi-Agent network with live Langfuse callbacks context attached
                final_execution_state = agent_graph.invoke(
                    initial_state,
                    config={"callbacks": callbacks}
                )
                output_text = final_execution_state["response"]

                # Render collapsible telemetry panels for student capstone evaluation
                with st.expander("🛠️ View Agent Execution Logs (Langfuse-Linked)"):
                    plan_list = final_execution_state.get('plan', [])
                    planner_query = (
                        plan_list[0]
                        if isinstance(plan_list, list) and len(plan_list) > 0
                        else "No specific keyword formulation required"
                    )
                    st.markdown(f"**Planner Target Query:** `{planner_query}`")
                    st.markdown(
                        f"**ChromaDB Vector Retrieval Total Chunks:** `{len(final_execution_state.get('context', []))}`")
                    st.markdown(
                        f"**Compliance Auditor Verified:** `{final_execution_state.get('isValidated', False)}`")
                    st.markdown(
                        f"**Total Validation Retries Used:** `{final_execution_state.get('retry_count', 0)} / 2`")

                # Output the verified text
                st.markdown(output_text)
                st.session_state.chat_history.append(
                    {"role": "assistant", "content": output_text})
            except Exception as e:
                st.error(
                    f"Agent Engine Failed to reach execution state: {str(e)}")
