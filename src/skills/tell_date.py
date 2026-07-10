"""
Skill for telling today's date.

This skill responds to date-related queries and returns today's date
in a human-readable format.
"""

from datetime import datetime

from src.skills.base import BaseSkill


class TellDateSkill(BaseSkill):
    """
    Skill that tells today's date.

    This skill matches queries about today's date and returns the date
    in a user-friendly format.
    """

    @property
    def name(self) -> str:
        """
        Get the skill name.

        Returns:
            str: "tell_date"
        """
        return "tell_date"

    @property
    def description(self) -> str:
        """
        Get the skill description.

        Returns:
            str: Description of this skill's capabilities.
        """
        return "Tells today's date"

    def can_handle(self, command: str) -> bool:
        """
        Determine if this skill can handle date-related queries.

        Matches commands containing keywords like "date", "today",
        "today's date", "what date is it", etc.

        Args:
            command: The user command to evaluate.

        Returns:
            bool: True if the command is about today's date.
        """
        keywords = ["date", "today", "today's date", "what date", "current date"]
        command_lower = command.lower()
        return any(keyword in command_lower for keyword in keywords)

    def execute(self, command: str) -> str:
        """
        Execute the skill and return today's date.

        Args:
            command: The user command (not used for date queries).

        Returns:
            str: Today's date in a human-readable format.
        """
        today = datetime.now().strftime("%A, %B %d, %Y")
        self.logger.info(f"Told current date: {today}")
        return f"Today is {today}"
