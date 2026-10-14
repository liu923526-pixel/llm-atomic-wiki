#!/bin/bash
# Wiki Lint - Programmatic Layer
# Compatible with macOS, Linux, and Windows
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/lint.py" "$@"
