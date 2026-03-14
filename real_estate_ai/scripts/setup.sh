#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$PROJECT_DIR/../.venv/bin/python"

if [[ ! -x "$VENV_PY" ]]; then
  echo "Python venv not found at $VENV_PY"
  echo "Create it first from workspace root: python3 -m venv .venv"
  exit 1
fi

"$VENV_PY" -m pip install --upgrade pip
"$VENV_PY" -m pip install -r "$PROJECT_DIR/requirements.txt"

echo "Dependencies installed in virtual environment."
