# Configuration settings for the application
# This module defines the AppConfig class, which uses Pydantic's BaseSettings to manage application configuration. It includes settings for Google Gemini authentication, local ChromaDB storage, and Langfuse telemetry. The constructor validates the presence of required environment variables and provides a user-friendly error message if any are missing. A global instance of the configuration is created for use throughout the application.
import sys
# Import necessary libraries for configuration management and validation
from pydantic import ValidationError, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# application settings, database settings, and security settings. The model_config attribute specifies that the configuration should be loaded from a .env file with UTF-8 encoding.
from typing import Optional

# Define the AppConfig class that inherits from BaseSettings


class AppConfig(BaseSettings):
    # 1. Google Gemini Core API Access Key (Mandatory)
    GOOGLE_API_KEY: str = Field(...,
                                description="Google Gemini Core API Access Key")

    # 2. Local ChromaDB Storage Variables
    CHROMADB_PATH: str = "./data/chroma_db"
    COLLECTION_NAME: str = "enterprise_knowledge"

    # 3. Langfuse Region-Specific Telemetry (Japan Cloud)
    LANGFUSE_PUBLIC_KEY: Optional[str] = None
    LANGFUSE_SECRET_KEY: Optional[str] = None
    LANGFUSE_HOST: str = "https://jp.cloud.langfuse.com"

    # 4. Pydantic Environment File Bindings
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def __init__(self, **values):
        """Self-validating constructor that intercepts missing configuration errors."""
        try:
            super().__init__(**values)
        except ValidationError as error:
            sys.exit(
                f"\n{'='*60}\n"
                f"❌ CRITICAL CONFIGURATION ERROR\n"
                f"{'='*60}\n"
                f"Your '.env' file is missing mandatory environment variables.\n"
                f"Please ensure it contains your secret keys:\n\n"
                f"👉 GOOGLE_API_KEY=your_gemini_key\n\n"
                f"Error Details:\n{error}\n"
                f"{'='*60}\n"
            )


# Create a global instance of the AppConfig class to be used throughout the application
settings = AppConfig()
