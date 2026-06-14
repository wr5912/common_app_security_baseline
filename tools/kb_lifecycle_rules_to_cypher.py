#!/usr/bin/env python3
"""Convert lifecycle baseline knowledge into JSONL and Cypher rule artifacts."""
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None

try:
    from .wabk_common import Document, configure_logging, json_dumps, load_documents, stable_id
except ImportError:  # allow running as: python tools/kb_lifecycle_rules_to_cypher.py
    from wabk_common import Document, configure_logging, json_dumps, load_documents, stable_id


LOG = logging.getLogger("wabk.lifecycle_rules")

CODE_FENCE_RE = re.compile(r"```(?:yaml|yml|text|txt)?\s*\n(.*?)```", re.S)
YAML_FENCE_RE = re.compile(r"```(?:yaml|yml)\s*\n(.*?)```", re.S)
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
COMMAND_TOKEN_RE = re.compile(
    r"(?<![\w])(?:-[A-Za-z][\w-]+|/[A-Za-z?][\w?]*|IEX|DownloadString|FromBase64String|EncodedCommand)(?![\w])"
)

STRUCTURED_RULE_HEADINGS = {
    "结构化生命周期基线",
    "结构化生命周期规则",
    "生命周期条件规则",
}

RULE_SOURCE_TYPES = {
    "process",
    "service",
    "process_relation",
    "security_baseline",
}

DEFAULT_CREATION_EVIDENCE = [
    "parent_process",
    "child_process",
    "image_path",
    "command_line",
    "user",
]

RUNTIME_EVIDENCE_KEYWORDS = [
    ("网络", "network_connections"),
    ("外联", "network_connections"),
    ("连接", "network_connections"),
    ("文件", "file_activity"),
    ("落地", "file_activity"),
    ("注册表", "registry_activity"),
    ("Run Key", "persistence_changes"),
    ("计划任务", "persistence_changes"),
    ("服务", "persistence_changes"),
    ("持久化", "persistence_changes"),
]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert KB lifecycle baseline rules to JSONL and Cypher.")
    parser.add_argument("--vault", default="kb", help="Obsidian vault root path")
    parser.add_argument("--out-jsonl", default="out/lifecycle_rules.jsonl", help="Output rule JSONL path")
    parser.add_argument("--out-cypher", default="out/lifecycle_rules.cypher", help="Output Cypher path")
    parser.add_argument(
        "--out-query-cypher",
        default="out/lifecycle_analysis_queries.cypher",
        help="Output reusable STIX behavior graph analysis query templates",
    )
    parser.add_argument(
        "--no-derived-relation-rules",
        action="store_true",
        help="Only emit explicit structured lifecycle YAML rules; do not derive rules from process_relation pages",
    )
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if no rule is generated")
    parser.add_argument("--debug", action="store_true", help="Enable debug logs")
    parser.add_argument("--log-file", default=None, help="Write logs to file as well as stderr")
    return parser.parse_args(argv)


def normalize_heading(value: str) -> str:
    text = re.sub(r"^\s*\d+\.\s*", "", value or "").strip()
    return re.sub(r"\s+", "", text)


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, tuple):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def clean_link_text(value: Any) -> str:
    items = as_list(value)
    if not items:
        return ""
    text = items[0].strip().strip('"').strip("'")
    if text.startswith("[[") and text.endswith("]]"):
        text = text[2:-2]
    text = text.split("|", 1)[0].split("#", 1)[0].strip()
    text = text.rsplit("/", 1)[-1]
    if text.lower().endswith(".md"):
        text = text[:-3]
    return text.strip()


def normalize_token(value: Any) -> str:
    return str(value or "").strip().lower()


def unique_strings(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        text = normalize_token(value)
        if text and text not in seen:
            seen.add(text)
            result.append(text)
    return result


def section_by_heading(doc: Document, names: set[str]) -> list[dict[str, Any]]:
    wanted = {normalize_heading(name) for name in names}
    return [section for section in doc.sections if normalize_heading(str(section.get("heading", ""))) in wanted]


def extract_fence_lines(content: str) -> list[str]:
    blocks = CODE_FENCE_RE.findall(content or "")
    source = "\n".join(blocks) if blocks else content
    lines: list[str] = []
    for raw in source.splitlines():
        line = raw.strip().strip("`").strip()
        line = re.sub(r"^\s*[-*]\s+", "", line).strip()
        if not line or line.startswith("<!--") or line.startswith("说明"):
            continue
        lines.append(line)
    return lines


def extract_command_terms(lines: list[str]) -> list[str]:
    terms: set[str] = set()
    for line in lines:
        for item in INLINE_CODE_RE.findall(line):
            if item.strip():
                terms.add(item.strip())
        for item in COMMAND_TOKEN_RE.findall(line):
            if item.strip():
                terms.add(item.strip())
        if not re.search(r"[\u4e00-\u9fff]", line) and len(line) <= 80:
            terms.add(line.strip())
    return sorted(terms)


def parse_yaml_blocks(content: str) -> list[dict[str, Any]]:
    if not yaml:
        LOG.warning("PyYAML is unavailable; skip structured lifecycle YAML block parsing")
        return []
    parsed_blocks: list[dict[str, Any]] = []
    for block in YAML_FENCE_RE.findall(content or ""):
        try:
            parsed = yaml.safe_load(block) or {}
        except Exception as exc:
            LOG.warning("skip invalid lifecycle YAML block: %s", exc)
            continue
        if isinstance(parsed, dict):
            parsed_blocks.append(parsed)
    return parsed_blocks


def collect_required_evidence(value: Any) -> list[str]:
    evidence: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key) in {"required_evidence", "required_followup_evidence"}:
                evidence.extend(as_list(item))
            evidence.extend(collect_required_evidence(item))
    elif isinstance(value, list):
        for item in value:
            evidence.extend(collect_required_evidence(item))
    return sorted(set(evidence))


def collect_condition_values(value: Any, keys: set[str]) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key) in keys:
                found.extend(as_list(item))
            found.extend(collect_condition_values(item, keys))
    elif isinstance(value, list):
        for item in value:
            found.extend(collect_condition_values(item, keys))
    return unique_strings(found)


def build_match_fields(conditions: dict[str, Any]) -> dict[str, list[str]]:
    return {
        "parent_process_names": collect_condition_values(
            conditions,
            {"parent_process_name", "parent_process_any", "expected_parent_processes"},
        ),
        "child_process_names": collect_condition_values(
            conditions,
            {"child_process_name", "child_process_any", "expected_child_processes"},
        ),
        "runtime_child_process_names": collect_condition_values(
            conditions,
            {"suspicious_child_processes", "runtime_child_process_any"},
        ),
        "command_line_terms": collect_condition_values(
            conditions,
            {"command_line_contains_any", "command_contains", "command_line_any"},
        ),
        "image_location_terms": collect_condition_values(
            conditions,
            {"suspicious_image_locations", "image_location_any"},
        ),
        "runtime_indicators": collect_condition_values(
            conditions,
            {"risk_escalates_when", "followed_by_any", "required_followup_evidence"},
        ),
        "false_positive_contexts": collect_condition_values(
            conditions,
            {"allowed_contexts"},
        ),
    }


def infer_phase(conditions: dict[str, Any]) -> str:
    explicit = str(conditions.get("phase") or "").strip()
    if explicit:
        return explicit
    has_creation = isinstance(conditions.get("creation"), dict)
    has_runtime = isinstance(conditions.get("runtime"), dict)
    if has_creation and has_runtime:
        return "lifecycle"
    if has_creation:
        return "creation"
    if has_runtime:
        return "runtime"
    return "lifecycle"


def result_if_matched(normality: str, risk_level: str) -> str:
    normality = (normality or "").lower()
    risk_level = (risk_level or "").lower()
    if risk_level in {"high", "critical"} or normality in {"rare", "suspicious", "malicious_like"}:
        return "risky"
    return "match_known"


def make_rule(doc: Document, kind: str, index: int, conditions: dict[str, Any]) -> dict[str, Any]:
    normality = str(doc.frontmatter.get("normality") or conditions.get("normality") or "")
    risk_level = str(doc.frontmatter.get("risk_level") or conditions.get("risk_level") or "")
    confidence = str(doc.frontmatter.get("confidence") or conditions.get("confidence") or "")
    phase = infer_phase(conditions)
    applies_to = str(conditions.get("applies_to") or doc.type)
    match_fields = build_match_fields(conditions)
    return {
        "rule_id": stable_id("lifecycle_rule", f"{doc.path}:{kind}:{index}"),
        "rule_name": f"{doc.title}::{kind}",
        "rule_kind": kind,
        "source_doc_id": doc.id,
        "source_path": doc.path,
        "source_title": doc.title,
        "source_type": doc.type,
        "os": doc.os,
        "phase": phase,
        "applies_to": applies_to,
        "normality": normality,
        "risk_level": risk_level,
        "confidence": confidence,
        "conditions": conditions,
        "evidence_requirements": collect_required_evidence(conditions),
        "result_if_matched": result_if_matched(normality, risk_level),
        **match_fields,
    }


def structured_rules(doc: Document) -> list[dict[str, Any]]:
    if doc.type not in RULE_SOURCE_TYPES:
        return []
    rules: list[dict[str, Any]] = []
    sections = section_by_heading(doc, STRUCTURED_RULE_HEADINGS)
    for section in sections:
        for parsed in parse_yaml_blocks(str(section.get("content", ""))):
            conditions = parsed.get("lifecycle_baseline") or parsed.get("rule_conditions") or parsed
            if not isinstance(conditions, dict):
                continue
            rules.append(make_rule(doc, "structured_lifecycle", len(rules) + 1, conditions))
    return rules


def relation_names(doc: Document) -> tuple[str, str]:
    parent = clean_link_text(doc.frontmatter.get("parent_process"))
    child = clean_link_text(doc.frontmatter.get("child_process"))
    if parent and child:
        return parent, child
    if "->" in doc.title:
        left, right = doc.title.split("->", 1)
        return left.strip(), right.strip()
    return parent, child


def section_lines(doc: Document, headings: set[str]) -> list[str]:
    lines: list[str] = []
    for section in section_by_heading(doc, headings):
        lines.extend(extract_fence_lines(str(section.get("content", ""))))
    return sorted(set(lines))


def infer_runtime_evidence(evidence_lines: list[str]) -> list[str]:
    found: set[str] = set()
    text = "\n".join(evidence_lines)
    for keyword, evidence_name in RUNTIME_EVIDENCE_KEYWORDS:
        if keyword in text:
            found.add(evidence_name)
    return sorted(found)


def derived_relation_rule(doc: Document) -> dict[str, Any] | None:
    parent, child = relation_names(doc)
    if not parent or not child:
        return None
    high_risk_terms = section_lines(doc, {"高风险参数", "高风险参数与命令行关注"})
    command_terms = extract_command_terms(high_risk_terms)
    evidence_lines = section_lines(doc, {"证据需求", "需要补充的证据"})
    conditions = {
        "version": 1,
        "applies_to": "process_relation",
        "phase": "creation",
        "creation": {
            "required_evidence": DEFAULT_CREATION_EVIDENCE,
            "parent_process_name": parent,
            "child_process_name": child,
            "expected_relation": doc.frontmatter.get("relation") or "spawn",
            "command_line_contains_any": command_terms,
            "high_risk_indicators": high_risk_terms,
        },
        "runtime": {
            "required_followup_evidence": infer_runtime_evidence(evidence_lines),
        },
        "source_text": {
            "high_risk_terms": high_risk_terms,
            "evidence_requirements": evidence_lines,
        },
    }
    return make_rule(doc, "derived_process_relation", 1, conditions)


def build_rules(docs: list[Document], include_derived_relation_rules: bool) -> list[dict[str, Any]]:
    rules: list[dict[str, Any]] = []
    for doc in docs:
        if doc.path.startswith("99_模板/"):
            continue
        explicit = structured_rules(doc)
        rules.extend(explicit)
        if include_derived_relation_rules and doc.type == "process_relation" and not explicit:
            derived = derived_relation_rule(doc)
            if derived:
                rules.append(derived)
    return rules


def cypher_escape(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def rule_cypher(rule: dict[str, Any]) -> str:
    props = {
        "rule_id": rule["rule_id"],
        "rule_name": rule["rule_name"],
        "rule_kind": rule["rule_kind"],
        "source_doc_id": rule["source_doc_id"],
        "source_path": rule["source_path"],
        "source_title": rule["source_title"],
        "source_type": rule["source_type"],
        "os": rule["os"],
        "phase": rule["phase"],
        "applies_to": rule["applies_to"],
        "normality": rule["normality"],
        "risk_level": rule["risk_level"],
        "confidence": rule["confidence"],
        "conditions_json": json_dumps(rule["conditions"]),
        "evidence_requirements": rule["evidence_requirements"],
        "result_if_matched": rule["result_if_matched"],
        "parent_process_names": rule["parent_process_names"],
        "child_process_names": rule["child_process_names"],
        "runtime_child_process_names": rule["runtime_child_process_names"],
        "command_line_terms": rule["command_line_terms"],
        "image_location_terms": rule["image_location_terms"],
        "runtime_indicators": rule["runtime_indicators"],
        "false_positive_contexts": rule["false_positive_contexts"],
    }
    prop_text = ", ".join(f"{key}: {cypher_escape(value)}" for key, value in props.items())
    return (
        f"MERGE (r:KbLifecycleRule {{rule_id: {cypher_escape(rule['rule_id'])}}})\n"
        f"SET r += {{{prop_text}}}\n"
        f"WITH r\n"
        f"OPTIONAL MATCH (d:KbDocument {{id: {cypher_escape(rule['source_doc_id'])}}})\n"
        f"WITH r, d\n"
        f"FOREACH (_ IN CASE WHEN d IS NULL THEN [] ELSE [1] END | "
        f"MERGE (d)-[:DEFINES_LIFECYCLE_RULE]->(r));"
    )


def render_cypher(rules: list[dict[str, Any]]) -> str:
    lines = [
        "// 终端应用安全基线画像库生命周期条件规则库",
        "// Generated by tools/kb_lifecycle_rules_to_cypher.py",
        "//",
        "// 查询时请区分知识库规则节点和 STIX 行为事实节点：",
        "//   规则节点: (:KbLifecycleRule)",
        "//   行为进程: (:Process) WHERE NOT p:KbDocument",
        "//",
        "// 示例：按进程创建关系匹配规则",
        "// MATCH (p:Process)-[:parent_ref]->(parent:Process)",
        "// WHERE NOT p:KbDocument AND NOT parent:KbDocument",
        "// WITH p, parent,",
        "//      toLower(last(split(replace(coalesce(p.image_path, ''), '\\\\', '/'), '/'))) AS child_name,",
        "//      toLower(last(split(replace(coalesce(parent.image_path, ''), '\\\\', '/'), '/'))) AS parent_name",
        "// MATCH (r:KbLifecycleRule {applies_to: 'process_relation', phase: 'creation'})",
        "// WHERE toLower(r.conditions_json) CONTAINS '\"parent_process_name\": \"' + parent_name + '\"'",
        "//   AND toLower(r.conditions_json) CONTAINS '\"child_process_name\": \"' + child_name + '\"'",
        "// RETURN p, parent, r.rule_name, r.risk_level, r.result_if_matched;",
        "",
        "CREATE CONSTRAINT kb_lifecycle_rule_id IF NOT EXISTS FOR (r:KbLifecycleRule) REQUIRE r.rule_id IS UNIQUE;",
        "CREATE INDEX kb_lifecycle_rule_phase IF NOT EXISTS FOR (r:KbLifecycleRule) ON (r.phase);",
        "CREATE INDEX kb_lifecycle_rule_applies_to IF NOT EXISTS FOR (r:KbLifecycleRule) ON (r.applies_to);",
        "CREATE INDEX kb_lifecycle_rule_source_path IF NOT EXISTS FOR (r:KbLifecycleRule) ON (r.source_path);",
        "",
    ]
    lines.extend(rule_cypher(rule) for rule in rules)
    return "\n".join(lines) + "\n"


ANALYSIS_QUERY_HEADER = """// STIX 行为事实图进程全生命周期条件判断查询模板
// Generated by tools/kb_lifecycle_rules_to_cypher.py
//
// 参数约定：
//   $process_key: 目标进程实例标识，可对应 process_key / stix_id / process_uid。
//   $lookback_ms / $lookahead_ms: 可选时间窗口。运行时证据若带 event_time / created_time，
//     必须落在目标进程 created_time 附近；缺少时间字段时保守保留为待上层继续核验。
//
// 结论边界：
//   创建时和运行时证据都齐全且可由规则解释，才允许上层服务收敛为 safe。
//   缺少任一关键证据时，上层服务应输出 evidence_insufficient。
"""

CREATION_RULE_QUERY = """// 1. 创建时规则匹配：父进程、子进程、命令行、路径上下文。
MATCH (p:Process)
WHERE NOT p:KbDocument
  AND ($process_key IS NULL OR p.process_key = $process_key OR p.stix_id = $process_key OR p.process_uid = $process_key)
OPTIONAL MATCH (p)-[:parent_ref]->(parent:Process)
WITH p, parent,
     toLower(last(split(replace(coalesce(p.image_path, p.name, p.process_name, ''), '\\\\', '/'), '/'))) AS child_name,
     toLower(last(split(replace(coalesce(parent.image_path, parent.name, parent.process_name, ''), '\\\\', '/'), '/'))) AS parent_name,
     toLower(coalesce(p.command_line, p.cmd_line, '')) AS command_line
MATCH (r:KbLifecycleRule)
WHERE r.phase IN ['creation', 'lifecycle']
  AND r.applies_to IN ['process_relation', 'process', 'process_behavior', 'security_baseline']
  AND (coalesce(r.parent_process_names, []) = [] OR parent_name IN r.parent_process_names)
  AND (coalesce(r.child_process_names, []) = [] OR child_name IN r.child_process_names)
WITH p, parent, child_name, parent_name, r, command_line,
     [term IN coalesce(r.command_line_terms, []) WHERE command_line CONTAINS toLower(term)] AS matched_command_terms
RETURN p, parent, child_name, parent_name,
       collect({
         rule_id: r.rule_id,
         rule_name: r.rule_name,
         source_path: r.source_path,
         risk_level: r.risk_level,
         normality: r.normality,
         result_if_matched: r.result_if_matched,
         matched_command_terms: matched_command_terms,
         evidence_requirements: r.evidence_requirements
       }) AS creation_rule_matches;
"""

RUNTIME_EVIDENCE_QUERY = """// 2. 运行时证据摘要：子进程、网络、文件、注册表/配置证据面。
MATCH (p:Process)
WHERE NOT p:KbDocument
  AND ($process_key IS NULL OR p.process_key = $process_key OR p.stix_id = $process_key OR p.process_uid = $process_key)
WITH p,
     coalesce($lookback_ms, 0) AS lookback_ms,
     coalesce($lookahead_ms, 3600000) AS lookahead_ms,
     coalesce(p.created_time, p.create_time, p.start_time, 0) AS process_time
OPTIONAL MATCH (child:Process)-[:parent_ref]->(p)
OPTIONAL MATCH (net_obs:ObservedData)-[:x_subject_process]->(p)
OPTIONAL MATCH (net_obs)-[:x_network_flow]->(net:NetworkTraffic)
OPTIONAL MATCH (file_obs:ObservedData)-[:x_subject_process]->(p)
OPTIONAL MATCH (file_obs)-[:x_target_file]->(file:File)
OPTIONAL MATCH (reg_obs:ObservedData)-[:x_subject_process]->(p)
OPTIONAL MATCH (reg_obs)-[:x_target_registry_key]->(reg:RegistryKey)
WITH p, process_time, lookback_ms, lookahead_ms,
     [item IN collect(DISTINCT CASE
       WHEN child IS NOT NULL
            AND (
              coalesce(child.created_time, child.create_time, child.start_time, 0) = 0
              OR process_time = 0
              OR (
                coalesce(child.created_time, child.create_time, child.start_time, 0) >= process_time - lookback_ms
                AND coalesce(child.created_time, child.create_time, child.start_time, 0) <= process_time + lookahead_ms
              )
            )
         THEN child
       ELSE null
     END) WHERE item IS NOT NULL] AS children,
     [item IN collect(DISTINCT CASE
       WHEN net IS NOT NULL
            AND (
              coalesce(net_obs.event_time, 0) = 0
              OR process_time = 0
              OR (net_obs.event_time >= process_time - lookback_ms AND net_obs.event_time <= process_time + lookahead_ms)
            )
         THEN net
       ELSE null
     END) WHERE item IS NOT NULL] AS direct_networks,
     [item IN collect(DISTINCT CASE
       WHEN file IS NOT NULL
            AND (
              coalesce(file_obs.event_time, 0) = 0
              OR process_time = 0
              OR (file_obs.event_time >= process_time - lookback_ms AND file_obs.event_time <= process_time + lookahead_ms)
            )
         THEN file
       ELSE null
     END) WHERE item IS NOT NULL] AS files,
     [item IN collect(DISTINCT CASE
       WHEN reg IS NOT NULL
            AND (
              coalesce(reg_obs.event_time, 0) = 0
              OR process_time = 0
              OR (reg_obs.event_time >= process_time - lookback_ms AND reg_obs.event_time <= process_time + lookahead_ms)
            )
         THEN reg
       ELSE null
     END) WHERE item IS NOT NULL] AS registry_keys
WITH p, children, direct_networks, files, registry_keys,
     [c IN children | toLower(last(split(replace(coalesce(c.image_path, c.name, c.process_name, ''), '\\\\', '/'), '/')))] AS child_names
OPTIONAL MATCH (r:KbLifecycleRule)
WHERE r.phase IN ['runtime', 'lifecycle']
WITH p, children, direct_networks, files, registry_keys, child_names, r,
     [indicator IN coalesce(r.runtime_indicators, [])
      WHERE
        (size(direct_networks) > 0 AND indicator IN [
          'network_connection', 'network_connections', 'network_after_spawn',
          'network_after_install', 'abnormal_external_connection', 'lateral_movement'
        ])
        OR (size(files) > 0 AND indicator IN [
          'file_write', 'file_activity', 'file_drop_after_spawn',
          'downloaded_file', 'sensitive_file_access', 'data_archive'
        ])
        OR (size(registry_keys) > 0 AND indicator IN [
          'registry_activity', 'registry_or_config_activity', 'persistence_change',
          'persistence_changes', 'persistence_after_spawn', 'persistence_write',
          'service_creation', 'scheduled_task_change', 'run_key_change'
        ])
        OR (size(children) > 0 AND indicator IN ['child_processes', 'unknown_child_process'])
     ] AS matched_runtime_indicators
WITH p, children, direct_networks, files, registry_keys, child_names,
     collect(
       CASE
         WHEN r IS NULL THEN null
         WHEN coalesce(r.runtime_child_process_names, []) <> []
              AND any(name IN child_names WHERE name IN r.runtime_child_process_names)
           THEN {
             rule_id: r.rule_id,
             rule_name: r.rule_name,
             source_path: r.source_path,
             risk_level: r.risk_level,
             normality: r.normality,
             matched_runtime_indicators: matched_runtime_indicators,
             evidence_requirements: r.evidence_requirements
           }
         WHEN matched_runtime_indicators <> []
           THEN {
             rule_id: r.rule_id,
             rule_name: r.rule_name,
             source_path: r.source_path,
             risk_level: r.risk_level,
             normality: r.normality,
             matched_runtime_indicators: matched_runtime_indicators,
             evidence_requirements: r.evidence_requirements
           }
         ELSE null
       END
     ) AS raw_runtime_rule_matches
RETURN p,
       size(children) AS child_process_count,
       size(direct_networks) AS direct_network_count,
       size(files) AS related_file_count,
       size(registry_keys) AS related_registry_count,
       child_names,
       [item IN raw_runtime_rule_matches WHERE item IS NOT NULL] AS runtime_rule_matches;
"""

EVIDENCE_COMPLETENESS_QUERY = """// 3. 证据完整性骨架：上层服务可按本结果收敛 lifecycle_result。
MATCH (p:Process)
WHERE NOT p:KbDocument
  AND ($process_key IS NULL OR p.process_key = $process_key OR p.stix_id = $process_key OR p.process_uid = $process_key)
WITH p,
     coalesce($lookback_ms, 0) AS lookback_ms,
     coalesce($lookahead_ms, 3600000) AS lookahead_ms,
     coalesce(p.created_time, p.create_time, p.start_time, 0) AS process_time
OPTIONAL MATCH (p)-[:parent_ref]->(parent:Process)
OPTIONAL MATCH (creation_obs:ObservedData)-[:x_created_process]->(p)
OPTIONAL MATCH (creation_obs)-[:x_actor_user]->(user:UserAccount)
OPTIONAL MATCH (child:Process)-[:parent_ref]->(p)
OPTIONAL MATCH (net_obs:ObservedData)-[:x_subject_process]->(p)
OPTIONAL MATCH (net_obs)-[:x_network_flow]->(net:NetworkTraffic)
OPTIONAL MATCH (file_obs:ObservedData)-[:x_subject_process]->(p)
OPTIONAL MATCH (file_obs)-[:x_target_file]->(file:File)
OPTIONAL MATCH (reg_obs:ObservedData)-[:x_subject_process]->(p)
OPTIONAL MATCH (reg_obs)-[:x_target_registry_key]->(reg:RegistryKey)
WITH p, parent, process_time, lookback_ms, lookahead_ms,
     collect(DISTINCT user) AS users,
     [item IN collect(DISTINCT CASE
       WHEN child IS NOT NULL
            AND (
              coalesce(child.created_time, child.create_time, child.start_time, 0) = 0
              OR process_time = 0
              OR (
                coalesce(child.created_time, child.create_time, child.start_time, 0) >= process_time - lookback_ms
                AND coalesce(child.created_time, child.create_time, child.start_time, 0) <= process_time + lookahead_ms
              )
            )
         THEN child
       ELSE null
     END) WHERE item IS NOT NULL] AS children,
     [item IN collect(DISTINCT CASE
       WHEN net IS NOT NULL
            AND (
              coalesce(net_obs.event_time, 0) = 0
              OR process_time = 0
              OR (net_obs.event_time >= process_time - lookback_ms AND net_obs.event_time <= process_time + lookahead_ms)
            )
         THEN net
       ELSE null
     END) WHERE item IS NOT NULL] AS direct_networks,
     [item IN collect(DISTINCT CASE
       WHEN file IS NOT NULL
            AND (
              coalesce(file_obs.event_time, 0) = 0
              OR process_time = 0
              OR (file_obs.event_time >= process_time - lookback_ms AND file_obs.event_time <= process_time + lookahead_ms)
            )
         THEN file
       ELSE null
     END) WHERE item IS NOT NULL] AS files,
     [item IN collect(DISTINCT CASE
       WHEN reg IS NOT NULL
            AND (
              coalesce(reg_obs.event_time, 0) = 0
              OR process_time = 0
              OR (reg_obs.event_time >= process_time - lookback_ms AND reg_obs.event_time <= process_time + lookahead_ms)
            )
         THEN reg
       ELSE null
     END) WHERE item IS NOT NULL] AS registry_keys
WITH p, parent, users, children, direct_networks, files, registry_keys,
     (size(users) > 0 OR toString(coalesce(p.user_name, p.user_id, p.user_domain, '')) <> '') AS has_user,
     (
       size(children) > 0
       OR size(direct_networks) > 0
       OR size(files) > 0
       OR size(registry_keys) > 0
     ) AS has_runtime_evidence
RETURN p,
       parent IS NOT NULL AS has_parent_process,
       coalesce(p.image_path, p.file_path, '') <> '' AS has_image_path,
       coalesce(p.command_line, p.cmd_line, '') <> '' AS has_command_line,
       has_user,
       size(children) > 0 AS has_child_process_evidence,
       size(direct_networks) > 0 AS has_network_evidence,
       size(files) > 0 AS has_file_evidence,
       size(registry_keys) > 0 AS has_registry_evidence,
       CASE
         WHEN parent IS NULL OR coalesce(p.image_path, p.file_path, '') = ''
              OR coalesce(p.command_line, p.cmd_line, '') = '' OR NOT has_user
           THEN 'evidence_insufficient'
         WHEN NOT has_runtime_evidence
           THEN 'evidence_insufficient'
         ELSE 'lifecycle_evidence_present'
       END AS lifecycle_evidence_result;
"""


def render_analysis_queries() -> str:
    return "\n\n".join(
        [
            ANALYSIS_QUERY_HEADER,
            CREATION_RULE_QUERY,
            RUNTIME_EVIDENCE_QUERY,
            EVIDENCE_COMPLETENESS_QUERY,
        ]
    )


def write_jsonl(rules: list[dict[str, Any]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        for rule in rules:
            handle.write(json.dumps(rule, ensure_ascii=False, sort_keys=True, default=str) + "\n")


def write_cypher(rules: list[dict[str, Any]], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_cypher(rules), encoding="utf-8")


def write_analysis_queries(out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_analysis_queries(), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    configure_logging(args.debug, args.log_file)
    docs = load_documents(Path(args.vault))
    rules = build_rules(docs, include_derived_relation_rules=not args.no_derived_relation_rules)
    write_jsonl(rules, Path(args.out_jsonl))
    write_cypher(rules, Path(args.out_cypher))
    write_analysis_queries(Path(args.out_query_cypher))
    by_kind: dict[str, int] = {}
    for rule in rules:
        by_kind[rule["rule_kind"]] = by_kind.get(rule["rule_kind"], 0) + 1
    print(
        f"rules={len(rules)} kinds={json.dumps(by_kind, ensure_ascii=False, sort_keys=True)} "
        f"jsonl={args.out_jsonl} cypher={args.out_cypher} query_cypher={args.out_query_cypher}"
    )
    return 1 if args.strict and not rules else 0


if __name__ == "__main__":
    raise SystemExit(main())
