"""
Combined speech service for SynAI.

This module provides a unified interface for speech recognition and synthesis,
coordinating both services for complete voice interaction capabilities.
"""

import logging

from src.services.speech.speech_recognizer import SpeechRecognizer
from src.services.speech.speech_synthesizer import SpeechSynthesizer

logger = logging.getLogger(__name__)


class SpeechService:
    """
    Unified interface for speech recognition and synthesis.

    This service combines speech recognition and synthesis capabilities,
    providing methods for both listening and speaking through a single API.
    """

    def __init__(
        self,
        recognizer: SpeechRecognizer,
        synthesizer: SpeechSynthesizer,
    ) -> None:
        """
        Initialize the speech service with recognizer and synthesizer.

        Args:
            recognizer: The speech recognizer service.
            synthesizer: The speech synthesizer service.
        """
        self.recognizer = recognizer
        self.synthesizer = synthesizer
        self.logger = logging.getLogger(self.__class__.__name__)

    def listen(self, timeout: float | None = None) -> str | None:
        """
        Listen for speech from the microphone.

        Args:
            timeout: Optional timeout in seconds.

        Returns:
            str: The recognized speech, or None if no speech was recognized.
        """
        self.logger.debug("Speech service listening")
        return self.recognizer.listen(timeout)

    def speak(self, text: str) -> None:
        """
        Speak the given text using text-to-speech synthesis.

        Args:
            text: The text to speak.
        """
        self.logger.info(f"Speech service speaking: {text[:50]}...")
        self.synthesizer.speak(text)

    def close(self) -> None:
        """
        Clean up all speech service resources.
        """
        self.logger.debug("Closing speech service")
        self.recognizer.close()
        self.synthesizer.close()
