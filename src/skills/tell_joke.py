"""
Skill for telling jokes.

This skill responds to joke requests and returns random jokes using the
pyjokes library.
"""

import pyjokes

from src.skills.base import BaseSkill


class TellJokeSkill(BaseSkill):
    """
    Skill that tells jokes.

    This skill matches requests for jokes and returns random jokes
    from a collection of programming jokes.
    """

    @property
    def name(self) -> str:
        """
        Get the skill name.

        Returns:
            str: "tell_joke"
        """
        return "tell_joke"

    @property
    def description(self) -> str:
        """
        Get the skill description.

        Returns:
            str: Description of this skill's capabilities.
        """
        return "Tells a random joke"

    def can_handle(self, command: str) -> bool:
        """
        Determine if this skill can handle joke requests.

        Matches commands containing keywords like "joke", "tell me a joke",
        "make me laugh", etc.

        Args:
            command: The user command to evaluate.

        Returns:
            bool: True if the command is a request for a joke.
        """
        keywords = ["joke", "tell me a joke", "make me laugh", "funny"]
        command_lower = command.lower()
        return any(keyword in command_lower for keyword in keywords)

    def execute(self, command: str) -> str:
        """
        Execute the skill and return a random joke.

        Args:
            command: The user command (not used for joke requests).

        Returns:
            str: A random programming joke.
        """
        joke = pyjokes.get_joke(language="en", category="neutral")
        self.logger.info("Told a joke")
        return joke
