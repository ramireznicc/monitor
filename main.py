# main.py
import logging
import threading
import time
import socket
import platform
import datetime
from logging.handlers import RotatingFileHandler

import psutil

from system_monitor.notifier import notify, format_startup, format_shutdown, format_system_status
from system_monitor.config import (
    LOG_FILE,
    LOG_LEVEL,
    INTERVAL_SECONDS,
    STARTUP_NOTIFY_ENABLED,
    SHUTDOWN_NOTIFY_ENABLED,
)

# Send System Status to Telegram every 3 minutes
STATUS_PUSH_INTERVAL_SECONDS = 180  # TODO: make configurable via .env later


def setup_file_logging() -> None:
    """
    Configure logging to write only to a rotating file defined by config.LOG_FILE.
    No console output.
    """
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    # Remove any existing handlers (console, etc.)
    for h in list(logger.handlers):
        logger.removeHandler(h)

    # Rotating file handler (5 MB max, keep 3 backups)
    file_handler = RotatingFileHandler(
        str(LOG_FILE),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def _uptime_str() -> str:
    boot = datetime.datetime.fromtimestamp(psutil.boot_time())
    delta = datetime.datetime.now() - boot
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, _ = divmod(rem, 60)
    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    return " ".join(parts) or "0m"


def startup_sequence():
    if STARTUP_NOTIFY_ENABLED:
        hostname = socket.gethostname()
        os_pretty = f"{platform.system()} {platform.release()}"
        uptime = _uptime_str()
        # Interval displayed for logging info only
        notify(format_startup(hostname, os_pretty, uptime, INTERVAL_SECONDS))

    # Immediately send first System Status after startup
    notify(format_system_status())


def logging_worker(stop_event: threading.Event):
    """
    Keeps logging system metrics every INTERVAL_SECONDS.
    This does not send Telegram messages, only logs to file.
    """
    while not stop_event.is_set():
        try:
            cpu = psutil.cpu_percent(interval=0.0)
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            logging.info(
                "System metrics | CPU: %.1f%% | RAM: %.1f%% | Disk: %.1f%%",
                cpu, mem.percent, disk.percent
            )
        except Exception as exc:
            logging.exception(f"Metrics logging error: {exc}")

        for _ in range(INTERVAL_SECONDS):
            if stop_event.is_set():
                break
            time.sleep(1)


def telegram_status_worker(stop_event: threading.Event):
    """
    Sends System Status to Telegram every STATUS_PUSH_INTERVAL_SECONDS.
    """
    # Already sent one at startup
    while not stop_event.is_set():
        for _ in range(STATUS_PUSH_INTERVAL_SECONDS):
            if stop_event.is_set():
                return
            time.sleep(1)

        try:
            notify(format_system_status())
        except Exception as exc:
            logging.exception(f"Telegram status push error: {exc}")


def main():
    setup_file_logging()  # logs only go to file (no console printing)

    stop_event = threading.Event()

    try:
        startup_sequence()

        t_log = threading.Thread(target=logging_worker, args=(stop_event,), daemon=True)
        t_push = threading.Thread(target=telegram_status_worker, args=(stop_event,), daemon=True)

        t_log.start()
        t_push.start()

        # Keep main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Interrupted by user, shutting down...")
    finally:
        stop_event.set()
        time.sleep(0.5)
        # Shutdown notification safely handled
        try:
            if SHUTDOWN_NOTIFY_ENABLED:
                hostname = socket.gethostname()
                notify(format_shutdown(hostname))
        except Exception as exc:
            logging.exception(f"Shutdown notification failed: {exc}")


if __name__ == "__main__":
    main()