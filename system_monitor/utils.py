# monitor/utils.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(log_file: Path, level: str = "INFO") -> None:
    """
    Configure logging to write only to a rotating file.
    No console output.
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    # Evitar duplicar handlers si ya está configurado
    if any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        return

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    # File handler con rotación (5 MB, mantiene 3 backups)
    file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    # Limpiar otros handlers (por si basicConfig se ejecutó en otro lado)
    logger.handlers.clear()
    logger.addHandler(file_handler)