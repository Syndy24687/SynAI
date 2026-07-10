"""
Skill for telling the current time.

This skill responds to time-related queries and returns the current time
in a human-readable format.
"""

from datetime import datetime

from src.skills.base import BaseSkill


class TellTimeSkill(BaseSkill):
    """
    Skill that tells the current time.

    This skill matches queries about the current time and returns the
    time in a user-friendly format.
    """

    @property
    def name(self) -> str:
        """
        Get the skill name.

        Returns:
            str: "tell_time"
        """
        return "tell_time"

    @property
    def description(self) -> str:
        """
        Get the skill description.

        Returns:
            str: Description of this skill's capabilities.
        """
        return "Tells the current time"

    def can_handle(self, command: str) -> bool:
        """
        Determine if this skill can handle time-related queries.

        Matches commands containing keywords like "time", "what time",
        "current time", etc.

        Args:
            command: The user command to evaluate.

        Returns:
            bool: True if the command is about the current time.
        """
        keywords = ["time", "what time is it", "what's the time", "current time"]
        command_lower = command.lower()
        return any(keyword in command_lower for keyword in keywords)

    def execute(self, command: str) -> str:
        """
        Execute the skill and return the current time.

        Args:
            command: The user command (not used for time queries).

        Returns:
            str: The current time in a human-readable format.
        """
        current_time = datetime.now().strftime("%I:%M %p")
        self.logger.info(f"Told current time: {current_time}")
        return f"The current time is {current_time}"
