import logging
import os

def configure_logging(log_level: str = "INFO", log_file: str = None):
    """
    Configure structured logging for the application.
    """
    log_level = getattr(logging, log_level.upper(), logging.INFO)
    handlers = [logging.StreamHandler()]

    if log_file:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers
    )
