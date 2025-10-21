#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-python3}"

[ -d .venv ] || { echo "[setup] Creating virtual environment..."; "$PY" -m venv .venv >/dev/null 2>&1; }
# shellcheck disable=SC1091
. .venv/bin/activate

python -m pip install -U pip wheel -q >/dev/null 2>&1 || true
if [ -f requirements.txt ]; then
  python -m pip install -r requirements.txt -q >/dev/null 2>&1 || {
    echo "[setup] Dependency install failed. Showing logs..."
    python -m pip install -r requirements.txt
    exit 1
  }
fi

echo ""
echo "🖥️  System Monitor started"
echo "-----------------------------------------"
echo "Press [Ctrl + C] to stop monitoring"
echo "-----------------------------------------"
echo ""

python main.py