# main.py
import time
import logging
import signal
import sys
from typing import Dict

from system_monitor.config import (
    LOG_FILE,
    LOG_LEVEL,
    INTERVAL_SECONDS,
    CPU_THRESHOLD,
    MEM_THRESHOLD,
    DISK_THRESHOLD,
    ALERT_COOLDOWN_SECONDS,
    TELEGRAM_ENABLED,
)
from system_monitor.utils import setup_logging
from system_monitor.system_checker import snapshot
from system_monitor.notifier import notify, format_alert

RUNNING = True
_last_alert_ts: Dict[str, float] = {}


def handle_signal(signum, frame):
    """
    Signal handler to stop the monitoring loop gracefully without extra logs.
    """
    global RUNNING
    RUNNING = False


def _should_alert(metric: str, now: float) -> bool:
    """
    Decide if we can send an alert for a given metric based on cooldown.
    """
    last = _last_alert_ts.get(metric, 0.0)
    if now - last >= ALERT_COOLDOWN_SECONDS:
        _last_alert_ts[metric] = now
        return True
    return False


def main():
    """
    Entry point for the System Monitor.
    - Sets up file-based logging.
    - Registers signal handlers for graceful shutdown.
    - Periodically logs system metrics (CPU, Memory, Disk).
    - Emits alerts (log WARNING and optional Telegram) when thresholds are exceeded,
      with a per-metric cooldown to prevent spam.
    """
    setup_logging(LOG_FILE, LOG_LEVEL)
    logging.info("System Monitor started")

    # Register signal handlers for a clean shutdown (Ctrl+C, SIGTERM)
    signal.signal(signal.SIGINT, handle_signal)   # Ctrl+C
    signal.signal(signal.SIGTERM, handle_signal)  # Service stop/kill

    try:
        while RUNNING:
            cpu, mem, disk = snapshot()
            logging.info(f"CPU={cpu}% MEM={mem}% DISK={disk}%")

            now = time.time()

            if cpu > CPU_THRESHOLD and _should_alert("CPU", now):
                msg = f"CPU high: {cpu:.1f}% (threshold {CPU_THRESHOLD:.1f}%)"
                logging.warning(msg)
                if TELEGRAM_ENABLED:
                    notify(format_alert("CPU", cpu, CPU_THRESHOLD))

            if mem > MEM_THRESHOLD and _should_alert("MEM", now):
                msg = f"Memory high: {mem:.1f}% (threshold {MEM_THRESHOLD:.1f}%)"
                logging.warning(msg)
                if TELEGRAM_ENABLED:
                    notify(format_alert("Memory", mem, MEM_THRESHOLD))

            if disk > DISK_THRESHOLD and _should_alert("DISK", now):
                msg = f"Disk usage high: {disk:.1f}% (threshold {DISK_THRESHOLD:.1f}%)"
                logging.warning(msg)
                if TELEGRAM_ENABLED:
                    notify(format_alert("Disk", disk, DISK_THRESHOLD))

            time.sleep(INTERVAL_SECONDS)
    except Exception as e:
        # Log unexpected exceptions and exit with non-zero status
        logging.exception(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        logging.info("System Monitor stopped")
        logging.info("")


if __name__ == "__main__":
    main()