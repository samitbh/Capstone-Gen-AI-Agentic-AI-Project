# This module defines the DocumentIngestionService class,
# which provides functionality to ingest and extract content
# from various file formats (TXT, PDF, CSV, Excel, JSON, YAML) uploaded as byte streams.
# The service handles the parsing and conversion of these formats
# into a unified string representation that can be further processed
#  by the application's multi-agent system.
# It uses libraries like PyPDF2 for PDF parsing and
# pandas for tabular data handling,
# ensuring robust support for a wide range of enterprise document types.

import io
import json
import logging
import pandas as pd
import PyPDF2

# Configure tracking metrics for background system logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DocumentIngestionService")


class DocumentIngestionService:
    """
    Multi-format cleaning engine that extracts content layers from file 
    byte streams uploaded via Streamlit.
    """

# The ingest_stream method takes in raw byte data and the file name,
# determines the file type based on the extension,
# and applies the appropriate parsing logic to return a clean text string.
# It supports TXT, PDF, CSV, Excel, JSON, and YAML formats,
# making it a versatile component for the document ingestion pipeline.
#  With error handling to manage unsupported formats and decoding issues
    def ingest_stream(self, file_payload: bytes, file_name: str) -> str:
        ext = file_name.split(".")[-1].lower()
        """
        Routes the inbound file payload to its designated format extractor based on extension.
        Includes localized error-trapping bounds to guarantee application runtime stability.
        """
        if not file_payload:
            raise ValueError(
                f"Ingestion failed: The uploaded file '{file_name}' is empty.")
        ext = file_name.split(".")[-1].lower()
        logger.info(
            f"Initiating ingestion trace pipeline for resource asset: {file_name} [Extension: .{ext}]")

        try:
            if ext == "txt":
                # Simple text files are decoded directly into strings. The 'ignore' error handling ensures that any non-UTF-8 bytes are skipped without crashing the ingestion process.
                return file_payload.decode("utf-8", errors="ignore")
            elif ext == "pdf":
                text_buffer = []
                pdf_file = io.BytesIO(file_payload)
                reader = PyPDF2.PdfReader(pdf_file)
                for page in reader.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text_buffer.append(extracted_text)
                return "\n".join(text_buffer)
            elif ext in ["csv", "xlsx"]:
                buffer = io.BytesIO(file_payload)
                df = pd.read_csv(
                    buffer) if ext == "csv" else pd.read_excel(buffer)
                return df.to_json(orient="records", indent=2)
            elif ext in ["json", "yaml", "yml"]:
                raw_string = file_payload.decode("utf-8", errors="ignore")
                if ext == "json":
                    return json.dumps(json.loads(raw_string), indent=2)
                return raw_string
            else:
                raise ValueError(
                    f"Extension .{ext} is not supported by the ingestion service.")
        except Exception as e:
            logger.error(
                f"Critical execution fault processing file '{file_name}': {str(e)}")
            # Re-raise with a clean user-facing wrapper message for the Streamlit UI layer
            raise RuntimeError(
                f"Failed to process '{file_name}' due to structural formatting errors: {str(e)}")
