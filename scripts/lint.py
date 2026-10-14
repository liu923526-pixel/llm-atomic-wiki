#!/usr/bin/env python3
"""Wiki Lint - Programmatic Layer
Checks 4 items: ghost links, orphan pages, format violations, outdated markers.
Outputs lint-report.md in the repo root.
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

def main():
    repo_root = Path(__file__).resolve().parent.parent
    wiki_dir = repo_root / "wiki"
    report_file = repo_root / "lint-report.md"

    errors = 0
    warnings = 0

    # Collect all wiki markdown files (exclude special files)
    ignore_files = {"index.md", "log.md", "_template.md", "README.md"}
    wiki_files = {}
    if wiki_dir.exists():
        for p in wiki_dir.glob("*.md"):
            if p.name not in ignore_files and not p.name.startswith("."):
                wiki_files[p.stem] = p

    report_lines = [
        "# Wiki Lint Report\n",
        f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
    ]

    # 1. Ghost Links
    report_lines.append("## 1. Ghost Links（指向不存在頁面的連結）\n")
    found_ghost = False
    outgoing_links = {slug: [] for slug in wiki_files}
    incoming_links = {slug: 0 for slug in wiki_files}

    link_pattern = re.compile(r"\[\[([^\]]+)\]\]")

    for slug, path in sorted(wiki_files.items()):
        try:
            content = path.read_text(encoding="utf-8")
        except Exception as e:
            continue

        matches = link_pattern.findall(content)
        for link in matches:
            target = link.split("|")[0].strip()
            outgoing_links[slug].append(target)
            if target not in wiki_files:
                report_lines.append(f"- `{slug}` → `[[{target}]]` (not found)")
                found_ghost = True
                errors += 1
            else:
                incoming_links[target] += 1

    if not found_ghost:
        report_lines.append("None.\n")
    else:
        report_lines.append("")

    # 2. Orphan Pages
    report_lines.append("## 2. Orphan Pages（沒有任何頁面連結過來的頁面）\n")
    found_orphan = False
    for slug in sorted(wiki_files.keys()):
        if incoming_links[slug] == 0:
            report_lines.append(f"- `{slug}`")
            found_orphan = True
            warnings += 1

    if not found_orphan:
        report_lines.append("None.\n")
    else:
        report_lines.append("")

    # 3. Format Violations
    report_lines.append("## 3. Format Violations（格式違規）\n")
    found_format = False
    slug_valid_pattern = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

    for slug, path in sorted(wiki_files.items()):
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            continue

        first_line = content.splitlines()[0] if content.splitlines() else ""
        if not first_line.startswith("# "):
            report_lines.append(f"- `{slug}`: first line is not `# title` → `{first_line}`")
            found_format = True
            errors += 1

        if not slug_valid_pattern.match(slug):
            report_lines.append(f"- `{slug}`: filename contains uppercase, underscore, or invalid characters")
            found_format = True
            errors += 1

    if not found_format:
        report_lines.append("None.\n")
    else:
        report_lines.append("")

    # 4. Outdated Markers
    report_lines.append("## 4. Outdated Markers（時效性用語）\n")
    found_outdated = False
    temporal_pattern = re.compile(
        r"(最新版|目前最新|currently v|latest v|just released|剛出|剛推出|截至\s*[0-9]{4})",
        re.IGNORECASE
    )

    for slug, path in sorted(wiki_files.items()):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue

        matched_lines = []
        for idx, line in enumerate(lines, start=1):
            if temporal_pattern.search(line):
                matched_lines.append(f"{idx}:{line}")

        if matched_lines:
            report_lines.append(f"### `{slug}`\n```")
            report_lines.extend(matched_lines)
            report_lines.append("```\n")
            found_outdated = True
            warnings += 1

    if not found_outdated:
        report_lines.append("None.\n")
    else:
        report_lines.append("")

    # Summary
    report_lines.append("---\n")
    report_lines.append(f"**Summary**: {errors} errors, {warnings} warnings across {len(wiki_files)} wiki pages\n")

    report_file.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Lint complete: {errors} errors, {warnings} warnings. Report: {report_file}")
    sys.exit(1 if errors > 0 else 0)

if __name__ == "__main__":
    main()
