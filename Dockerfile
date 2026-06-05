# 1. Use explicit deterministic stable slim base image matching your host Python environment
FROM python:3.12-slim-bookworm

# Prevent Python from writing pyc files and enable unbuffered output logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/workspace

WORKDIR /workspace

# Install system dependencies needed for compiling certain python utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only dependencies first to utilize layer caching mechanics
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy structural codebase blocks
COPY app/ ./app/
COPY main.py .

# Create internal persistent structural directory references
RUN mkdir -p /workspace/data/chroma_db /workspace/data/static_data

# Create and switch to non-privileged user account for security isolation
RUN useradd -u 8888 appuser && chown -R appuser:appuser /workspace
USER appuser

EXPOSE 8501

# Launch production web service container configuration
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
