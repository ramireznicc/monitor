# system_monitor/notifier.py
import logging
import json
from typing import Optional

import requests

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
    except requests.RequestException as exc:
        logging.exception(f"Telegram request failed: {exc}")
        return False


def notify(message: str) -> bool:
    """
    High-level notification entry point.
    Currently routes to Telegram if enabled.
    Returns True if at least one notifier succeeded.
    """
    # In the future, we can fan-out to more channels (email, Slack, etc.)
    if TELEGRAM_ENABLED:
        return _send_telegram_message(message)
    return False


def format_alert(metric: str, value: float, threshold: float) -> str:
    """
    Format a standardized alert message for a metric exceeding its threshold.
    """
    return (
        f"⚠️ <b>System Monitor Alert</b>\n"
        f"Metric: <b>{metric}</b>\n"
        f"Value: <b>{value:.1f}%</b> (threshold: {threshold:.1f}%)"
    )