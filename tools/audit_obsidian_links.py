#!/usr/bin/env python3
"""Audit Obsidian links against real note names and aliases.

The normal SQLite/Neo4j extractors resolve links through document titles, which
is useful for graph construction but too permissive for Obsidian navigation.
This audit treats a link as valid only when it resolves to an existing file
stem/path or to a declared YAML alias.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    from .wabk_common import Document, build_title_index, load_documents, resolve_link
except ImportError:  # allow running as: python tools/audit_obsidian_links.py
    from wabk_common import Document, build_title_index, load_documents, resolve_link


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit Obsidian links by filename/path/alias resolution.")
    parser.add_argument("--vault", default="kb", help="Knowledge-base vault root")
    parser.add_argument("--out-md", default=None, help="Write Markdown report")
    parser.add_argument("--out-json", default=None, help="Write JSON report")
    parser.add_argument("--fail", action="store_true", help="Exit non-zero if any link issue exists")
    return parser.parse_args(argv)


def doc_target_keys(doc: Document) -> set[str]:
    rel_without_suffix = Path(doc.path).with_suffix("").as_posix()
    keys = {rel_without_suffix, Path(doc.path).stem}
    keys.update(str(alias).strip() for alias in doc.aliases if str(alias).strip())
    return {key.strip().lower() for key in keys if key.strip()}


def link_target_keys(target_text: str) -> set[str]:
    target = target_text.strip()
    if not target:
        return set()
    keys = {target}
    if "/" in target:
        keys.add(Path(target).name)
    if target.endswith(".md"):
        without_suffix = Path(target).with_suffix("").as_posix()
        keys.add(without_suffix)
        keys.add(Path(without_suffix).name)
    return {key.strip().lower() for key in keys if key.strip()}


def build_strict_index(docs: list[Document]) -> tuple[dict[str, set[str]], list[dict[str, Any]]]:
    index: dict[str, set[str]] = defaultdict(set)
    by_id = {doc.id: doc for doc in docs}
    for doc in docs:
        for key in doc_target_keys(doc):
            index[key].add(doc.id)

    duplicates: list[dict[str, Any]] = []
    for key, doc_ids in sorted(index.items()):
        if len(doc_ids) <= 1:
            continue
        duplicates.append(
            {
                "target_key": key,
                "documents": [
                    {"title": by_id[doc_id].title, "path": by_id[doc_id].path, "type": by_id[doc_id].type}
                    for doc_id in sorted(doc_ids, key=lambda item: by_id[item].path)
                ],
            }
        )
    return index, duplicates


def issue_reason(target_text: str, target_doc: Document | None, status: str) -> str:
    parts: list[str] = []
    if "->" in target_text:
        parts.append("arrow_relation")
    if "/" in target_text:
        parts.append("slash_in_target")
    if "*" in target_text:
        parts.append("asterisk_in_target")
    if target_doc and Path(target_doc.path).stem != target_text:
        parts.append("stem_title_mismatch")
    if status == "unresolved":
        parts.append("unresolved")
    if status == "ambiguous":
        parts.append("ambiguous")
    return "+".join(parts) if parts else status


def build_report(vault: Path) -> dict[str, Any]:
    docs = load_documents(vault)
    by_id = {doc.id: doc for doc in docs}
    title_index = build_title_index(docs)
    strict_index, duplicate_target_keys = build_strict_index(docs)

    strict_resolved = 0
    issues: list[dict[str, Any]] = []
    for doc in docs:
        for occurrence in doc.link_occurrences:
            target_text = occurrence["target_text"].strip()
            matched_doc_ids: set[str] = set()
            for key in link_target_keys(target_text):
                matched_doc_ids.update(strict_index.get(key, set()))

            if len(matched_doc_ids) == 1:
                strict_resolved += 1
                continue

            if len(matched_doc_ids) > 1:
                status = "ambiguous"
                target_doc = None
            else:
                loose_doc_id = resolve_link(target_text, title_index)
                target_doc = by_id.get(loose_doc_id) if loose_doc_id else None
                status = "title_only" if target_doc else "unresolved"

            issues.append(
                {
                    "status": status,
                    "reason": issue_reason(target_text, target_doc, status),
                    "source_title": doc.title,
                    "source_type": doc.type,
                    "source_path": doc.path,
                    "line_no": occurrence.get("line_no"),
                    "raw_link": occurrence.get("raw_link"),
                    "target_text": target_text,
                    "target_title": target_doc.title if target_doc else None,
                    "target_type": target_doc.type if target_doc else None,
                    "target_path": target_doc.path if target_doc else None,
                    "context_heading": occurrence.get("context_heading"),
                    "line_text": occurrence.get("line_text"),
                }
            )

    by_status = Counter(item["status"] for item in issues)
    by_reason = Counter(item["reason"] for item in issues)
    by_source_type = Counter(item["source_type"] for item in issues)
    by_target_type = Counter(item["target_type"] or "unresolved" for item in issues)
    return {
        "vault": str(vault),
        "documents": len(docs),
        "strict_resolved": strict_resolved,
        "issue_count": len(issues),
        "duplicate_target_key_count": len(duplicate_target_keys),
        "by_status": dict(sorted(by_status.items())),
        "by_reason": dict(by_reason.most_common()),
        "by_source_type": dict(by_source_type.most_common()),
        "by_target_type": dict(by_target_type.most_common()),
        "duplicate_target_keys": duplicate_target_keys,
        "issues": issues,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Obsidian 严格双链审计",
        "",
        f"- Vault：`{report['vault']}`",
        f"- 文档数：{report['documents']}",
        f"- 严格已解析链接：{report['strict_resolved']}",
        f"- 问题链接：{report['issue_count']}",
        f"- 重复目标键：{report['duplicate_target_key_count']}",
        "",
        "## 状态统计",
        "",
        "| 状态 | 数量 |",
        "|---|---:|",
    ]
    for status, count in report["by_status"].items():
        lines.append(f"| {status} | {count} |")

    lines.extend(["", "## 原因统计", "", "| 原因 | 数量 |", "|---|---:|"])
    for reason, count in report["by_reason"].items():
        lines.append(f"| {reason} | {count} |")

    lines.extend(["", "## 重复目标键", ""])
    if report["duplicate_target_keys"]:
        lines.extend(["| target_key | 文档 |", "|---|---|"])
        for item in report["duplicate_target_keys"]:
            docs = "<br>".join(f"`{doc['path']}`" for doc in item["documents"])
            lines.append(f"| `{item['target_key']}` | {docs} |")
    else:
        lines.append("无。")

    lines.extend(["", "## 问题明细", ""])
    if report["issues"]:
        lines.extend(["| 状态 | 来源 | 行 | 链接目标 | 命中的标题页 | 原因 |", "|---|---|---:|---|---|---|"])
        for item in report["issues"]:
            target = item["target_path"] or "-"
            lines.append(
                "| {status} | `{source}` | {line_no} | `{target_text}` | `{target}` | {reason} |".format(
                    status=item["status"],
                    source=item["source_path"],
                    line_no=item["line_no"],
                    target_text=item["target_text"].replace("|", "\\|"),
                    target=target,
                    reason=item["reason"],
                )
            )
    else:
        lines.append("无。")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = build_report(Path(args.vault))
    if args.out_json:
        out_json = Path(args.out_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.out_md:
        out_md = Path(args.out_md)
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(render_markdown(report), encoding="utf-8")
    print(
        "documents={documents} strict_resolved={strict_resolved} issues={issue_count} duplicate_target_keys={duplicate_target_key_count}".format(
            **report
        )
    )
    has_failure = report["issue_count"] > 0 or report["duplicate_target_key_count"] > 0
    return 1 if args.fail and has_failure else 0


if __name__ == "__main__":
    raise SystemExit(main())
