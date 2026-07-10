"""
Core interfaces and protocols for SynAI.

This module defines stable abstractions and contracts that prevent circular
dependencies and enable loose coupling between services.
"""

from typing import Any, Protocol


class Skill(Protocol):
    """
    Protocol for extensible skills in SynAI.

    All skills must implement this interface to be registered and executed
    by the skill registry and orchestrator.
    """

    @property
    def name(self) -> str:
        """
        Get the skill name.

        Returns:
            str: A unique identifier for this skill.
        """
        ...

    @property
    def description(self) -> str:
        """
        Get the skill description.

        Returns:
            str: A human-readable description of what this skill does.
        """
        ...

    def can_handle(self, command: str) -> bool:
        """
        Determine if this skill can handle the given command.

        Args:
            command: The user command to evaluate.

        Returns:
            bool: True if this skill can handle the command, False otherwise.
        """
        ...

    def execute(self, command: str) -> str:
        """
        Execute the skill with the given command.

        Args:
            command: The user command to execute.

        Returns:
            str: The result of executing the skill.
        """
        ...
