#!/usr/bin/env python3
"""Smoke-test lifecycle rule matching with STIX-like behavior facts."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


NETWORK_INDICATORS = {
    "network_connection",
    "network_connections",
    "network_after_spawn",
    "network_after_install",
    "abnormal_external_connection",
    "lateral_movement",
}
FILE_INDICATORS = {
    "file_write",
    "file_activity",
    "file_drop_after_spawn",
    "downloaded_file",
    "sensitive_file_access",
    "data_archive",
}
REGISTRY_INDICATORS = {
    "registry_activity",
    "registry_or_config_activity",
    "persistence_change",
    "persistence_changes",
    "persistence_after_spawn",
    "persistence_write",
    "service_creation",
    "scheduled_task_change",
    "run_key_change",
}
CHILD_INDICATORS = {
    "child_processes",
    "unknown_child_process",
}


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run lifecycle-rule end-to-end smoke checks.")
    parser.add_argument("--rules-jsonl", default="out/lifecycle_rules.jsonl", help="Lifecycle rule JSONL file")
    parser.add_argument("--out", default="out/lifecycle_e2e_smoke.json", help="Smoke result JSON path")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if smoke checks fail")
    return parser.parse_args(argv)


def load_rules(path: Path) -> list[dict[str, Any]]:
    rules: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            text = line.strip()
            if not text:
                continue
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL at {path}:{line_no}: {exc}") from exc
            if isinstance(parsed, dict):
                rules.append(parsed)
    return rules


def basename(value: str) -> str:
    normalized = str(value or "").replace("\\", "/").strip().lower()
    if not normalized:
        return ""
    return normalized.rsplit("/", 1)[-1]


def fixture_complete_office_lifecycle() -> dict[str, Any]:
    return {
        "name": "office_powershell_full_lifecycle",
        "process_key": "proc-office-1",
        "process": {
            "image_path": r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
            "command_line": "powershell.exe -NoProfile -EncodedCommand SQBFAFgA",
            "user_name": "alice",
        },
        "parent": {
            "image_path": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
        },
        "children": [],
        "network_connections": [{"dst": "203.0.113.10", "dst_port": 443}],
        "files": [{"path": r"C:\Users\alice\AppData\Local\Temp\stage.ps1"}],
        "registry_keys": [{"key": r"HKCU\Software\Microsoft\Windows\CurrentVersion\Run"}],
    }


def fixture_missing_runtime_evidence() -> dict[str, Any]:
    item = fixture_complete_office_lifecycle()
    item = json.loads(json.dumps(item))
    item["name"] = "office_powershell_missing_runtime"
    item["network_connections"] = []
    item["files"] = []
    item["registry_keys"] = []
    return item


def match_creation_rules(fact: dict[str, Any], rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    child_name = basename(fact["process"].get("image_path") or fact["process"].get("name"))
    parent_name = basename((fact.get("parent") or {}).get("image_path") or (fact.get("parent") or {}).get("name"))
    command_line = str(fact["process"].get("command_line") or fact["process"].get("cmd_line") or "").lower()
    matches: list[dict[str, Any]] = []
    for rule in rules:
        if rule.get("phase") not in {"creation", "lifecycle"}:
            continue
        if rule.get("applies_to") not in {"process_relation", "process", "process_behavior", "security_baseline"}:
            continue
        parents = set(rule.get("parent_process_names") or [])
        children = set(rule.get("child_process_names") or [])
        if parents and parent_name not in parents:
            continue
        if children and child_name not in children:
            continue
        matched_terms = [term for term in rule.get("command_line_terms") or [] if str(term).lower() in command_line]
        matches.append({
            "rule_id": rule.get("rule_id"),
            "rule_name": rule.get("rule_name"),
            "source_path": rule.get("source_path"),
            "risk_level": rule.get("risk_level"),
            "normality": rule.get("normality"),
            "result_if_matched": rule.get("result_if_matched"),
            "matched_command_terms": matched_terms,
            "evidence_requirements": rule.get("evidence_requirements") or [],
        })
    return matches


def matched_runtime_indicators(fact: dict[str, Any], rule: dict[str, Any]) -> list[str]:
    indicators = set(rule.get("runtime_indicators") or [])
    matched: set[str] = set()
    if fact.get("network_connections"):
        matched.update(indicators & NETWORK_INDICATORS)
    if fact.get("files"):
        matched.update(indicators & FILE_INDICATORS)
    if fact.get("registry_keys"):
        matched.update(indicators & REGISTRY_INDICATORS)
    if fact.get("children"):
        matched.update(indicators & CHILD_INDICATORS)
    return sorted(matched)


def match_runtime_rules(fact: dict[str, Any], rules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    child_names = {basename(child.get("image_path") or child.get("name")) for child in fact.get("children") or []}
    matches: list[dict[str, Any]] = []
    for rule in rules:
        if rule.get("phase") not in {"runtime", "lifecycle"}:
            continue
        runtime_children = set(rule.get("runtime_child_process_names") or [])
        indicators = matched_runtime_indicators(fact, rule)
        if runtime_children and child_names.intersection(runtime_children):
            matches.append(runtime_match(rule, indicators))
        elif indicators:
            matches.append(runtime_match(rule, indicators))
    return matches


def runtime_match(rule: dict[str, Any], indicators: list[str]) -> dict[str, Any]:
    return {
        "rule_id": rule.get("rule_id"),
        "rule_name": rule.get("rule_name"),
        "source_path": rule.get("source_path"),
        "risk_level": rule.get("risk_level"),
        "normality": rule.get("normality"),
        "matched_runtime_indicators": indicators,
        "evidence_requirements": rule.get("evidence_requirements") or [],
    }


def evidence_result(fact: dict[str, Any]) -> dict[str, Any]:
    process = fact.get("process") or {}
    has_parent = bool(fact.get("parent"))
    has_image_path = bool(process.get("image_path") or process.get("file_path"))
    has_command_line = bool(process.get("command_line") or process.get("cmd_line"))
    has_user = bool(process.get("user_name") or process.get("user_id") or process.get("user_domain"))
    has_runtime = any([
        fact.get("children"),
        fact.get("network_connections"),
        fact.get("files"),
        fact.get("registry_keys"),
    ])
    result = "lifecycle_evidence_present"
    if not all([has_parent, has_image_path, has_command_line, has_user, has_runtime]):
        result = "evidence_insufficient"
    return {
        "has_parent_process": has_parent,
        "has_image_path": has_image_path,
        "has_command_line": has_command_line,
        "has_user": has_user,
        "has_child_process_evidence": bool(fact.get("children")),
        "has_network_evidence": bool(fact.get("network_connections")),
        "has_file_evidence": bool(fact.get("files")),
        "has_registry_evidence": bool(fact.get("registry_keys")),
        "lifecycle_evidence_result": result,
    }


def analyze_fact(fact: dict[str, Any], rules: list[dict[str, Any]]) -> dict[str, Any]:
    creation_matches = match_creation_rules(fact, rules)
    runtime_matches = match_runtime_rules(fact, rules)
    evidence = evidence_result(fact)
    if evidence["lifecycle_evidence_result"] == "evidence_insufficient":
        lifecycle_result = "evidence_insufficient"
    elif not creation_matches or not runtime_matches:
        lifecycle_result = "baseline_gap"
    elif any(match.get("result_if_matched") == "risky" for match in creation_matches):
        lifecycle_result = "risky"
    else:
        lifecycle_result = "safe"
    return {
        "fixture": fact["name"],
        "creation_rule_matches": creation_matches,
        "runtime_rule_matches": runtime_matches,
        "evidence": evidence,
        "lifecycle_result": lifecycle_result,
    }


def build_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    by_fixture = {item["fixture"]: item for item in results}
    complete = by_fixture["office_powershell_full_lifecycle"]
    missing = by_fixture["office_powershell_missing_runtime"]
    checks = {
        "complete_fixture_has_creation_rule": bool(complete["creation_rule_matches"]),
        "complete_fixture_has_runtime_rule": bool(complete["runtime_rule_matches"]),
        "complete_fixture_lifecycle_risky": complete["lifecycle_result"] == "risky",
        "missing_runtime_is_evidence_insufficient": missing["lifecycle_result"] == "evidence_insufficient",
    }
    return {
        "passed": all(checks.values()),
        "checks": checks,
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    rules = load_rules(Path(args.rules_jsonl))
    facts = [fixture_complete_office_lifecycle(), fixture_missing_runtime_evidence()]
    results = [analyze_fact(fact, rules) for fact in facts]
    summary = build_summary(results)
    report = {
        "rules_path": args.rules_jsonl,
        "rule_count": len(rules),
        "summary": summary,
        "results": results,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    print(
        f"passed={summary['passed']} rules={len(rules)} "
        f"fixtures={len(results)} out={args.out}"
    )
    return 1 if args.strict and not summary["passed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
