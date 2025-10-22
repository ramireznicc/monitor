# system_monitor/notifier.py
import logging
import psutil

from system_monitor.config import (
    TELEGRAM_ENABLED,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    TELEGRAM_TIMEOUT_SECONDS,
)


def _send_telegram_message(text: str) -> bool:
    """
    Send a plain text message to a Telegram chat using the Bot API.
    Returns True on success, False otherwise.
    """
    if not TELEGRAM_ENABLED:
        return False

    # Lazy import to avoid hard dependency when Telegram is disabled
    try:
        import requests  # type: ignore
    except Exception:
        logging.error("Telegram enabled but 'requests' is not installed")
        return False

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logging.error("Telegram is enabled but BOT_TOKEN or CHAT_ID is not set")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    try:
        import requests  # type: ignore
        resp = requests.post(url, json=payload, timeout=TELEGRAM_TIMEOUT_SECONDS)
        if resp.status_code == 200:
            return True
        else:
            logging.error(
                "Telegram API error: status=%s, body=%s",
                resp.status_code,
                resp.text[:500],
            )
            return False
    except Exception as exc:
        logging.exception(f"Telegram request failed: {exc}")
        return False


def notify(message: str) -> bool:
    """
    High-level notification entry point.
    Currently routes to Telegram if enabled.
    Returns True if at least one notifier succeeded.
    """
    if TELEGRAM_ENABLED:
        return _send_telegram_message(message)
    return False


def _severity_emoji(percent: float) -> str:
    """
    Return an emoji representing severity based on usage percentage.
    - 0-50% -> green
    - 51-75% -> yellow
    - 76-100% -> red
    """
    if percent <= 50:
        return "🟢"
    if percent <= 75:
        return "🟡"
    return "🔴"


def _format_gb(bytes_val: int) -> str:
    """Return bytes as a string in GB with 2 decimals."""
    return f"{bytes_val / (1024**3):.2f} GB"


def format_system_status() -> str:
    """
    Build a clean System Status message with CPU, Memory and Disk info.
    No thresholds, purely periodic status snapshot.
    """
    # CPU info
    cpu_logical = psutil.cpu_count(logical=True) or 0
    cpu_physical = psutil.cpu_count(logical=False) or 0
    cpu_freq = psutil.cpu_freq()
    cpu_freq_current = f"{(cpu_freq.current/1000):.2f} GHz" if cpu_freq and cpu_freq.current else "N/A"
    cpu_usage = psutil.cpu_percent(interval=0.0)

    # Memory & Disk
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    # Severities
    mem_sev = _severity_emoji(mem.percent)
    cpu_sev = _severity_emoji(cpu_usage)
    disk_sev = _severity_emoji(disk.percent)

    return (
        f"📊 <b>System Status</b>\n\n"
        f"💻 <b>CPU</b>\n"
        f"• Cores (Logical/Physical): {cpu_logical}/{cpu_physical}\n"
        f"• Current Frequency: {cpu_freq_current}\n"
        f"• Usage: {cpu_sev} {cpu_usage:.1f}%\n\n"
        f"💾 <b>Memory (RAM)</b>\n"
        f"• Total: {_format_gb(mem.total)}\n"
        f"• Used: {_format_gb(mem.used)}\n"
        f"• Usage: {mem_sev} {mem.percent:.1f}%\n\n"
        f"💿 <b>Disk (/)</b>\n"
        f"• Total: {_format_gb(disk.total)}\n"
        f"• Used: {_format_gb(disk.used)}\n"
        f"• Usage: {disk_sev} {disk.percent:.1f}%"
    )


def format_startup(hostname: str, os_pretty: str, uptime: str, interval_s: int) -> str:
    """
    Format the startup message with system info and runtime settings.
    """
    return (
        "✅ <b>System Monitor started</b>\n"
        f"Host: <b>{hostname}</b>\n"
        f"OS: {os_pretty}\n"
        f"Uptime: {uptime}\n"
        f"Interval: {interval_s}s\n"
    )


def format_shutdown(hostname: str) -> str:
    """
    Format the shutdown message.
    """
    return f"🛑 <b>System Monitor stopped</b>\nHost: <b>{hostname}</b>"