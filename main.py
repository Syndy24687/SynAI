"""
SynAI Application Entry Point.

This module serves as the single entry point for the SynAI desktop assistant.
It handles application initialization, logging setup, and execution of either
the interactive CLI or voice mode.
"""

import argparse
import logging
import sys

from src.core.app import create_app
from src.utils.logging import configure_logging

logger = logging.getLogger(__name__)


def run_cli_loop(app) -> int:
    """
    Run the interactive command-line interface.

    Prompts the user for input, dispatches commands through the orchestrator,
    and displays responses. Exits when the user types "exit" or "quit".

    Args:
        app: The SynAI application instance.

    Returns:
        int: Exit code (0 for success).
    """
    print(f"Welcome to {app.settings.app_name}!")
    print("Type 'exit' or 'quit' to exit.\n")

    exit_commands = {"exit", "quit"}

    while True:
        try:
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in exit_commands:
                print(f"Goodbye! Thanks for using {app.settings.app_name}.")
                logger.info("User exited the application")
                break

            response = app.execute_command(user_input)
            print(f"\nSynAI: {response}\n")

        except KeyboardInterrupt:
            print(f"\n\nGoodbye! Thanks for using {app.settings.app_name}.")
            logger.info("User interrupted the application")
            break
        except Exception as e:
            print(f"Error: {e}")
            logger.error(f"Error in CLI loop: {e}", exc_info=True)

    return 0


def run_voice_loop(app) -> int:
    """
    Run the interactive voice mode.

    Continuously listens for speech, converts it to text, sends it to the
    orchestrator, and speaks the response. Exits when the user says "exit"
    or "quit" or on interrupt.

    Args:
        app: The SynAI application instance.

    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    if not app.has_speech_service():
        print("Error: Speech service is not available.")
        print("Please ensure vosk, sounddevice, edge-tts, and pygame are installed.")
        logger.error("Speech service not available in voice mode")
        return 1

    print(f"Welcome to {app.settings.app_name} Voice Mode!")
    print("Say 'exit' or 'quit' to exit.\n")

    exit_commands = {"exit", "quit"}
    listening = True

    while listening:
        try:
            print("Listening...")
            logger.debug("Starting voice recognition")

            recognized_text = app.listen(timeout=None)

            if recognized_text is None:
                print("Sorry, I didn't catch that. Please try again.\n")
                logger.warning("No speech recognized")
                continue

            print(f"You: {recognized_text}\n")
            logger.info(f"User said: {recognized_text}")

            if recognized_text.lower() in exit_commands:
                print(f"Goodbye! Thanks for using {app.settings.app_name}.")
                logger.info("User exited voice mode")
                break

            response = app.execute_command(recognized_text)
            print(f"SynAI: {response}\n")

            try:
                app.speak(response)
            except Exception as e:
                print(f"Error speaking response: {e}")
                logger.error(f"Error speaking response: {e}", exc_info=True)

        except KeyboardInterrupt:
            print(f"\n\nGoodbye! Thanks for using {app.settings.app_name}.")
            logger.info("User interrupted voice mode")
            listening = False
        except Exception as e:
            print(f"Error: {e}")
            logger.error(f"Error in voice loop: {e}", exc_info=True)

    return 0


def main() -> int:
    """
    Main entry point for the SynAI application.

    This function performs the following operations:
    1. Parses command-line arguments
    2. Configures logging
    3. Creates and initializes the application
    4. Runs either CLI or voice mode based on arguments
    5. Handles graceful shutdown

    Returns:
        int: Exit code (0 for success, 1 for error).
    """
    parser = argparse.ArgumentParser(
        description="SynAI - Offline-first desktop AI assistant"
    )
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Run in voice mode instead of CLI mode",
    )

    args = parser.parse_args()

    try:
        configure_logging()

        app = create_app()
        app.startup()

        if args.voice:
            logger.info("Starting SynAI in voice mode")
            return run_voice_loop(app)
        else:
            logger.info("Starting SynAI in CLI mode")
            return run_cli_loop(app)

    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
