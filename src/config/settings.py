"""
Configuration management for SynAI.

This module provides typed configuration loading from environment variables
using Pydantic settings. All configuration is centralized here for easy access
and validation across the application.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Settings are validated using Pydantic and can be customized through
    environment variables or a .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "SynAI"
    app_debug: bool = False
    app_log_level: str = "INFO"

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "neural-chat"

    database_url: str = "sqlite:///./data/synai.db"

    log_dir: Path = Path("./logs")
    
    speech_model_path: Path = Path("./models/vosk-model-small-en-us-0.15")

    def __init__(self, **data):
        """
        Initialize settings.

        Args:
            **data: Keyword arguments to override default settings.
        """
        super().__init__(**data)
        self.log_dir.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    """
    Get the application settings instance.

    This function provides a single point of access to the application
    configuration and ensures consistent settings throughout the application.

    Returns:
        Settings: The validated application settings.
    """
    return Settings()
