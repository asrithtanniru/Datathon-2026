#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="$PROJECT_DIR/.venv/bin/python"
export KMP_DUPLICATE_LIB_OK=TRUE

cd "$PROJECT_DIR"
"$VENV_PY" -m uvicorn backend.main:app --reload
