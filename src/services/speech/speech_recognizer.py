"""
Speech recognition service using Vosk.

This module provides a service for converting microphone audio into text
using the Vosk speech recognition engine with offline-first capabilities.
"""

import json
import logging
import queue
from pathlib import Path

import sounddevice as sd
from vosk import KaldiRecognizer, Model

logger = logging.getLogger(__name__)


class SpeechRecognizer:
    """
    Service for converting microphone audio to text.

    This service uses Vosk for offline speech recognition. It handles
    microphone input, audio streaming, and recognition result parsing.
    """

    def __init__(self, model_path: str) -> None:
        """
        Initialize the speech recognizer with a Vosk model.

        Args:
            model_path: Path to the Vosk model directory.

        Raises:
            FileNotFoundError: If the model path does not exist.
            Exception: If the model fails to load.
        """
        self.model_path = Path(model_path)
        self.logger = logging.getLogger(self.__class__.__name__)

        if not self.model_path.exists():
            msg = f"Model path not found: {self.model_path}"
            self.logger.error(msg)
            raise FileNotFoundError(msg)

        try:
            self.model = Model(str(self.model_path))
            self.logger.info(f"Loaded speech model from: {self.model_path}")
        except Exception as e:
            msg = f"Failed to load speech model: {e}"
            self.logger.error(msg)
            raise

        self.sample_rate = 16000
        self.chunk_size = 8192

    def listen(self, timeout: float | None = None) -> str | None:
        """
        Listen to microphone and return recognized speech.

        This method captures audio from the default microphone and processes
        it through the Vosk recognizer until speech is detected or the
        optional timeout is reached.

        Args:
            timeout: Optional timeout in seconds. If None, listens indefinitely
                     until speech is recognized.

        Returns:
            str: The recognized speech as text, or None if no speech was
                 recognized within the timeout period.
        """
        self.logger.debug("Starting speech recognition")

        audio_queue = queue.Queue()

        def audio_callback(
            indata: bytearray, frames: int, time_info, status
        ) -> None:
            """
            Callback function for audio stream.

            Args:
                indata: Audio data from microphone.
                frames: Number of frames in the audio data.
                time_info: Timing information (unused).
                status: Status flags for the stream (unused).
            """
            if status:
                self.logger.warning(f"Audio stream status: {status}")
            audio_queue.put(bytes(indata))

        rec = KaldiRecognizer(self.model, self.sample_rate)
        rec.SetWords("")

        try:
            with sd.RawInputStream(
                samplerate=self.sample_rate,
                blocksize=self.chunk_size,
                channels=1,
                dtype="int16",
                callback=audio_callback,
            ):
                self.logger.debug("Microphone stream opened with callback")

                while True:
                    data = audio_queue.get()

                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get("text", "").strip()

                        if text:
                            self.logger.info(f"Recognized: {text}")
                            return text

                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "")

                    if partial_text:
                        self.logger.debug(f"Partial: {partial_text}")

        except Exception as e:
            msg = f"Error during speech recognition: {e}"
            self.logger.error(msg, exc_info=True)
            return None

        return None

    def close(self) -> None:
        """
        Clean up resources.

        Call this method when done with the recognizer to ensure all
        resources are properly released.
        """
        self.logger.debug("Closing speech recognizer")
