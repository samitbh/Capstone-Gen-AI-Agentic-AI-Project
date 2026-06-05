# Import the native time module to control API call pacing
import time
# Efficiently breaks large documents into manageable chunks with overlap for context retention.
from langchain_text_splitters import RecursiveCharacterTextSplitter
# A high-performance vector database that supports persistent storage and fast similarity search.
from langchain_community.vectorstores import Chroma
# Google's enterprise-grade embedding model that converts text into dense vector representations for semantic search and retrieval.
from langchain_google_genai import GoogleGenerativeAIEmbeddings
# Centralized configuration management for the application, including API keys and database settings.
from app.core.config import settings

# The VectorStoreService class encapsulates all operations related to text processing, embedding generation, and vector storage. It initializes the necessary components for handling document ingestion and retrieval, providing a clean interface for the rest of the application to interact with the vector store.


class VectorStoreService:
    def __init__(self):
        # 1. Initialize Google's Enterprise Text Embedding Model
        # Converts text chunks into 768-dimensional dense vector matrices.
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=settings.GOOGLE_API_KEY
        )

        # 2. Configure Semantic Chunking Boundaries
        # Breaks large documents down into 1,000-character pieces.
        # The 150-character overlap prevents losing context at split points.
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=150
        )

        # 3. Connect Persistently to the Local ChromaDB Instance
        # Uses Cosine Distance natively to map and look up similar vectors.
        # Links directly to the collection name defined in your configuration.
        self.db = Chroma(
            persist_directory=settings.CHROMADB_PATH,
            embedding_function=self.embeddings,
            collection_name=settings.COLLECTION_NAME
        )

    def process_and_store(self, text: str, metadata: dict, batch_size: int = 5):
        """
        Splits incoming raw document strings into chunks, generates 
        vector embeddings in paced batches to prevent 429 Quota exhaustion errors (Google API rate limits for free tier),
        and saves them permanently into ChromaDB.
        """
        # Segment the large text payload into overlapping pieces
        chunks = self.splitter.split_text(text)
        total_chunks = len(chunks)

        # Tag every single chunk with metadata (e.g., the source file name)
        metadatas = [metadata for _ in chunks]

        # Paced Batch Processing: Upload chunks in safe groups of 10
        for i in range(0, total_chunks, batch_size):
            batch_chunks = chunks[i: i + batch_size]
            batch_metadatas = metadatas[i: i + batch_size]

            # Commit the current batch to the database
            self.db.add_texts(texts=batch_chunks, metadatas=batch_metadatas)

            # Introduce a 2-second delay between batches to stay under the 100 requests/min ceiling
            if i + batch_size < total_chunks:
                time.sleep(1.5)

    def similarity_search(self, query: str, k: int = 3):
        """
        Converts a user query into a vector, runs a cosine similarity 
        search against ChromaDB, and returns the top-K matching text pieces.
        """
        # Search the database for the k-closest matching document chunks
        docs = self.db.similarity_search(query, k=k)

        # Extract and return just the raw string content from the documents
        return [doc.page_content for doc in docs]
