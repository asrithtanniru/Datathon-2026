#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$PROJECT_DIR/../.venv/bin/python"
PER_CLASS="${1:-120}"

cd "$PROJECT_DIR"
"$VENV_PY" training/download_kaggle_subset.py --per-class "$PER_CLASS" --clean
