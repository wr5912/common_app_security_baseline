#!/usr/bin/env python3
"""Audit KB profile completeness for scoped application pages.

The Markdown vault remains the source of truth. This tool checks whether each
scoped application has linked or back-linked coverage across the core profile
chain:

app -> service/startup -> process -> process relation -> file/registry/network
-> security baseline -> source evidence.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    from .wabk_common import Document, build_title_index, load_documents, resolve_link
except ImportError:  # allow running as: python tools/audit_profile_completeness.py
    from wabk_common import Document, build_title_index, load_documents, resolve_link


REQUIRED_TYPES = [
    "service",
    "process",
    "process_relation",
    "startup_method",
    "registry_pattern",
    "file_artifact",
    "network_behavior",
    "security_baseline",
    "source_evidence",
]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit complete-profile coverage for KB applications.")
    parser.add_argument("--vault", default="kb", help="Knowledge-base vault root")
    parser.add_argument("--scope-git-range", default=None, help="Git range used to scope added app pages, for example HEAD^..HEAD")
    parser.add_argument("--scope-file", default=None, help="Text file containing one app title or path per line")
    parser.add_argument("--out-md", default=None, help="Write Markdown report")
    parser.add_argument("--out-json", default=None, help="Write JSON report")
    parser.add_argument("--fail", action="store_true", help="Exit non-zero if any scoped app is incomplete")
    return parser.parse_args(argv)


def git_added_app_paths(git_range: str) -> list[str]:
    base, head = split_git_range(git_range)
    raw = subprocess.check_output(
        ["git", "-c", "core.quotepath=false", "diff", "--name-status", base, head],
        text=True,
    )
    paths: list[str] = []
    for line in raw.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2 and parts[0] == "A" and parts[1].startswith("kb/01_应用/") and parts[1].endswith(".md"):
            paths.append(parts[1])
    return paths


def split_git_range(git_range: str) -> tuple[str, str]:
    if ".." in git_range:
        base, head = git_range.split("..", 1)
        return base or "HEAD^", head or "HEAD"
    return f"{git_range}^", git_range


def read_scope_file(path: str) -> list[str]:
    return [line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#")]


def normalize_link_value(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        values = value
    else:
        values = [value]
    result: list[str] = []
    for item in values:
        text = str(item)
        if "[[" in text and "]]" in text:
            result.extend(part.split("]]", 1)[0].strip() for part in text.split("[[")[1:] if "]]" in part)
        elif text.strip():
            result.append(text.strip().strip('"').strip("'"))
    return result


def app_matches(doc: Document, app_title: str, app_id: str | None) -> bool:
    if doc.title == app_title or doc.name == app_title:
        return True
    for key in ["app", "application", "related_app", "source_app"]:
        for value in normalize_link_value(doc.frontmatter.get(key)):
            if value == app_title:
                return True
    if app_id and doc.frontmatter.get("app_id") == app_id:
        return True
    return app_title in doc.links


def build_incoming_links(docs: list[Document], title_index: dict[str, str]) -> dict[str, set[str]]:
    incoming: dict[str, set[str]] = defaultdict(set)
    for doc in docs:
        for occ in doc.link_occurrences:
            target = resolve_link(occ["target_text"], title_index)
            if target:
                incoming[target].add(doc.id)
    return incoming


def collect_coverage(
    app: Document,
    docs: list[Document],
    by_id: dict[str, Document],
    by_title: dict[str, Document],
    incoming: dict[str, set[str]],
) -> dict[str, list[dict[str, str]]]:
    app_id = app.frontmatter.get("app_id")
    related: dict[str, dict[str, Document]] = {kind: {} for kind in REQUIRED_TYPES}

    for doc in docs:
        if doc.id == app.id:
            continue
        if doc.type in related and app_matches(doc, app.title, str(app_id) if app_id else None):
            related[doc.type][doc.id] = doc

    for target in app.links:
        target_doc = by_title.get(target)
        if target_doc and target_doc.type in related:
            related[target_doc.type][target_doc.id] = target_doc

    for source_id in incoming.get(app.id, set()):
        source = by_id[source_id]
        if source.type in related:
            related[source.type][source.id] = source

    return {
        kind: [
            {
                "title": doc.title,
                "path": doc.path,
                "status": str(doc.frontmatter.get("status", "")),
                "confidence": str(doc.frontmatter.get("confidence", "")),
            }
            for doc in sorted(items.values(), key=lambda d: d.path)
        ]
        for kind, items in related.items()
    }


def collect_not_applicable(coverage: dict[str, list[dict[str, str]]]) -> set[str]:
    not_applicable: set[str] = set()
    for evidence in coverage.get("source_evidence", []):
        doc = by_path.get(evidence["path"])
        if not doc:
            continue
        for value in doc.frontmatter.get("not_applicable_types") or []:
            not_applicable.add(str(value))
    return not_applicable


def status_ok(doc: Document) -> bool:
    return str(doc.frontmatter.get("status", "")).strip() not in {"", "draft", "needs_review"}


def confidence_ok(doc: Document) -> bool:
    return str(doc.frontmatter.get("confidence", "")).strip() not in {"", "low"}


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Windows 常见应用完整画像覆盖审计",
        "",
        f"- 审计范围：{report['scope_count']} 个应用",
        f"- 完整应用：{report['complete_count']} 个",
        f"- 不完整应用：{report['incomplete_count']} 个",
        "",
        "## 汇总表",
        "",
        "| 应用 | 完整 | 缺失类型 | 状态 | 置信度 |",
        "|---|---:|---|---|---|",
    ]
    for item in report["apps"]:
        missing = ", ".join(item["missing_types"]) if item["missing_types"] else "-"
        lines.append(
            f"| [[{item['title']}]] | {'yes' if item['complete'] else 'no'} | {missing} | {item['status']} | {item['confidence']} |"
        )
    lines.extend(["", "## 明细", ""])
    for item in report["apps"]:
        lines.append(f"### {item['title']}")
        lines.append("")
        lines.append(f"- 路径：`{item['path']}`")
        lines.append(f"- 完整：`{item['complete']}`")
        lines.append(f"- 缺失类型：`{', '.join(item['missing_types']) if item['missing_types'] else '-'}`")
        lines.append(f"- 页面状态：`{item['status']}`；置信度：`{item['confidence']}`")
        for kind in REQUIRED_TYPES:
            docs = item["coverage"][kind]
            if docs:
                linked = ", ".join(f"[[{doc['title']}]]" for doc in docs)
            else:
                linked = "_缺失_"
            lines.append(f"- {kind}: {linked}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def resolve_scope_apps(scope_items: list[str], docs: list[Document], vault: Path) -> list[Document]:
    title_map = {doc.title: doc for doc in docs}
    path_map = {doc.path: doc for doc in docs}
    scoped: list[Document] = []
    for item in scope_items:
        rel = item
        if rel.startswith(str(vault) + "/"):
            rel = rel[len(str(vault)) + 1 :]
        if rel in path_map:
            doc = path_map[rel]
        elif item in title_map:
            doc = title_map[item]
        elif Path(item).name.endswith(".md") and str(Path(item).parent).endswith("01_应用"):
            doc = title_map.get(Path(item).stem)
        else:
            raise SystemExit(f"scope item not found as app title/path: {item}")
        if doc.type != "app":
            raise SystemExit(f"scope item is not type=app: {item} -> {doc.path}")
        scoped.append(doc)
    return sorted({doc.id: doc for doc in scoped}.values(), key=lambda d: d.title)


def build_report(vault: Path, scope_items: list[str]) -> dict[str, Any]:
    docs = load_documents(vault)
    by_title = {doc.title: doc for doc in docs}
    global by_path
    by_path = {doc.path: doc for doc in docs}
    by_id = {doc.id: doc for doc in docs}
    title_index = build_title_index(docs)
    incoming = build_incoming_links(docs, title_index)
    scoped_apps = resolve_scope_apps(scope_items, docs, vault)

    apps: list[dict[str, Any]] = []
    for app in scoped_apps:
        coverage = collect_coverage(app, docs, by_id, by_title, incoming)
        not_applicable = collect_not_applicable(coverage)
        missing = [kind for kind in REQUIRED_TYPES if not coverage[kind] and kind not in not_applicable]
        if not status_ok(app):
            missing.append("app_status")
        if not confidence_ok(app):
            missing.append("app_confidence")
        complete = not missing
        apps.append(
            {
                "title": app.title,
                "path": app.path,
                "status": str(app.frontmatter.get("status", "")),
                "confidence": str(app.frontmatter.get("confidence", "")),
                "complete": complete,
                "missing_types": missing,
                "not_applicable_types": sorted(not_applicable),
                "coverage": coverage,
            }
        )
    return {
        "scope_count": len(apps),
        "complete_count": sum(1 for item in apps if item["complete"]),
        "incomplete_count": sum(1 for item in apps if not item["complete"]),
        "required_types": REQUIRED_TYPES,
        "apps": apps,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    vault = Path(args.vault)
    scope_items: list[str]
    if args.scope_file:
        scope_items = read_scope_file(args.scope_file)
    elif args.scope_git_range:
        scope_items = git_added_app_paths(args.scope_git_range)
    else:
        scope_items = [str(path) for path in sorted((vault / "01_应用").glob("*.md"))]

    report = build_report(vault, scope_items)
    if args.out_json:
        out = Path(args.out_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.out_md:
        out = Path(args.out_md)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown(report), encoding="utf-8")

    print(
        f"scope={report['scope_count']} complete={report['complete_count']} "
        f"incomplete={report['incomplete_count']}"
    )
    return 1 if args.fail and report["incomplete_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
