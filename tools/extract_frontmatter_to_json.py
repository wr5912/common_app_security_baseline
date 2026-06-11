#!/usr/bin/env python3
"""Extract YAML frontmatter from this Obsidian vault into JSONL.

Usage:
  python tools/extract_frontmatter_to_json.py /path/to/vault > pages.jsonl

This script intentionally has minimal dependencies. If PyYAML is unavailable,
it falls back to a simple line parser for common scalar/array patterns.
"""
from __future__ import annotations

import json
import re
import sys
import signal
from pathlib import Path

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None


def parse_simple_yaml(text: str) -> dict:
    data: dict[str, object] = {}
    current_key: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith('#'):
            continue
        if line.startswith('  - ') and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(line.strip()[2:].strip('"'))
            continue
        if ':' in line and not line.startswith(' '):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            if not value:
                data[key] = []
            elif value in {'true', 'false'}:
                data[key] = value == 'true'
            else:
                data[key] = value.strip('"')
    return data


def extract_frontmatter(content: str) -> tuple[dict, str]:
    if not content.startswith('---'):
        return {}, content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    fm_text = parts[1].strip()
    body = parts[2]
    if yaml:
        parsed = yaml.safe_load(fm_text) or {}
    else:
        parsed = parse_simple_yaml(fm_text)
    return parsed, body


def extract_links(content: str) -> list[str]:
    links = re.findall(r'\[\[([^\]|#]+)', content)
    return sorted(set(link.strip() for link in links if link.strip()))


def main() -> None:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    for path in sorted(root.rglob('*.md')):
        if '.obsidian' in path.parts:
            continue
        content = path.read_text(encoding='utf-8')
        fm, body = extract_frontmatter(content)
        title = None
        for line in body.splitlines():
            if line.startswith('# '):
                title = line[2:].strip()
                break
        record = {
            'path': str(path.relative_to(root)),
            'title': title or path.stem,
            'type': fm.get('type'),
            'frontmatter': fm,
            'links': extract_links(content),
        }
        print(json.dumps(record, ensure_ascii=False))


if __name__ == '__main__':
    main()
