#!/usr/bin/env python3
"""Run lifecycle-rule smoke checks against a Neo4j behavior graph fixture."""
from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


DEFAULT_IMAGE = "neo4j:5-community"
DEFAULT_DATABASE = "neo4j"
DEFAULT_LOOKAHEAD_MS = 60 * 60 * 1000
PROCESS_KEY_FULL = "proc-office-neo4j-full"
PROCESS_KEY_EARLY = "proc-office-neo4j-early"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Neo4j lifecycle-rule end-to-end smoke checks.")
    parser.add_argument("--rules-cypher", default="out/lifecycle_rules.cypher", help="Lifecycle rule Cypher file")
    parser.add_argument(
        "--query-cypher",
        default="out/lifecycle_analysis_queries.cypher",
        help="Generated lifecycle analysis query template file",
    )
    parser.add_argument("--out", default="out/lifecycle_neo4j_e2e_smoke.json", help="Smoke report JSON path")
    parser.add_argument("--uri", default=None, help="Existing Neo4j Bolt URI. If omitted, a Docker container is used")
    parser.add_argument("--user", default="neo4j", help="Neo4j username for existing instances")
    parser.add_argument("--password", default="", help="Neo4j password for existing instances")
    parser.add_argument("--database", default=DEFAULT_DATABASE, help="Neo4j database")
    parser.add_argument("--image", default=DEFAULT_IMAGE, help="Docker image used when --uri is omitted")
    parser.add_argument("--container-name", default=None, help="Optional Docker container name")
    parser.add_argument("--bolt-port", type=int, default=57687, help="Preferred host Bolt port for Docker mode")
    parser.add_argument("--http-port", type=int, default=57474, help="Preferred host HTTP port for Docker mode")
    parser.add_argument("--keep-container", action="store_true", help="Keep the temporary Docker container")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if checks fail")
    return parser.parse_args(argv)


def import_graph_driver() -> Any:
    try:
        from neo4j import GraphDatabase  # type: ignore
    except ImportError as exc:
        raise RuntimeError("neo4j Python driver is not installed. Run: uv pip install -r tools/requirements.txt") from exc
    return GraphDatabase


def is_port_available(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.2)
        return sock.connect_ex(("127.0.0.1", port)) != 0


def choose_port(preferred: int) -> int:
    if is_port_available(preferred):
        return preferred
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def run_command(args: list[str]) -> str:
    completed = subprocess.run(args, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return completed.stdout.strip()


def start_docker(args: argparse.Namespace) -> tuple[str, str]:
    bolt_port = choose_port(args.bolt_port)
    http_port = choose_port(args.http_port)
    name = args.container_name or f"common-app-baseline-neo4j-smoke-{int(time.time())}"
    run_command(
        [
            "docker",
            "run",
            "--rm",
            "-d",
            "--name",
            name,
            "--log-driver",
            "none",
            "--tmpfs",
            "/data:rw,size=2g",
            "--tmpfs",
            "/logs:rw,size=256m",
            "--tmpfs",
            "/tmp:rw,size=512m",
            "-p",
            f"127.0.0.1:{bolt_port}:7687",
            "-p",
            f"127.0.0.1:{http_port}:7474",
            "-e",
            "NEO4J_AUTH=none",
            args.image,
        ]
    )
    return name, f"bolt://127.0.0.1:{bolt_port}"


def stop_docker(name: str | None, keep: bool) -> None:
    if name and not keep:
        subprocess.run(["docker", "stop", name], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def wait_for_neo4j(uri: str, user: str, password: str, database: str, timeout: int = 240) -> None:
    GraphDatabase = import_graph_driver()
    deadline = time.time() + timeout
    last_error: Exception | None = None
    while time.time() < deadline:
        try:
            auth = (user, password) if password else None
            with GraphDatabase.driver(uri, auth=auth) as driver:
                driver.verify_connectivity()
                with driver.session(database=database) as session:
                    session.run("RETURN 1 AS ok").consume()
            return
        except Exception as exc:  # pragma: no cover - depends on local service timing
            last_error = exc
            time.sleep(2)
    raise RuntimeError(f"Neo4j is not ready at {uri}: {last_error}")


def split_cypher_statements(text: str) -> list[str]:
    statements: list[str] = []
    buffer: list[str] = []
    for line in text.splitlines():
        buffer.append(line)
        stripped = line.strip()
        if stripped.endswith(";") and not stripped.startswith("//"):
            statement = "\n".join(buffer).rstrip()
            statements.append(statement[:-1].strip())
            buffer = []
    tail = "\n".join(buffer).strip()
    if tail:
        statements.append(tail)
    return [item for item in statements if item and not item.lstrip().startswith("// Generated only")]


def run_statements(session: Any, statements: list[str]) -> None:
    for statement in statements:
        session.run(statement).consume()


def load_queries(path: Path) -> dict[str, str]:
    statements = split_cypher_statements(path.read_text(encoding="utf-8"))
    if len(statements) < 3:
        raise ValueError(f"expected at least 3 query statements in {path}, got {len(statements)}")
    return {"creation": statements[0], "runtime": statements[1], "evidence": statements[2]}


def cleanup_smoke_graph(session: Any, smoke_id: str) -> None:
    session.run("MATCH (n {smoke_id: $smoke_id}) DETACH DELETE n", smoke_id=smoke_id).consume()


def create_fixture(session: Any, smoke_id: str, process_key: str, base_time: int, runtime_delta: int) -> None:
    session.run(
        """
        MERGE (parent:Process {process_key: $parent_key})
        SET parent += {
          smoke_id: $smoke_id,
          stix_id: $parent_stix_id,
          process_uid: $parent_uid,
          name: 'WINWORD.EXE',
          process_name: 'WINWORD.EXE',
          image_path: 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE',
          file_path: 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE',
          created_time: $parent_time,
          create_time: $parent_time,
          start_time: $parent_time
        }
        MERGE (p:Process {process_key: $process_key})
        SET p += {
          smoke_id: $smoke_id,
          stix_id: $process_stix_id,
          process_uid: $process_uid,
          name: 'powershell.exe',
          process_name: 'powershell.exe',
          image_path: 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe',
          file_path: 'C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe',
          command_line: 'powershell.exe -NoProfile -EncodedCommand SQBFAFgA',
          cmd_line: 'powershell.exe -NoProfile -EncodedCommand SQBFAFgA',
          user_name: 'alice',
          user_id: 'S-1-5-21-1000',
          user_domain: 'CONTOSO',
          created_time: $base_time,
          create_time: $base_time,
          start_time: $base_time
        }
        MERGE (p)-[:parent_ref]->(parent)
        MERGE (u:UserAccount {user_key: $user_key})
        SET u += {smoke_id: $smoke_id, user_name: 'alice'}
        MERGE (creation:ObservedData {event_uid: $creation_uid})
        SET creation += {smoke_id: $smoke_id, event_time: $base_time, event_code: 'es_process_creation'}
        MERGE (creation)-[:x_created_process]->(p)
        MERGE (creation)-[:x_actor_user]->(u)
        """,
        smoke_id=smoke_id,
        parent_key=f"{process_key}-parent",
        parent_stix_id=f"process--{process_key}-parent",
        parent_uid=f"{process_key}-parent-uid",
        process_key=process_key,
        process_stix_id=f"process--{process_key}",
        process_uid=f"{process_key}-uid",
        parent_time=base_time - 100,
        base_time=base_time,
        user_key=f"{process_key}-user",
        creation_uid=f"{process_key}-creation",
    ).consume()
    create_runtime_fixture(session, smoke_id, process_key, base_time + runtime_delta)


def create_runtime_fixture(session: Any, smoke_id: str, process_key: str, event_time: int) -> None:
    session.run(
        """
        MATCH (p:Process {process_key: $process_key})
        MERGE (net:NetworkTraffic {stix_id: $net_id})
        SET net += {smoke_id: $smoke_id, dst_ref_value: '203.0.113.10', dst_port: 443}
        MERGE (file:File {stix_id: $file_id})
        SET file += {smoke_id: $smoke_id, path: 'C:\\Users\\alice\\AppData\\Local\\Temp\\stage.ps1'}
        MERGE (reg:RegistryKey {stix_id: $reg_id})
        SET reg += {smoke_id: $smoke_id, key: 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'}
        MERGE (net_obs:ObservedData {event_uid: $net_obs_id})
        SET net_obs += {smoke_id: $smoke_id, event_time: $event_time, event_code: 'es_network_connection'}
        MERGE (file_obs:ObservedData {event_uid: $file_obs_id})
        SET file_obs += {smoke_id: $smoke_id, event_time: $event_time, event_code: 'es_file_access'}
        MERGE (reg_obs:ObservedData {event_uid: $reg_obs_id})
        SET reg_obs += {smoke_id: $smoke_id, event_time: $event_time, event_code: 'es_registry_set'}
        MERGE (net_obs)-[:x_subject_process]->(p)
        MERGE (net_obs)-[:x_network_flow]->(net)
        MERGE (file_obs)-[:x_subject_process]->(p)
        MERGE (file_obs)-[:x_target_file]->(file)
        MERGE (reg_obs)-[:x_subject_process]->(p)
        MERGE (reg_obs)-[:x_target_registry_key]->(reg)
        """,
        smoke_id=smoke_id,
        process_key=process_key,
        event_time=event_time,
        net_id=f"{process_key}-net",
        file_id=f"{process_key}-file",
        reg_id=f"{process_key}-reg",
        net_obs_id=f"{process_key}-net-obs",
        file_obs_id=f"{process_key}-file-obs",
        reg_obs_id=f"{process_key}-reg-obs",
    ).consume()


def create_interference_node(session: Any, smoke_id: str) -> None:
    session.run(
        """
        MERGE (p:KbDocument:Process {process_key: $process_key})
        SET p += {smoke_id: $smoke_id, image_path: 'C:\\Fake\\powershell.exe'}
        """,
        smoke_id=smoke_id,
        process_key=PROCESS_KEY_FULL,
    ).consume()


def run_analysis(session: Any, queries: dict[str, str], process_key: str) -> dict[str, Any]:
    params = {"process_key": process_key, "lookback_ms": 0, "lookahead_ms": DEFAULT_LOOKAHEAD_MS}
    creation = session.run(queries["creation"], **params).data()
    runtime = session.run(queries["runtime"], **params).data()
    evidence = session.run(queries["evidence"], **params).data()
    return {
        "process_key": process_key,
        "creation": creation,
        "runtime": runtime,
        "evidence": evidence,
        "lifecycle_result": lifecycle_result(creation, runtime, evidence),
    }


def lifecycle_result(creation: list[dict[str, Any]], runtime: list[dict[str, Any]], evidence: list[dict[str, Any]]) -> str:
    if not evidence or evidence[0].get("lifecycle_evidence_result") == "evidence_insufficient":
        return "evidence_insufficient"
    creation_matches = creation[0].get("creation_rule_matches") if creation else []
    runtime_matches = runtime[0].get("runtime_rule_matches") if runtime else []
    if not creation_matches or not runtime_matches:
        return "baseline_gap"
    if any(item.get("result_if_matched") == "risky" for item in creation_matches):
        return "risky"
    return "safe"


def count_rules(session: Any) -> int:
    record = session.run("MATCH (r:KbLifecycleRule) RETURN count(r) AS count").single()
    return int(record["count"]) if record else 0


def build_checks(report: dict[str, Any]) -> dict[str, bool]:
    full = report["results"][PROCESS_KEY_FULL]
    early = report["results"][PROCESS_KEY_EARLY]
    full_creation = full["creation"][0] if full["creation"] else {}
    full_runtime = full["runtime"][0] if full["runtime"] else {}
    early_evidence = early["evidence"][0] if early["evidence"] else {}
    return {
        "rules_imported": report["rule_count"] > 0,
        "full_has_single_process_row": len(full["creation"]) == 1,
        "full_has_creation_rule": bool(full_creation.get("creation_rule_matches")),
        "full_has_runtime_rule": bool(full_runtime.get("runtime_rule_matches")),
        "full_lifecycle_risky": full["lifecycle_result"] == "risky",
        "early_runtime_outside_window": early_evidence.get("lifecycle_evidence_result") == "evidence_insufficient",
        "kb_document_process_excluded": len(full["creation"]) == 1,
    }


def run_smoke(args: argparse.Namespace, uri: str, smoke_id: str) -> dict[str, Any]:
    GraphDatabase = import_graph_driver()
    auth = (args.user, args.password) if args.password else None
    queries = load_queries(Path(args.query_cypher))
    with GraphDatabase.driver(uri, auth=auth) as driver:
        with driver.session(database=args.database) as session:
            cleanup_smoke_graph(session, smoke_id)
            run_statements(session, split_cypher_statements(Path(args.rules_cypher).read_text(encoding="utf-8")))
            create_fixture(session, smoke_id, PROCESS_KEY_FULL, 1_700_000_000_000, 10_000)
            create_fixture(session, smoke_id, PROCESS_KEY_EARLY, 1_700_000_000_000, -90_000)
            create_interference_node(session, smoke_id)
            report = {
                "uri": uri,
                "database": args.database,
                "rule_count": count_rules(session),
                "results": {
                    PROCESS_KEY_FULL: run_analysis(session, queries, PROCESS_KEY_FULL),
                    PROCESS_KEY_EARLY: run_analysis(session, queries, PROCESS_KEY_EARLY),
                },
            }
            report["checks"] = build_checks(report)
            report["passed"] = all(report["checks"].values())
            cleanup_smoke_graph(session, smoke_id)
            return report


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    container_name: str | None = None
    uri = args.uri
    try:
        if not uri:
            container_name, uri = start_docker(args)
            args.password = ""
        wait_for_neo4j(uri, args.user, args.password, args.database)
        report = run_smoke(args, uri, f"lifecycle-neo4j-smoke-{int(time.time())}")
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str), encoding="utf-8")
        print(f"passed={report['passed']} rules={report['rule_count']} uri={uri} out={args.out}")
        return 1 if args.strict and not report["passed"] else 0
    finally:
        stop_docker(container_name, args.keep_container)


if __name__ == "__main__":
    raise SystemExit(main())
