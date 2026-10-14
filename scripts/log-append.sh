#!/bin/bash
# Append an entry to wiki/log.md
# Compatible with macOS, Linux, and Windows
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/log_append.py" "$@"
