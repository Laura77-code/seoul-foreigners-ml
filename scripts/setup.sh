#!/usr/bin/env bash
set -e

echo "== Seoul Foreigners ML setup =="

if ! command -v python >/dev/null 2>&1; then
  echo "Python was not found. Install Python 3.10+ and try again."
  exit 1
fi

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

if [ -f ".venv/Scripts/activate" ]; then
  source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
else
  echo "Virtual environment activation script not found."
  exit 1
fi

python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .

echo "Setup complete."
