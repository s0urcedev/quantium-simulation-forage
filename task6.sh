#!/usr/bin/env bash

set -u

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_ACTIVATE="$PROJECT_DIR/venv/bin/activate"

if [ ! -f "$VENV_ACTIVATE" ]; then
	echo "Virtual environment not found at $VENV_ACTIVATE"
	exit 1
fi

# shellcheck disable=SC1090
source "$VENV_ACTIVATE" || exit 1

pytest "$PROJECT_DIR/task5.py" -q
TEST_EXIT_CODE=$?

if [ "$TEST_EXIT_CODE" -eq 0 ]; then
	exit 0
fi

exit 1
