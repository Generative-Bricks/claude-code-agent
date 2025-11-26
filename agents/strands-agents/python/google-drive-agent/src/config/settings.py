"""
Configuration Management for Google Drive Agent.

Loads settings from environment variables with sensible defaults.

Following SIMPLICITY principle: Single source of truth for configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Project paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    CREDENTIALS_DIR = PROJECT_ROOT / "credentials"
    CACHE_DIR = PROJECT_ROOT / "data" / "cache"

    # Google Drive API
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

    # AWS Configuration (if using Bedrock)
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_PROFILE = os.getenv("AWS_PROFILE", "default")

    # Cache Configuration
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

    @classmethod
    def validate(cls) -> None:
        """
        Validate required settings are present.

        Raises:
            ValueError: If required settings are missing
        """
        errors = []

        # Check if credentials directory exists
        if not cls.CREDENTIALS_DIR.exists():
            errors.append(f"Credentials directory not found: {cls.CREDENTIALS_DIR}")

        # Check for credentials.json
        credentials_file = cls.CREDENTIALS_DIR / "credentials.json"
        if not credentials_file.exists():
            errors.append(
                f"Google OAuth credentials not found: {credentials_file}\n"
                "Please follow setup instructions in README.md"
            )

        if errors:
            raise ValueError("Configuration errors:\n" + "\n".join(errors))

    @classmethod
    def print_settings(cls) -> None:
        """Print current settings (for debugging)."""
        print("⚙️  Current Settings:")
        print(f"   Project Root: {cls.PROJECT_ROOT}")
        print(f"   Credentials Dir: {cls.CREDENTIALS_DIR}")
        print(f"   Cache Dir: {cls.CACHE_DIR}")
        print(f"   Cache Enabled: {cls.CACHE_ENABLED}")
        print(f"   AWS Region: {cls.AWS_REGION}")
        print(f"   Log Level: {cls.LOG_LEVEL}")


# Create singleton instance
settings = Settings()
