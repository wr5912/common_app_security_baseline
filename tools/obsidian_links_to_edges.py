#!/usr/bin/env python3
"""Extract Obsidian links from Markdown pages as simple graph edges.

Usage:
  python tools/obsidian_links_to_edges.py /path/to/vault > edges.csv
"""
from __future__ import annotations

import csv
import re
import sys
import signal
from pathlib import Path


def main() -> None:
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')
    writer = csv.DictWriter(sys.stdout, fieldnames=['source_path', 'source_title', 'target_title', 'edge_type'])
    writer.writeheader()
    for path in sorted(root.rglob('*.md')):
        if '.obsidian' in path.parts:
            continue
        content = path.read_text(encoding='utf-8')
        title = path.stem
        for line in content.splitlines():
            if line.startswith('# '):
                title = line[2:].strip()
                break
        links = sorted(set(re.findall(r'\[\[([^\]|#]+)', content)))
        for target in links:
            writer.writerow({
                'source_path': str(path.relative_to(root)),
                'source_title': title,
                'target_title': target.strip(),
                'edge_type': 'LINKS_TO',
            })


if __name__ == '__main__':
    main()
