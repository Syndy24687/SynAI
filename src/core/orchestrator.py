"""
Central orchestrator for SynAI command handling.

The orchestrator routes incoming commands to appropriate skills and
coordinates the execution of tasks across the system.
"""

import logging
from typing import Any

from src.core.skill_registry import SkillRegistry

logger = logging.getLogger(__name__)


class Orchestrator:
    """
    Central coordinator for command routing and execution.

    The Orchestrator is responsible for:
    - Receiving user commands
    - Finding the appropriate skill to handle each command
    - Executing the skill and returning results
    - Handling cases where no skill matches a command
    """

    def __init__(self, skill_registry: SkillRegistry) -> None:
        """
        Initialize the orchestrator with a skill registry.

        Args:
            skill_registry: The registry containing available skills.
        """
        self.skill_registry = skill_registry
        logger.debug("Orchestrator initialized")

    def execute_command(self, command: str) -> str:
        """
        Execute a command by finding and running the appropriate skill.

        This method:
        1. Searches for a skill that can handle the command
        2. Executes the skill if found
        3. Returns a friendly error message if no skill matches

        Args:
            command: The user command to execute.

        Returns:
            str: The result of executing the command, or a message indicating
                 no matching skill was found.
        """
        logger.info(f"Processing command: {command}")

        skill = self.skill_registry.find_skill(command)

        if skill is None:
            msg = "Sorry, I couldn't find a skill to handle that command."
            logger.warning(f"No skill found for: {command}")
            return msg

        try:
            result = skill.execute(command)
            logger.info(f"Command executed successfully by skill: {skill.name}")
            return result
        except Exception as e:
            msg = f"Error executing skill '{skill.name}': {e}"
            logger.error(msg, exc_info=True)
            return f"An error occurred: {e}"

    def get_skills(self) -> list[Any]:
        """
        Get all available skills.

        Returns:
            list[Any]: A list of all registered skills.
        """
        return self.skill_registry.get_all_skills()
