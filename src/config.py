"""Centralized configuration and logging for mini-sidekick.

Loads environment variables via python-dotenv at import time and exposes
them as typed, named module-level constants. All other modules should
import settings from here rather than calling os.getenv directly.

Also configures the root logger to write timestamped, level-tagged,
module-tagged entries to stdout, so every agent decision and tool call
flows through a single stream.

    from config import CLAUDE_API_KEY, DB_PATH, get_logger
    log = get_logger(__name__)
"""
from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load .env into the process environment. override=False so real env vars
# (CI, container runtimes) take precedence over what's in the file.
load_dotenv(override=False)


# --- Settings ---------------------------------------------------------------

_VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(
            f"{name} is required but not set. "
            f"Add it to your .env file (see .env.example)."
        )
    return value


def _path(name: str, default: str) -> Path:
    raw = os.getenv(name) or default
    return Path(raw).expanduser().resolve()


def _log_level(name: str, default: str = "INFO") -> str:
    raw = (os.getenv(name) or default).upper()
    if raw not in _VALID_LOG_LEVELS:
        raise ValueError(
            f"{name}={raw!r} is not a valid log level. "
            f"Expected one of: {', '.join(sorted(_VALID_LOG_LEVELS))}."
        )
    return raw


CLAUDE_API_KEY: str = _require("CLAUDE_API_KEY")
DB_PATH: Path = _path("DB_PATH", "./data/sidekick.db")
CHARTS_DIR: Path = _path("CHARTS_DIR", "./charts")
LOG_LEVEL: str = _log_level("LOG_LEVEL", "INFO")

# Make sure the directories exist so downstream code can write to them
# without first-run "no such file or directory" surprises.
DB_PATH.parent.mkdir(parents=True, exist_ok=True)
CHARTS_DIR.mkdir(parents=True, exist_ok=True)


# --- Logging ----------------------------------------------------------------

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
    force=True,  # override any handlers set up by imported libraries
)

# Quiet down chatty third-party loggers so the single stream stays readable.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a logger with the given name, inheriting the root config.

    Use at module top: ``log = get_logger(__name__)``.
    """
    return logging.getLogger(name)


get_logger(__name__).info(
    "config loaded (LOG_LEVEL=%s, DB_PATH=%s, CHARTS_DIR=%s)",
    LOG_LEVEL, DB_PATH, CHARTS_DIR,
)


__all__ = [
    "CLAUDE_API_KEY",
    "DB_PATH",
    "CHARTS_DIR",
    "LOG_LEVEL",
    "get_logger",
]