"""Reusable logger configuration for agent guardrail execution."""

from __future__ import annotations

import logging
from typing import Final

LOGGER_NAME: Final[str] = "agent_guardrails"


def get_logger(name: str = LOGGER_NAME) -> logging.Logger:
    """Return a configured logger for the package.

    The logger is initialized once with a simple stream handler and a compact
    formatter that keeps operational logs readable.
    """

    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.propagate = False
    return logger

