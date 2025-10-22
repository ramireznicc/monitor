# system_monitor/utils.py
import logging
import platform
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

import psutil


def setup_logging(log_file: Path, level: str = "INFO") -> None:
    """
    Configure root logger to write only to a rotating file.
    - No console output.
    - Rotation: 5 MB per file, keep 3 backups.
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    # Remove any existing handlers to avoid duplicates
    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def get_hostname() -> str:
    """
    Return the current machine hostname.
    """
    return platform.node() or "unknown-host"


def get_os_pretty() -> str:
    """
    Return a human-friendly OS string (e.g., 'Linux Fedora 40 (Linux-6.10.x)').
    """
    dist = platform.platform()
    system = platform.system()
    release = platform.release()
    return f"{system} {release} ({dist})"


def get_uptime_human() -> str:
    """
    Return system uptime in a human-friendly format (e.g., '2d 3h 15m').
    """
    boot_ts = getattr(psutil, "boot_time", lambda: time.time())()
    seconds = int(time.time() - boot_ts)

    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours or days:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)