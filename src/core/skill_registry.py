"""
Skill registry for discovering and managing skills.

This module provides a centralized registry for skill registration and discovery,
enabling dynamic skill loading and execution through the orchestrator.
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class SkillRegistry:
    """
    Registry for managing and discovering skills.

    The SkillRegistry maintains a list of registered skills and provides
    methods to register new skills, find skills that can handle commands,
    and execute them.
    """

    def __init__(self) -> None:
        """
        Initialize an empty skill registry.
        """
        self._skills: Dict[str, Any] = {}

    def register(self, skill: Any) -> None:
        """
        Register a skill in the registry.

        Args:
            skill: A skill instance that implements the Skill protocol.

        Raises:
            ValueError: If a skill with the same name is already registered.
        """
        if skill.name in self._skills:
            msg = f"Skill '{skill.name}' is already registered"
            raise ValueError(msg)

        self._skills[skill.name] = skill
        logger.debug(f"Registered skill: {skill.name}")

    def find_skill(self, command: str) -> Any | None:
        """
        Find a skill that can handle the given command.

        This method iterates through registered skills and returns the first
        one that can handle the command. If multiple skills can handle a
        command, the first registered one is returned.

        Args:
            command: The user command to handle.

        Returns:
            Any: The skill that can handle the command, or None if no skill
                 can handle it.
        """
        for skill in self._skills.values():
            if skill.can_handle(command):
                logger.debug(f"Found skill '{skill.name}' for command: {command}")
                return skill

        logger.debug(f"No skill found for command: {command}")
        return None

    def get_all_skills(self) -> List[Any]:
        """
        Get all registered skills.

        Returns:
            List[Any]: A list of all registered skill instances.
        """
        return list(self._skills.values())

    def get_skill(self, name: str) -> Any | None:
        """
        Get a skill by name.

        Args:
            name: The name of the skill to retrieve.

        Returns:
            Any: The skill instance, or None if not found.
        """
        return self._skills.get(name)

    def is_registered(self, name: str) -> bool:
        """
        Check if a skill is registered by name.

        Args:
            name: The name of the skill to check.

        Returns:
            bool: True if the skill is registered, False otherwise.
        """
        return name in self._skills

    def clear(self) -> None:
        """
        Clear all registered skills from the registry.

        This is useful for testing or resetting the application state.
        """
        self._skills.clear()
        logger.debug("Cleared skill registry")
