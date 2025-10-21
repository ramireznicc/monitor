import time
import logging
import psutil
from datetime import datetime
from pathlib import Path

# Define log directory and file
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "monitor.log"

# Configure logging format and level
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def snapshot():
    """
    Take a snapshot of current system usage (CPU, Memory, Disk).
    Returns:
        tuple: (cpu_percent, mem_percent, disk_percent)
    """
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    return cpu, mem, disk

def main():
    """
    Main monitoring loop.
    Logs system metrics every 10 seconds until interrupted.
    """

    logging.info("System Monitor started")
    try:
        while True:
            cpu, mem, disk = snapshot()
            logging.info(f"CPU={cpu}% MEM={mem}% DISK={disk}%")
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("System Monitor paused")
        logging.info("")

if __name__ == "__main__":
    main()
