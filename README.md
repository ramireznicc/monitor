
# System Monitor (with optional Telegram alerts)

A lightweight Python system monitor for Linux that collects CPU, RAM, Disk, and basic Network stats and automatically sends Telegram notifications every 180 seconds. Runs locally with a small footprint, logs to console/file, and works with a simple .env configuration.




## Requirements

- Linux
- Python 3.10+, pip, venv
- Internet (only for Telegram)
- Telegram bot token + chat ID (optional)
## Quick Start

``` bash
# Clone and enter the project
git clone https://github.com/ramireznicc/monitor.git
cd system-monitor

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create your config
cp .env.example .env
# Edit .env and set your values (optional for Telegram)
```

Run:
```bash
python main.py
# Or
chmod +x run.sh && ./run.sh
```

Notes:

- Debian/Ubuntu: if venv is missing → sudo apt-get install -y python3-venv
- Arch/Manjaro: if needed → sudo pacman -S python-virtualenv
- Fedora usually has venv by default

## Configuration

Minimal example:
```bash
# Telegram (optional)
TELEGRAM_BOT_TOKEN=123456:ABC...     # from @BotFather
TELEGRAM_CHAT_ID=123456789           # your chat id or a group id (-100...)

# Thresholds
CPU_THRESHOLD=85
RAM_THRESHOLD=85
DISK_THRESHOLD=90
NET_TX_THRESHOLD_MBPS=200
NET_RX_THRESHOLD_MBPS=200

# Check interval (seconds)
CHECK_INTERVAL_SECONDS=5

# Logging
LOG_TO_FILE=true
LOG_FILE=monitor.log
LOG_LEVEL=INFO
```

If you don’t set TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID, the monitor runs without Telegram alerts and logs locally.


## Project Structure
```text
├── .gitignore
├── README.md
├── main.py
├── requirements.txt
├── run.sh
└── system_monitor/
    ├── __init__.py
    ├── config.py
    ├── notifier.py
    ├── system_checker.py
    └── utils.py
```