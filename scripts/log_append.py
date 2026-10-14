#!/usr/bin/env python3
"""Append an entry to log.md (newest on top after header)
Usage: python3 log_append.py "Description of changes"
"""

import sys
from datetime import datetime
from pathlib import Path

def main():
    repo_root = Path(__file__).resolve().parent.parent
    log_file = repo_root / "log.md"
    date_str = datetime.now().strftime("%Y-%m-%d")
    message = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1].strip() else "（未提供變更描述）"

    header = "# Wiki Change Log\n\n"
    existing_content = ""
    if log_file.exists():
        existing_content = log_file.read_text(encoding="utf-8")
        if existing_content.startswith("# Wiki Change Log"):
            lines = existing_content.splitlines(keepends=True)
            # Find after the header title and any leading blank line
            content_start = 1
            while content_start < len(lines) and lines[content_start].strip() == "":
                content_start += 1
            body = "".join(lines[content_start:])
        else:
            body = existing_content
    else:
        body = ""

    new_entry = f"## {date_str}\n\n- {message}\n\n"
    final_text = header + new_entry + body.lstrip()

    log_file.write_text(final_text, encoding="utf-8")
    print(f"Log appended: {date_str} — {message}")

if __name__ == "__main__":
    main()
