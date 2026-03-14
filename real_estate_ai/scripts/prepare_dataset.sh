#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$PROJECT_DIR/../.venv/bin/python"

cd "$PROJECT_DIR"
"$VENV_PY" training/prepare_dataset.py
