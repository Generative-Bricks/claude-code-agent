"""
API Configuration for Portfolio Collaboration System.

Manages environment variables and application settings for the FastAPI server.

Biblical Principle: EXCELLENCE - Production-ready configuration from inception.
"""

import os
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API server host")
    api_port: int = Field(default=8000, description="API server port")
    api_reload: bool = Field(default=True, description="Enable auto-reload in development")

    # CORS Configuration
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:5173",  # Vite dev server
            "http://localhost:3000",  # Alternative frontend port
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
        ],
        description="Allowed CORS origins",
    )
    cors_credentials: bool = Field(default=True, description="Allow credentials")
    cors_methods: List[str] = Field(default=["*"], description="Allowed HTTP methods")
    cors_headers: List[str] = Field(default=["*"], description="Allowed HTTP headers")

    # OpenAI Configuration
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY", description="OpenAI API key")

    # Application Paths
    project_root: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent.parent,
        description="Project root directory",
    )

    @property
    def examples_dir(self) -> Path:
        """Path to examples directory."""
        return self.project_root / "examples"

    @property
    def outputs_dir(self) -> Path:
        """Path to outputs directory."""
        return self.project_root / "outputs"

    @property
    def logs_dir(self) -> Path:
        """Path to logs directory."""
        return self.project_root / "logs"

    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        description="Log message format",
    )

    class Config:
        """Pydantic settings configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env that aren't in APISettings


# Global settings instance
settings = APISettings()

# Ensure required directories exist
settings.outputs_dir.mkdir(parents=True, exist_ok=True)
settings.logs_dir.mkdir(parents=True, exist_ok=True)
