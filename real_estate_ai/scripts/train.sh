#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$PROJECT_DIR/../.venv/bin/python"
EPOCHS="${1:-4}"
BATCH_SIZE="${2:-8}"

cd "$PROJECT_DIR"
"$VENV_PY" training/train_classifier.py --epochs "$EPOCHS" --batch-size "$BATCH_SIZE"
