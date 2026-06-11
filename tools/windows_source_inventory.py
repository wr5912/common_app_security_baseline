#!/usr/bin/env python3
"""Parse the Windows common application/service Markdown source list."""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceRow:
    row_id: str
    line_no: int
    section: str
    subsection: str
    service_pattern: str
    app_vendor: str
    description: str
    row_kind: str


SECTION_RE = re.compile(r"^##\s+(.+?)\s*$")
SUBSECTION_RE = re.compile(r"^###\s+(.+?)\s*$")


def strip_cell(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\[(.*?)\]\([^)]+\)", r"\1", value)
    value = value.replace("<INSTANCE>", "INSTANCE")
    value = value.replace("`", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def is_separator_row(cells: list[str]) -> bool:
    return all(re.fullmatch(r"[-:\s]+", cell or "") for cell in cells if cell is not None)


def row_kind(section: str) -> str:
    if section.startswith("1."):
        return "windows_builtin_service"
    if section.startswith("2."):
        return "windows_per_user_service"
    return "third_party_service"


def row_prefix(kind: str, subsection: str) -> str:
    if kind == "windows_builtin_service":
        return "win-builtin"
    if kind == "windows_per_user_service":
        return "win-per-user"
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", subsection).strip("-").lower()
    return "third-party-" + (slug or "service")


def parse_source(path: Path) -> list[SourceRow]:
    text = path.read_text(encoding="utf-8")
    section = ""
    subsection = ""
    rows: list[SourceRow] = []
    counters: dict[str, int] = {}

    for line_no, line in enumerate(text.splitlines(), start=1):
        section_match = SECTION_RE.match(line)
        if section_match:
            section = section_match.group(1).strip()
            subsection = ""
            continue
        subsection_match = SUBSECTION_RE.match(line)
        if subsection_match:
            subsection = subsection_match.group(1).strip()
            continue
        if not line.startswith("|"):
            continue
        cells = [strip_cell(cell) for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or is_separator_row(cells):
            continue
        first = cells[0]
        if first in {"ServiceName", "ServiceName / 模式", "模板 ServiceName"}:
            continue
        kind = row_kind(section)
        prefix = row_prefix(kind, subsection or section)
        counters[prefix] = counters.get(prefix, 0) + 1
        row_id = f"{prefix}-{counters[prefix]:03d}"
        rows.append(
            SourceRow(
                row_id=row_id,
                line_no=line_no,
                section=section,
                subsection=subsection,
                service_pattern=first,
                app_vendor=cells[1] if len(cells) > 1 else "",
                description=cells[2] if len(cells) > 2 else "",
                row_kind=kind,
            )
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse Windows common app/service source Markdown.")
    parser.add_argument("source", nargs="?", default="/tmp/windows系统上常见应用.md")
    args = parser.parse_args()
    rows = parse_source(Path(args.source))
    by_kind: dict[str, int] = {}
    for row in rows:
        by_kind[row.row_kind] = by_kind.get(row.row_kind, 0) + 1
    print(f"rows={len(rows)}")
    for kind in sorted(by_kind):
        print(f"{kind}={by_kind[kind]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
