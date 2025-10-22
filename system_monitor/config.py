# system_monitor/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Base directory (assumes running from project root)
BASE_DIR = Path(os.getenv("BASE_DIR", ".")).resolve()

# Logs configuration
LOG_DIR = Path(os.getenv("LOG_DIR", BASE_DIR / "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / os.getenv("LOG_FILE_NAME", "monitor.log")

# Monitoring interval for internal logging (seconds)
INTERVAL_SECONDS = int(os.getenv("INTERVAL_SECONDS", "10"))

# Thresholds (kept for future use; not used in periodic mode)
CPU_THRESHOLD = float(os.getenv("CPU_THRESHOLD", "85"))
MEM_THRESHOLD = float(os.getenv("MEM_THRESHOLD", "90"))
DISK_THRESHOLD = float(os.getenv("DISK_THRESHOLD", "90"))

# Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Telegram settings
TELEGRAM_ENABLED = os.getenv("TELEGRAM_ENABLED", "false").lower() in {"1", "true", "yes", "on"}
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
TELEGRAM_TIMEOUT_SECONDS = int(os.getenv("TELEGRAM_TIMEOUT_SECONDS", "10"))

# Alerting behavior (cooldown kept for future threshold-based alerts)
ALERT_COOLDOWN_SECONDS = int(os.getenv("ALERT_COOLDOWN_SECONDS", "300"))  # 5 minutes

# Startup/Shutdown notifications
STARTUP_NOTIFY_ENABLED = os.getenv("STARTUP_NOTIFY_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
SHUTDOWN_NOTIFY_ENABLED = os.getenv("SHUTDOWN_NOTIFY_ENABLED", "false").lower() in {"1", "true", "yes", "on"}