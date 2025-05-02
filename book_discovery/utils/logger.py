import logging
from typing import Any

def configure_logger(logger: Any) -> None:
    """Configure a logger with consistent formatting and level.
    
    Args:
        logger: The logger to configure.
    """
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    
    # Prevent log messages from propagating to the root logger
    logger.propagate = False