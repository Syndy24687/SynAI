"""
Base skill class for SynAI skills.

This module provides a base class that all skills should inherit from,
providing common functionality and ensuring consistent behavior across
all skill implementations.
"""

import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseSkill(ABC):
    """
    Abstract base class for all SynAI skills.

    All concrete skill implementations should inherit from this class
    and implement the abstract methods to ensure consistent behavior.
    """

    def __init__(self) -> None:
        """
        Initialize the skill with logging support.
        """
        self.logger = logging.getLogger(self.__class__.__name__)

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the skill name.

        Returns:
            str: A unique identifier for this skill.
        """
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Get the skill description.

        Returns:
            str: A human-readable description of what this skill does.
        """
        ...

    @abstractmethod
    def can_handle(self, command: str) -> bool:
        """
        Determine if this skill can handle the given command.

        Args:
            command: The user command to evaluate.

        Returns:
            bool: True if this skill can handle the command, False otherwise.
        """
        ...

    @abstractmethod
    def execute(self, command: str) -> str:
        """
        Execute the skill with the given command.

        Args:
            command: The user command to execute.

        Returns:
            str: The result of executing the skill.
        """
        ...
