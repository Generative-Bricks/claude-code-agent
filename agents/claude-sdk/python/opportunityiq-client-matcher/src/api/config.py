"""
API Configuration Settings

Manages all API configuration via environment variables and Pydantic settings.

Biblical Principle: EXCELLENCE - Centralized, validated configuration
"""

from pathlib import Path
from pydantic_settings import BaseSettings


class APISettings(BaseSettings):
    """
    API configuration settings loaded from environment variables.
    
    All settings can be overridden via .env file or environment variables.
    """
    
    # API Server Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = False  # Set to True for development
    
    # CORS Configuration
    cors_origins: list[str] = [
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://localhost:8080",  # Vue default
    ]
    cors_credentials: bool = True
    cors_methods: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_headers: list[str] = ["*"]
    
    # Logging Configuration
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logs_dir: Path = Path("logs")
    
    # Anthropic API Configuration
    anthropic_api_key: str = ""  # Required - set in .env
    
    # Data Paths
    scenarios_directory: str = "data/scenarios"
    clients_directory: str = "data/clients"
    reports_directory: str = "outputs"
    
    # Matching Defaults
    min_match_threshold: float = 60.0
    default_match_weight: float = 0.4
    default_revenue_weight: float = 0.6
    default_ranking_strategy: str = "composite"
    
    # API Security (optional for MVP)
    api_key: str = ""  # Optional API key for authentication
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        env_file_encoding = "utf-8"


# Global settings instance
settings = APISettings()

# Create logs directory if it doesn't exist
settings.logs_dir.mkdir(parents=True, exist_ok=True)





