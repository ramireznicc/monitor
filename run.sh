#!/usr/bin/env bash
set -euo pipefail

# Change directory to the project root
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"

# Create virtual environment if it doesn't exist
if [ ! -d .venv ]; then
  echo "[setup] Creating virtual environment..."
  "$PY" -m venv .venv
  . .venv/bin/activate
  python -m pip install -U pip wheel
  # Install dependencies if requirements.txt exists
  if [ -f requirements.txt ]; then
    pip install -r requirements.txt
  fi
else
  . .venv/bin/activate
fi

# Visual startup message
echo ""
echo "🖥️  System Monitor started"
echo "-----------------------------------------"
echo "Press [Ctrl + C] to pause monitoring"
echo "-----------------------------------------"
echo ""

# Run the monitor
python src/monitor_basic.py
