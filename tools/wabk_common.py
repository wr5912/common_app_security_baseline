#!/usr/bin/env python3
"""Shared parser and logging utilities for Windows App Security Baseline KB tools.

The tools intentionally keep the Markdown vault as the source of truth.
They parse:
- YAML frontmatter
- Markdown headings/sections
- Obsidian links: [[Page]], [[Page#Heading]], [[Page|Alias]]
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import logging
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

LOG = logging.getLogger("wabk")
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
MD_CODE_FENCE_RE = re.compile(r"```.*?```", re.S)
MD_INLINE_CODE_RE = re.compile(r"`([^`]+)`")


def configure_logging(debug: bool = False, log_file: str | None = None) -> None:
    level = logging.DEBUG if debug else logging.INFO
    fmt = "%(asctime)s %(levelname)-8s [%(name)s] %(message)s"
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_path, encoding="utf-8"))
    logging.basicConfig(level=level, format=fmt, handlers=handlers, force=True)
    LOG.debug("logging configured debug=%s log_file=%s", debug, log_file)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def stable_id(kind: str, value: str) -> str:
    digest = hashlib.sha1(value.encode("utf-8", errors="replace")).hexdigest()[:16]
    safe_kind = re.sub(r"[^a-zA-Z0-9_]+", "_", kind or "doc").strip("_").lower() or "doc"
    return f"{safe_kind}_{digest}"


def parse_simple_yaml(text: str) -> dict[str, Any]:
    """Small YAML fallback parser for common frontmatter patterns.

    Supports simple scalar values and indented list items. Use PyYAML in production.
    """
    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith("  - ") and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(_coerce_scalar(line.strip()[2:].strip()))
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            current_key = key
            if value == "":
                data[key] = []
            else:
                data[key] = _coerce_scalar(value)
    return data


def _coerce_scalar(value: str) -> Any:
    value = value.strip().strip('"').strip("'")
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() in {"null", "none"}:
        return None
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip('"').strip("'") for item in inner.split(",")]
    return value


def extract_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    if not content.startswith("---"):
        return {}, content
    # only split the first YAML block
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", content, flags=re.S)
    if not match:
        LOG.debug("frontmatter delimiter not closed; content treated as body")
        return {}, content
    fm_text, body = match.group(1), match.group(2)
    if yaml:
        try:
            parsed = yaml.safe_load(fm_text) or {}
            if not isinstance(parsed, dict):
                LOG.warning("frontmatter is not a mapping; fallback to empty mapping")
                parsed = {}
            return parsed, body
        except Exception as exc:
            LOG.warning("PyYAML failed to parse frontmatter: %s; fallback simple parser", exc)
    return parse_simple_yaml(fm_text), body


def extract_title(body: str, path: Path) -> str:
    for line in body.splitlines():
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) == 1:
            return match.group(2).strip()
    return path.stem


def strip_markdown(md: str) -> str:
    text = MD_CODE_FENCE_RE.sub(" ", md)
    text = MD_INLINE_CODE_RE.sub(r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^\)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^\)]*\)", r"\1", text)
    text = re.sub(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), text)
    text = re.sub(r"[#>*_\-]+", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_links(content: str) -> list[str]:
    return sorted({m.group(1).strip() for m in LINK_RE.finditer(content) if m.group(1).strip()})


def extract_link_occurrences(content: str) -> list[dict[str, Any]]:
    occurrences: list[dict[str, Any]] = []
    current_heading = ""
    for line_no, line in enumerate(content.splitlines(), start=1):
        h = HEADING_RE.match(line)
        if h:
            current_heading = h.group(2).strip()
        for m in LINK_RE.finditer(line):
            occurrences.append({
                "target_text": m.group(1).strip(),
                "raw_link": m.group(0),
                "line_no": line_no,
                "context_heading": current_heading,
                "line_text": line.strip(),
            })
    return occurrences


def extract_sections(body: str) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    buffer: list[str] = []
    order = 0
    for line in body.splitlines():
        match = HEADING_RE.match(line)
        if match:
            if current is not None:
                current["content"] = "\n".join(buffer).strip()
                current["content_text"] = strip_markdown(current["content"])
                sections.append(current)
            order += 1
            current = {
                "level": len(match.group(1)),
                "heading": match.group(2).strip(),
                "sort_order": order,
            }
            buffer = []
        else:
            buffer.append(line)
    if current is not None:
        current["content"] = "\n".join(buffer).strip()
        current["content_text"] = strip_markdown(current["content"])
        sections.append(current)
    return sections


def json_dumps(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value if v not in (None, "")]
    if isinstance(value, tuple):
        return [str(v) for v in value if v not in (None, "")]
    return [str(value)] if str(value) else []


def first_non_empty(*values: Any) -> str | None:
    for value in values:
        if value is None:
            continue
        if isinstance(value, str) and value.strip():
            return value.strip()
        if not isinstance(value, str):
            return str(value)
    return None


@dataclasses.dataclass
class Document:
    id: str
    path: str
    abs_path: Path
    title: str
    type: str
    name: str
    frontmatter: dict[str, Any]
    body: str
    body_text: str
    raw: str
    sha256: str
    mtime: str
    tags: list[str]
    aliases: list[str]
    links: list[str]
    link_occurrences: list[dict[str, Any]]
    sections: list[dict[str, Any]]


def infer_type(path: Path, fm: dict[str, Any]) -> str:
    explicit = first_non_empty(fm.get("type"))
    if explicit:
        return explicit
    parts = set(path.parts)
    if "01_应用" in parts:
        return "app"
    if "02_服务" in parts:
        return "service"
    if "03_进程" in parts:
        return "process"
    if "04_父子进程关系" in parts:
        return "process_relation"
    if "06_注册表画像" in parts:
        return "registry_pattern"
    if "07_文件与数据" in parts:
        return "file_artifact"
    if "08_网络行为" in parts:
        return "network_behavior"
    if "09_安全基线" in parts:
        return "security_baseline"
    return "document"


def infer_name(title: str, fm: dict[str, Any], doc_type: str) -> str:
    keys_by_type = {
        "app": ["app_name_cn", "app_name_en", "app_id", "name"],
        "service": ["service_name", "display_name", "name"],
        "process": ["process_name", "name"],
        "process_relation": ["relation_name", "parent_process", "child_process", "name"],
        "registry_pattern": ["key_pattern", "name"],
        "network_behavior": ["dst_domain_pattern", "name"],
    }
    for key in keys_by_type.get(doc_type, ["name"]):
        val = fm.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return title


def load_documents(vault: Path) -> list[Document]:
    LOG.info("scan markdown vault: %s", vault)
    docs: list[Document] = []
    for path in sorted(vault.rglob("*.md")):
        if any(part in {".obsidian", ".git"} for part in path.parts):
            continue
        rel = path.relative_to(vault).as_posix()
        try:
            raw = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raw = path.read_text(encoding="utf-8-sig")
        fm, body = extract_frontmatter(raw)
        title = extract_title(body, path)
        doc_type = infer_type(Path(rel), fm)
        name = infer_name(title, fm, doc_type)
        tags = as_list(fm.get("tags"))
        aliases = as_list(fm.get("aliases"))
        links = extract_links(raw)
        doc = Document(
            id=stable_id("doc", rel),
            path=rel,
            abs_path=path,
            title=title,
            type=doc_type,
            name=name,
            frontmatter=fm,
            body=body,
            body_text=strip_markdown(body),
            raw=raw,
            sha256=sha256_text(raw),
            mtime=datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).isoformat(),
            tags=tags,
            aliases=aliases,
            links=links,
            link_occurrences=extract_link_occurrences(raw),
            sections=extract_sections(body),
        )
        docs.append(doc)
        LOG.debug("loaded doc path=%s type=%s title=%s links=%d sections=%d", rel, doc.type, title, len(links), len(doc.sections))
    LOG.info("loaded %d markdown documents", len(docs))
    return docs


def build_title_index(docs: Iterable[Document]) -> dict[str, str]:
    idx: dict[str, str] = {}
    for doc in docs:
        candidates = {doc.title, doc.name, Path(doc.path).stem, *doc.aliases}
        for key in candidates:
            if key:
                idx.setdefault(key.lower(), doc.id)
    LOG.debug("built title index with %d aliases", len(idx))
    return idx


def resolve_link(target_text: str, title_index: dict[str, str]) -> str | None:
    key = target_text.strip().lower()
    if key in title_index:
        return title_index[key]
    # Obsidian link may omit extension or use folder/name; try stem.
    stem = Path(target_text).stem.lower()
    return title_index.get(stem)


def open_sqlite(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn
