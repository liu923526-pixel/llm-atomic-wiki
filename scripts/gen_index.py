#!/usr/bin/env python3
"""Auto-generate index.md from wiki/ filenames + first-line titles.
Auto-discovers branch prefix from filename before the first hyphen.
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Optional predefined branch display mapping:
# e.g. {"2330": "台積電 (2330)", "cpo": "CPO 共同封裝光學", "cowos": "CoWoS 先進封裝"}
BRANCH_DISPLAY_MAP = {
    "harness-engineering": "Harness Engineering",
    "mcp": "MCP",
    "ai-skills": "AI Skills",
    "vibe-coding": "Vibe Coding",
    "ai-agent": "AI Agent",
    "self-media": "Self-Media",
    "product-business": "Product & Business",
    "claude-code": "Claude Code",
    "context-engineering": "Context Engineering",
    "career-mindset": "Career & Mindset",
    "developer-workflow": "Developer Workflow",
}

def get_display_name(branch_prefix: str) -> str:
    if branch_prefix in BRANCH_DISPLAY_MAP:
        return BRANCH_DISPLAY_MAP[branch_prefix]
    # Auto capitalize words
    words = branch_prefix.replace("-", " ").split()
    return " ".join(word.capitalize() for word in words)

def main():
    repo_root = Path(__file__).resolve().parent.parent
    wiki_dir = repo_root / "wiki"
    index_file = repo_root / "index.md"

    ignore_files = {"index.md", "log.md", "_template.md", "README.md"}
    wiki_files = []
    if wiki_dir.exists():
        for p in wiki_dir.glob("*.md"):
            if p.name not in ignore_files and not p.name.startswith("."):
                wiki_files.append(p)

    wiki_files.sort(key=lambda x: x.stem)

    # Group files by branch prefix (first hyphen)
    branches = {}
    for p in wiki_files:
        slug = p.stem
        parts = slug.split("-", 1)
        branch = parts[0]
        # Check if matched multi-word predefined branch
        for predefined in BRANCH_DISPLAY_MAP:
            if slug.startswith(predefined + "-") or slug == predefined:
                branch = predefined
                break

        if branch not in branches:
            branches[branch] = []
        branches[branch].append(p)

    lines = [
        "# Wiki Index\n",
        f"> Total pages: {len(wiki_files)}",
        f"> Auto-generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
        "---\n",
    ]

    for branch, files in sorted(branches.items()):
        display = get_display_name(branch)
        lines.append(f"## {display} ({len(files)} pages)\n")
        lines.append("| Slug | Title |")
        lines.append("|------|-------|")

        for f in sorted(files, key=lambda x: x.stem):
            slug = f.stem
            try:
                first_line = f.read_text(encoding="utf-8").splitlines()[0]
                title = re.sub(r"^#\s*", "", first_line).strip()
            except Exception:
                title = slug
            lines.append(f"| [[{slug}]] | {title} |")
        lines.append("")

    index_file.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
    print(f"Index generated: {len(wiki_files)} pages → {index_file}")

if __name__ == "__main__":
    main()
