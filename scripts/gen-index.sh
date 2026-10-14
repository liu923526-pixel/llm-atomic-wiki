#!/bin/bash
# Auto-generate wiki/index.md from wiki/ filenames + first-line titles.
# Compatible with macOS, Linux, and Windows
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$SCRIPT_DIR/gen_index.py" "$@"
