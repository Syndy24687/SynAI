"""
Dependency injection container for SynAI.

This module manages the registration and retrieval of application services.
It provides a centralized container for dependency injection, ensuring that
services are properly instantiated and configured before use.
"""

from typing import Any, Dict, Generic, TypeVar

T = TypeVar("T")


class Container:
    """
    Dependency injection container for managing application services.

    This container stores registered services and their factories, providing
    a central registry for dependency management. It supports both singleton
    and transient service registration patterns.
    """

    def __init__(self) -> None:
        """
        Initialize an empty service container.
        """
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Any] = {}

    def register(self, name: str, service: Any) -> None:
        """
        Register a singleton service in the container.

        Args:
            name: The service identifier.
            service: The service instance.
        """
        self._services[name] = service

    def register_factory(self, name: str, factory: Any) -> None:
        """
        Register a factory function for creating service instances.

        The factory will be called each time the service is requested,
        allowing for transient service creation.

        Args:
            name: The service identifier.
            factory: A callable that creates the service instance.
        """
        self._factories[name] = factory

    def get(self, name: str) -> Any:
        """
        Retrieve a registered service from the container.

        If the service is registered as a singleton, the same instance
        is returned on subsequent calls. If registered as a factory,
        a new instance is created each time.

        Args:
            name: The service identifier.

        Returns:
            Any: The requested service instance.

        Raises:
            KeyError: If the service is not registered in the container.
        """
        if name in self._services:
            return self._services[name]

        if name in self._factories:
            return self._factories[name]()

        raise KeyError(f"Service '{name}' not found in container")

    def has(self, name: str) -> bool:
        """
        Check if a service is registered in the container.

        Args:
            name: The service identifier.

        Returns:
            bool: True if the service is registered, False otherwise.
        """
        return name in self._services or name in self._factories

    def clear(self) -> None:
        """
        Clear all registered services and factories from the container.

        This is useful for testing or resetting the application state.
        """
        self._services.clear()
        self._factories.clear()


def create_container() -> Container:
    """
    Create and configure the application dependency injection container.

    This function initializes a container and registers all application
    services. Services are registered in the correct order to satisfy
    dependencies.

    Returns:
        Container: A configured dependency injection container.
    """
    import logging

    from src.config.settings import get_settings
    from src.core.skill_registry import SkillRegistry
    from src.core.orchestrator import Orchestrator
    from src.skills.tell_time import TellTimeSkill
    from src.skills.tell_date import TellDateSkill
    from src.skills.tell_joke import TellJokeSkill

    logger = logging.getLogger(__name__)
    container = Container()

    skill_registry = SkillRegistry()
    skill_registry.register(TellTimeSkill())
    skill_registry.register(TellDateSkill())
    skill_registry.register(TellJokeSkill())

    container.register("skill_registry", skill_registry)
    container.register("orchestrator", Orchestrator(skill_registry))

    settings = get_settings()

    try:
        from src.services.speech.speech_recognizer import SpeechRecognizer
        from src.services.speech.speech_synthesizer import SpeechSynthesizer
        from src.services.speech.speech_service import SpeechService

        recognizer = SpeechRecognizer(settings.speech_model_path)
        synthesizer = SpeechSynthesizer()
        speech_service = SpeechService(recognizer, synthesizer)

        container.register("speech_service", speech_service)
        logger.debug("Speech service registered")

    except Exception as e:
        logger.debug(f"Speech service not available: {e}")

    return container
