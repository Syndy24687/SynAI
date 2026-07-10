"""
Application bootstrap and initialization for SynAI.

This module handles application startup, service initialization, and
orchestration setup. It prepares the application for operation by
configuring all necessary components.
"""

import logging

from src.config.settings import get_settings
from src.core.container import create_container
from src.core.container import Container
from src.core.orchestrator import Orchestrator
from src.services.speech.speech_service import SpeechService


class Application:
    """
    Main application class responsible for bootstrapping SynAI.

    The Application class initializes all application services, configures
    the dependency container, and prepares the system for operation. It
    serves as the central entry point for application lifecycle management.
    """

    def __init__(self) -> None:
        """
        Initialize the application with configuration and container setup.

        During initialization, the application loads settings, creates the
        dependency injection container, and registers necessary services.
        """
        self.settings = get_settings()
        self.container = create_container()
        self.logger = logging.getLogger(__name__)
        self.orchestrator: Orchestrator = self.container.get("orchestrator")
        self.speech_service: SpeechService | None = None

        try:
            self.speech_service = self.container.get("speech_service")
        except KeyError:
            self.logger.debug("Speech service not available")

    def startup(self) -> None:
        """
        Perform application startup operations.

        This method initializes all services and prepares the application
        for operation. It is called after the application is constructed
        and before the main event loop starts.
        """
        self.logger.info(f"Starting {self.settings.app_name}")
        self.logger.debug(f"Debug mode: {self.settings.app_debug}")
        self.logger.debug(f"Ollama URL: {self.settings.ollama_base_url}")

        skills = self.orchestrator.get_skills()
        self.logger.info(f"Loaded {len(skills)} skills")
        for skill in skills:
            self.logger.debug(f"  - {skill.name}: {skill.description}")

        if self.speech_service:
            self.logger.info("Speech service enabled")
        else:
            self.logger.debug("Speech service disabled")

        self.logger.info(f"{self.settings.app_name} initialized successfully")

    def shutdown(self) -> None:
        """
        Perform application shutdown operations.

        This method cleans up resources and performs any necessary shutdown
        operations. It is called when the application terminates.
        """
        self.logger.info(f"Shutting down {self.settings.app_name}")

        if self.speech_service:
            try:
                self.speech_service.close()
            except Exception as e:
                self.logger.error(f"Error closing speech service: {e}", exc_info=True)

        self.container.clear()

    def get_container(self) -> Container:
        """
        Get the application's dependency injection container.

        Args:
            Returns:
            Container: The dependency injection container.
        """
        return self.container

    def execute_command(self, command: str) -> str:
        """
        Execute a user command through the orchestrator.

        Args:
            command: The user command to execute.

        Returns:
            str: The result of executing the command.
        """
        return self.orchestrator.execute_command(command)

    def listen(self, timeout: float | None = None) -> str | None:
        """
        Listen for speech input.

        Args:
            timeout: Optional timeout in seconds.

        Returns:
            str: The recognized speech, or None if no speech was recognized.

        Raises:
            RuntimeError: If speech service is not available.
        """
        if not self.speech_service:
            raise RuntimeError("Speech service is not available")
        return self.speech_service.listen(timeout)

    def speak(self, text: str) -> None:
        """
        Speak the given text using text-to-speech synthesis.

        Args:
            text: The text to speak.

        Raises:
            RuntimeError: If speech service is not available.
        """
        if not self.speech_service:
            raise RuntimeError("Speech service is not available")
        self.speech_service.speak(text)

    def has_speech_service(self) -> bool:
        """
        Check if speech service is available.

        Returns:
            bool: True if speech service is available, False otherwise.
        """
        return self.speech_service is not None


def create_app() -> Application:
    """
    Create and initialize the application instance.

    This function is the primary factory for creating the application.
    It handles all necessary setup and configuration to ensure the
    application is ready for use.

    Returns:
        Application: A configured Application instance.
    """
    app = Application()
    return app
