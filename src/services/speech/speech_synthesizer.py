"""
Speech synthesis service using edge-tts.

This module provides a service for converting text into spoken audio
using edge-tts for high-quality, offline-capable text-to-speech synthesis.
"""

import asyncio
import logging
import time
from pathlib import Path

import pygame
from edge_tts import Communicate

logger = logging.getLogger(__name__)


class SpeechSynthesizer:
    """
    Service for converting text to spoken audio.

    This service uses edge-tts for text-to-speech synthesis and pygame
    for audio playback. It handles text input, synthesis, and playback
    of audio responses.
    """

    def __init__(self, cache_dir: str = "./data/speech_cache") -> None:
        """
        Initialize the speech synthesizer.

        Args:
            cache_dir: Directory to cache synthesized speech files.
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.voice = "en-US-AriaNeural"

        try:
            pygame.mixer.init()
            self.logger.info("Audio mixer initialized")
        except Exception as e:
            self.logger.warning(f"Failed to initialize audio mixer: {e}")

    def speak(self, text: str) -> None:
        """
        Convert text to speech and play it.

        This method synthesizes the given text into speech and plays it
        through the system audio. If synthesis fails, a warning is logged.

        Args:
            text: The text to convert to speech.
        """
        self.logger.info(f"Synthesizing speech for: {text[:50]}...")

        try:
            asyncio.run(self._synthesize_and_play(text))
        except Exception as e:
            self.logger.error(f"Error during speech synthesis: {e}", exc_info=True)

    async def _synthesize_and_play(self, text: str) -> None:
        """
        Asynchronously synthesize and play text.

        Args:
            text: The text to synthesize and play.
        """
        try:
            communicate = Communicate(text, self.voice)
            audio_file = self.cache_dir / f"speech_{hash(text)}.mp3"

            await communicate.save(str(audio_file))
            self.logger.debug(f"Saved synthesized audio to: {audio_file}")

            self._play_audio(audio_file)

        except Exception as e:
            self.logger.error(f"Error synthesizing speech: {e}", exc_info=True)

    def _play_audio(self, audio_file: Path) -> None:
        """
        Play an audio file using pygame.

        Args:
            audio_file: Path to the audio file to play.
        """
        try:
            self.logger.debug(f"Playing audio: {audio_file}")
            pygame.mixer.music.load(str(audio_file))
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            self.logger.debug("Audio playback completed")

        except Exception as e:
            self.logger.error(f"Error playing audio: {e}", exc_info=True)

    def close(self) -> None:
        """
        Clean up resources.

        Call this method when done with the synthesizer to ensure all
        resources are properly released.
        """
        try:
            pygame.mixer.quit()
            self.logger.debug("Audio mixer closed")
        except Exception as e:
            self.logger.warning(f"Error closing audio mixer: {e}")
