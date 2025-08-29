import logging
import sys


def setup_logging() -> None:
    """Setup logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def get_logger(name: str) -> logging.Logger:
    """Get a logger for the application.

    Args:
        name: The name of the logger.

    Returns:
        A logger for the application.

    """
    return logging.getLogger(name)
