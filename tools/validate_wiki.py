#!/usr/bin/env python3
"""Validate Markdown KB structure before release."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

try:
    from .audit_obsidian_links import build_report as build_link_report
    from .wabk_common import Document, build_title_index, load_documents, resolve_link
except ImportError:  # allow running as: python tools/validate_wiki.py
    from audit_obsidian_links import build_report as build_link_report
    from wabk_common import Document, build_title_index, load_documents, resolve_link


ALLOWED_TYPES = {
    "agent_schema",
    "app",
    "changelog",
    "config_persistence",
    "extract_spec",
    "file_artifact",
    "index",
    "network_behavior",
    "overview",
    "process",
    "process_relation",
    "raw_sources_readme",
    "readme",
    "registry_pattern",
    "security_baseline",
    "service",
    "source_evidence",
    "startup_method",
    "todo",
    "workflow",
}

PROFILE_TYPES = {
    "app",
    "config_persistence",
    "file_artifact",
    "network_behavior",
    "process",
    "process_relation",
    "registry_pattern",
    "security_baseline",
    "service",
    "source_evidence",
    "startup_method",
}

INDEX_BY_TYPE = {
    "app": "00_总览/应用分类索引.md",
    "config_persistence": "00_总览/Linux持久化与配置索引.md",
    "file_artifact": "00_总览/文件与数据索引.md",
    "network_behavior": "00_总览/网络行为索引.md",
    "process": "00_总览/进程分类索引.md",
    "process_relation": "00_总览/高风险父子进程关系索引.md",
    "registry_pattern": "00_总览/注册表关键位置索引.md",
    "security_baseline": "00_总览/安全基线索引.md",
    "service": "00_总览/服务分类索引.md",
    "startup_method": "00_总览/启动方式索引.md",
}

VALID_OS = {"windows", "linux", "cross"}
CHANGELOG_PATH = "logs/变更日志.md"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Markdown KB structure.")
    parser.add_argument("--vault", default="kb", help="Knowledge-base vault root")
    parser.add_argument("--out-json", default=None, help="Write validation report JSON")
    parser.add_argument("--fail", action="store_true", help="Exit non-zero if validation issues exist")
    return parser.parse_args(argv)


def frontmatter_block(path: Path) -> tuple[str | None, str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None, "missing_frontmatter"
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, flags=re.S)
    if not match:
        return None, "unclosed_frontmatter"
    return match.group(1), None


def validate_frontmatter(vault: Path) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for path in sorted(vault.rglob("*.md")):
        rel = path.relative_to(vault).as_posix()
        block, error = frontmatter_block(path)
        if error:
            issues.append({"path": rel, "reason": error})
            continue
        if yaml is None:
            continue
        try:
            parsed = yaml.safe_load(block or "")
        except Exception as exc:
            issues.append({"path": rel, "reason": "yaml_parse_error", "detail": str(exc)})
            continue
        if not isinstance(parsed, dict):
            issues.append({"path": rel, "reason": "frontmatter_not_mapping"})
    return issues


def validate_enums(docs: list[Document]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    for doc in docs:
        if doc.type not in ALLOWED_TYPES:
            issues.append({"path": doc.path, "reason": "unknown_type", "type": doc.type})
        if doc.type in PROFILE_TYPES and doc.os not in VALID_OS:
            issues.append({"path": doc.path, "reason": "invalid_or_missing_os", "os": doc.os})
    return issues


def index_doc_ids(index_doc: Document, title_index: dict[str, str]) -> set[str]:
    doc_ids: set[str] = set()
    for target in index_doc.links:
        doc_id = resolve_link(target, title_index)
        if doc_id:
            doc_ids.add(doc_id)
    return doc_ids


def validate_indexes(docs: list[Document]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    by_path = {doc.path: doc for doc in docs}
    title_index = build_title_index(docs)
    resolved_by_type: dict[str, set[str]] = {}
    for doc_type, index_path in INDEX_BY_TYPE.items():
        index_doc = by_path.get(index_path)
        if not index_doc:
            issues.append({"path": index_path, "reason": "missing_index"})
            continue
        resolved_by_type[doc_type] = index_doc_ids(index_doc, title_index)
    for doc in docs:
        if doc.path.startswith("99_模板/") or doc.type not in INDEX_BY_TYPE:
            continue
        if doc.id not in resolved_by_type.get(doc.type, set()):
            issues.append({"path": doc.path, "reason": "missing_index_entry", "index": INDEX_BY_TYPE[doc.type]})
    return issues


def validate_changelog(docs: list[Document]) -> list[dict[str, Any]]:
    by_path = {doc.path: doc for doc in docs}
    changelog = by_path.get(CHANGELOG_PATH)
    if not changelog:
        return [{"path": CHANGELOG_PATH, "reason": "missing_changelog"}]
    if not re.search(r"^## \d{4}-\d{2}-\d{2} \| ", changelog.raw, flags=re.M):
        return [{"path": CHANGELOG_PATH, "reason": "missing_dated_changelog_entry"}]
    return []


def build_validation_report(vault: Path) -> dict[str, Any]:
    docs = load_documents(vault)
    link_report = build_link_report(vault)
    issue_groups = {
        "frontmatter": validate_frontmatter(vault),
        "enums": validate_enums(docs),
        "links": link_report["issues"],
        "duplicate_link_targets": link_report["duplicate_target_keys"],
        "indexes": validate_indexes(docs),
        "changelog": validate_changelog(docs),
    }
    issue_counts = {name: len(items) for name, items in issue_groups.items()}
    return {
        "vault": str(vault),
        "documents": len(docs),
        "issue_counts": issue_counts,
        "issue_count": sum(issue_counts.values()),
        "issues": issue_groups,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = build_validation_report(Path(args.vault))
    if args.out_json:
        out = Path(args.out_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str), encoding="utf-8")
    print(
        "documents={documents} issues={issue_count} counts={counts}".format(
            documents=report["documents"],
            issue_count=report["issue_count"],
            counts=json.dumps(report["issue_counts"], ensure_ascii=False, sort_keys=True),
        )
    )
    return 1 if args.fail and report["issue_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
