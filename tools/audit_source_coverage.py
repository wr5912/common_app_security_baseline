#!/usr/bin/env python3
"""Audit KB coverage for every row in the Windows common app/service source."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from .wabk_common import Document, build_title_index, load_documents, resolve_link
    from .windows_source_inventory import SourceRow, parse_source
except ImportError:
    from wabk_common import Document, build_title_index, load_documents, resolve_link
    from windows_source_inventory import SourceRow, parse_source


BASE_REQUIRED_TYPES = {
    "service",
    "startup_method",
    "process",
    "process_relation",
    "registry_pattern",
    "file_artifact",
    "network_behavior",
    "security_baseline",
    "source_evidence",
}
THIRD_PARTY_REQUIRED_TYPES = BASE_REQUIRED_TYPES | {"app"}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit full source-list coverage in the KB.")
    parser.add_argument("--vault", default="kb")
    parser.add_argument("--source", default="/tmp/windows系统上常见应用.md")
    parser.add_argument("--out-md")
    parser.add_argument("--out-json")
    parser.add_argument("--fail", action="store_true")
    return parser.parse_args(argv)


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item not in (None, "")]
    return [str(value)]


def source_ids(doc: Document) -> set[str]:
    ids: set[str] = set()
    for key in ("source_row_id", "source_row_ids"):
        ids.update(as_list(doc.frontmatter.get(key)))
    return {item.strip() for item in ids if item.strip()}


def status_ok(doc: Document) -> bool:
    return str(doc.frontmatter.get("status", "")).strip() not in {"", "draft", "needs_review"}


def confidence_ok(doc: Document) -> bool:
    return str(doc.frontmatter.get("confidence", "")).strip() not in {"", "low"}


def collect_linked_docs(seed_docs: list[Document], docs_by_id: dict[str, Document], title_index: dict[str, str]) -> dict[str, Document]:
    collected: dict[str, Document] = {}
    for doc in seed_docs:
        collected[doc.id] = doc
        for occurrence in doc.link_occurrences:
            doc_id = resolve_link(occurrence["target_text"], title_index)
            if doc_id and doc_id in docs_by_id:
                target = docs_by_id[doc_id]
                collected[target.id] = target
    return collected


def required_types_for(row: SourceRow) -> set[str]:
    if row.row_kind == "third_party_service":
        return THIRD_PARTY_REQUIRED_TYPES
    return BASE_REQUIRED_TYPES


def build_report(vault: Path, source: Path) -> dict[str, Any]:
    rows = parse_source(source)
    docs = load_documents(vault)
    title_index = build_title_index(docs)
    docs_by_id = {doc.id: doc for doc in docs}
    docs_by_source: dict[str, list[Document]] = {}
    for doc in docs:
        for source_id in source_ids(doc):
            docs_by_source.setdefault(source_id, []).append(doc)

    items: list[dict[str, Any]] = []
    for row in rows:
        tagged = sorted(docs_by_source.get(row.row_id, []), key=lambda doc: doc.path)
        linked = collect_linked_docs(tagged, docs_by_id, title_index)
        covered_types = {doc.type for doc in linked.values()}
        required = required_types_for(row)
        missing = sorted(required - covered_types)
        weak = [
            doc.title
            for doc in tagged
            if doc.type != "source_evidence" and (not status_ok(doc) or not confidence_ok(doc))
        ]
        complete = not missing and not weak
        items.append(
            {
                "row_id": row.row_id,
                "line_no": row.line_no,
                "row_kind": row.row_kind,
                "section": row.section,
                "subsection": row.subsection,
                "service_pattern": row.service_pattern,
                "app_vendor": row.app_vendor,
                "complete": complete,
                "missing_types": missing,
                "weak_docs": weak,
                "documents": [
                    {
                        "title": doc.title,
                        "type": doc.type,
                        "path": doc.path,
                        "status": str(doc.frontmatter.get("status", "")),
                        "confidence": str(doc.frontmatter.get("confidence", "")),
                    }
                    for doc in tagged
                ],
            }
        )

    by_kind: dict[str, dict[str, int]] = {}
    for item in items:
        stats = by_kind.setdefault(item["row_kind"], {"total": 0, "complete": 0})
        stats["total"] += 1
        if item["complete"]:
            stats["complete"] += 1

    return {
        "source": str(source),
        "source_rows": len(items),
        "covered": sum(1 for item in items if item["complete"]),
        "missing": sum(1 for item in items if not item["complete"]),
        "by_kind": by_kind,
        "items": items,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Windows 常见应用全量来源覆盖审计",
        "",
        f"- 来源：`{report['source']}`",
        f"- 来源行：{report['source_rows']}",
        f"- 已覆盖：{report['covered']}",
        f"- 未覆盖：{report['missing']}",
        "",
        "## 分类统计",
        "",
        "| 类型 | 总数 | 完整 | 缺失 |",
        "|---|---:|---:|---:|",
    ]
    for kind, stats in sorted(report["by_kind"].items()):
        lines.append(f"| {kind} | {stats['total']} | {stats['complete']} | {stats['total'] - stats['complete']} |")
    lines.extend(["", "## 未覆盖明细", ""])
    missing = [item for item in report["items"] if not item["complete"]]
    if not missing:
        lines.append("无。")
    else:
        lines.extend(["| 行 | row_id | 服务/模式 | 应用/厂商 | 缺失类型 | 弱页面 |", "|---:|---|---|---|---|---|"])
        for item in missing:
            lines.append(
                "| {line_no} | `{row_id}` | {service} | {app} | {missing} | {weak} |".format(
                    line_no=item["line_no"],
                    row_id=item["row_id"],
                    service=item["service_pattern"].replace("|", "\\|"),
                    app=item["app_vendor"].replace("|", "\\|"),
                    missing=", ".join(item["missing_types"]) or "-",
                    weak=", ".join(item["weak_docs"]) or "-",
                )
            )
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = build_report(Path(args.vault), Path(args.source))
    if args.out_json:
        out_json = Path(args.out_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.out_md:
        out_md = Path(args.out_md)
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(render_markdown(report), encoding="utf-8")
    print(f"source_rows={report['source_rows']} covered={report['covered']} missing={report['missing']}")
    return 1 if args.fail and report["missing"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
