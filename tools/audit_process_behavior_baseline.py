#!/usr/bin/env python3
"""Audit process creation and runtime baseline coverage in the Markdown KB."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from .wabk_common import Document, load_documents
except ImportError:  # allow running as: python tools/audit_process_behavior_baseline.py
    from wabk_common import Document, load_documents


PROCESS_REQUIRED_SECTIONS = [
    "进程创建基线",
    "启动参数基线",
    "运行时行为基线",
    "安全关注点",
    "证据需求",
    "关联安全基线",
]

RELATION_REQUIRED_SECTION_GROUPS = {
    "创建链路基线": ["创建链路基线"],
    "高风险参数": ["高风险参数", "高风险参数与命令行关注"],
    "证据需求": ["证据需求", "需要补充的证据"],
    "关联画像": ["关联画像"],
}

PROCESS_BASELINE_LINK = "进程创建与运行时异常"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit process creation/runtime baseline coverage.")
    parser.add_argument("--vault", default="kb", help="Knowledge-base vault root")
    parser.add_argument("--out-md", default=None, help="Write Markdown report")
    parser.add_argument("--out-json", default=None, help="Write JSON report")
    parser.add_argument("--scope", choices=["all", "process", "relation"], default="all", help="Document scope")
    parser.add_argument("--fail", action="store_true", help="Exit non-zero if any issue is found")
    return parser.parse_args(argv)


def normalize_heading(value: str) -> str:
    text = re.sub(r"^\s*\d+\.\s*", "", value or "").strip()
    return re.sub(r"\s+", "", text)


def section_headings(doc: Document) -> set[str]:
    return {normalize_heading(str(section.get("heading", ""))) for section in doc.sections}


def linked(doc: Document, target: str) -> bool:
    return target in doc.links


def relation_title_ok(doc: Document) -> bool:
    stem = Path(doc.path).stem
    return "->" in stem and "->" in doc.title


def audit_process(doc: Document) -> list[dict[str, str]]:
    headings = section_headings(doc)
    issues: list[dict[str, str]] = []
    for required in PROCESS_REQUIRED_SECTIONS:
        if normalize_heading(required) not in headings:
            issues.append({"code": "missing_process_section", "detail": required})
    if not linked(doc, PROCESS_BASELINE_LINK):
        issues.append({"code": "missing_process_baseline_link", "detail": PROCESS_BASELINE_LINK})
    if not str(doc.frontmatter.get("process_name", "")).strip():
        issues.append({"code": "missing_process_name", "detail": "frontmatter.process_name"})
    return issues


def audit_relation(doc: Document) -> list[dict[str, str]]:
    headings = section_headings(doc)
    issues: list[dict[str, str]] = []
    for label, aliases in RELATION_REQUIRED_SECTION_GROUPS.items():
        if not any(normalize_heading(alias) in headings for alias in aliases):
            issues.append({"code": "missing_relation_section", "detail": label})
    if not str(doc.frontmatter.get("parent_process", "")).strip():
        issues.append({"code": "missing_parent_process", "detail": "frontmatter.parent_process"})
    if not str(doc.frontmatter.get("child_process", "")).strip():
        issues.append({"code": "missing_child_process", "detail": "frontmatter.child_process"})
    if not relation_title_ok(doc):
        issues.append({"code": "relation_title_or_filename_not_canonical", "detail": "expected parent -> child"})
    return issues


def build_report(vault: Path, scope: str) -> dict[str, Any]:
    docs = load_documents(vault)
    rows: list[dict[str, Any]] = []
    process_count = 0
    relation_count = 0

    for doc in docs:
        if doc.path.startswith("99_模板/"):
            continue
        if doc.type == "process" and scope in {"all", "process"}:
            process_count += 1
            issues = audit_process(doc)
        elif doc.type == "process_relation" and scope in {"all", "relation"}:
            relation_count += 1
            issues = audit_relation(doc)
        else:
            continue
        if issues:
            rows.append(
                {
                    "title": doc.title,
                    "path": doc.path,
                    "type": doc.type,
                    "issues": issues,
                }
            )

    return {
        "process_count": process_count,
        "relation_count": relation_count,
        "issue_count": sum(len(row["issues"]) for row in rows),
        "document_issue_count": len(rows),
        "issues": rows,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# 进程创建与运行时基线审计",
        "",
        f"- 进程文档：{report['process_count']}",
        f"- 父子关系文档：{report['relation_count']}",
        f"- 问题文档：{report['document_issue_count']}",
        f"- 问题数：{report['issue_count']}",
        "",
    ]
    if not report["issues"]:
        lines.append("未发现问题。")
        return "\n".join(lines).rstrip() + "\n"

    lines.extend(["## 问题明细", ""])
    for item in report["issues"]:
        lines.append(f"### {item['title']}")
        lines.append("")
        lines.append(f"- 路径：`{item['path']}`")
        lines.append(f"- 类型：`{item['type']}`")
        for issue in item["issues"]:
            lines.append(f"- {issue['code']}: `{issue['detail']}`")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = build_report(Path(args.vault), args.scope)
    if args.out_json:
        out = Path(args.out_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.out_md:
        out = Path(args.out_md)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown(report), encoding="utf-8")

    print(
        f"process={report['process_count']} relation={report['relation_count']} "
        f"documents_with_issues={report['document_issue_count']} issues={report['issue_count']}"
    )
    return 1 if args.fail and report["issue_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
