# System Monitor (with optional Telegram alerts)

A lightweight Python system monitor for Linux that collects CPU, RAM, Disk, and basic Network stats and automatically sends Telegram notifications every 180 seconds. Runs locally with a small footprint, logs to console/file, and works with a simple .env configuration.

## Requirements

- Linux
- Python 3.10+, pip, venv
- Internet (only for Telegram)
- Telegram bot token + chat ID (optional)

## Quick Start

```bash
# Clone and enter the project
git clone https://github.com/<your-username>/system-monitor.git
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
