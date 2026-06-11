#!/usr/bin/env python3
"""Convert the Windows App Security Baseline Obsidian vault to SQLite.

Examples:
  python tools/kb_to_sqlite.py --vault kb --out out/windows_app_baseline.db --rebuild --debug
  python tools/kb_to_sqlite.py --vault kb --out out/windows_app_baseline.db --export-jsonl out/documents.jsonl
"""
from __future__ import annotations

import argparse
import json
import logging
import sqlite3
import sys
from pathlib import Path
from typing import Any

try:
    from .wabk_common import (
        Document,
        build_title_index,
        configure_logging,
        json_dumps,
        load_documents,
        now_iso,
        open_sqlite,
        resolve_link,
    )
except ImportError:  # allow running as: python tools/kb_to_sqlite.py
    from wabk_common import (
        Document,
        build_title_index,
        configure_logging,
        json_dumps,
        load_documents,
        now_iso,
        open_sqlite,
        resolve_link,
    )

LOG = logging.getLogger("wabk.sqlite")


def create_schema(conn: sqlite3.Connection) -> None:
    LOG.debug("create SQLite schema")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            path TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            os TEXT NOT NULL,
            name TEXT,
            frontmatter_json TEXT NOT NULL,
            body TEXT NOT NULL,
            body_text TEXT NOT NULL,
            raw_markdown TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            mtime TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            tags_json TEXT NOT NULL,
            aliases_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS entities (
            id TEXT PRIMARY KEY,
            doc_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
            entity_type TEXT NOT NULL,
            name TEXT NOT NULL,
            app_id TEXT,
            service_name TEXT,
            process_name TEXT,
            vendor TEXT,
            category TEXT,
            risk_level TEXT,
            confidence TEXT,
            path TEXT NOT NULL,
            frontmatter_json TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS sections (
            id TEXT PRIMARY KEY,
            doc_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
            level INTEGER NOT NULL,
            heading TEXT NOT NULL,
            content TEXT NOT NULL,
            content_text TEXT NOT NULL,
            sort_order INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS links (
            id TEXT PRIMARY KEY,
            source_doc_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
            source_path TEXT NOT NULL,
            target_text TEXT NOT NULL,
            target_doc_id TEXT REFERENCES documents(id) ON DELETE SET NULL,
            target_resolved INTEGER NOT NULL,
            raw_link TEXT NOT NULL,
            context_heading TEXT,
            line_no INTEGER,
            line_text TEXT
        );

        CREATE TABLE IF NOT EXISTS tags (
            tag TEXT NOT NULL,
            doc_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
            PRIMARY KEY(tag, doc_id)
        );

        CREATE TABLE IF NOT EXISTS frontmatter_kv (
            doc_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
            key TEXT NOT NULL,
            value_json TEXT NOT NULL,
            value_text TEXT,
            PRIMARY KEY(doc_id, key)
        );

        CREATE INDEX IF NOT EXISTS idx_documents_type ON documents(type);
        CREATE INDEX IF NOT EXISTS idx_documents_os ON documents(os);
        CREATE INDEX IF NOT EXISTS idx_documents_title ON documents(title);
        CREATE INDEX IF NOT EXISTS idx_entities_type_name ON entities(entity_type, name);
        CREATE INDEX IF NOT EXISTS idx_entities_service ON entities(service_name);
        CREATE INDEX IF NOT EXISTS idx_entities_process ON entities(process_name);
        CREATE INDEX IF NOT EXISTS idx_links_source ON links(source_doc_id);
        CREATE INDEX IF NOT EXISTS idx_links_target ON links(target_doc_id);
        CREATE INDEX IF NOT EXISTS idx_sections_doc ON sections(doc_id);
        """
    )
    try:
        conn.execute(
            "CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5("
            "doc_id UNINDEXED, title, path, type, name, body_text, frontmatter_json, tokenize='unicode61')"
        )
        LOG.debug("FTS5 virtual table enabled")
    except sqlite3.OperationalError as exc:
        LOG.warning("FTS5 is not available in this SQLite build: %s", exc)


def clear_schema(conn: sqlite3.Connection) -> None:
    LOG.debug("clear old rows")
    for table in ["documents_fts", "frontmatter_kv", "tags", "links", "sections", "entities", "documents", "metadata"]:
        try:
            conn.execute(f"DELETE FROM {table}")
        except sqlite3.OperationalError:
            LOG.debug("table not found while clearing: %s", table)


def _value_text(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    if value is None:
        return ""
    return str(value)


def insert_documents(conn: sqlite3.Connection, docs: list[Document]) -> None:
    LOG.info("insert %d documents", len(docs))
    title_index = build_title_index(docs)
    for doc in docs:
        LOG.debug("insert document path=%s type=%s title=%s", doc.path, doc.type, doc.title)
        conn.execute(
            """
            INSERT INTO documents(id,path,title,type,os,name,frontmatter_json,body,body_text,raw_markdown,sha256,mtime,word_count,tags_json,aliases_json)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                doc.id,
                doc.path,
                doc.title,
                doc.type,
                doc.os,
                doc.name,
                json_dumps(doc.frontmatter),
                doc.body,
                doc.body_text,
                doc.raw,
                doc.sha256,
                doc.mtime,
                len(doc.body_text.split()),
                json_dumps(doc.tags),
                json_dumps(doc.aliases),
            ),
        )
        conn.execute(
            """
            INSERT INTO entities(id,doc_id,entity_type,name,app_id,service_name,process_name,vendor,category,risk_level,confidence,path,frontmatter_json)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                f"ent_{doc.id}",
                doc.id,
                doc.type,
                doc.name,
                doc.frontmatter.get("app_id"),
                doc.frontmatter.get("service_name"),
                doc.frontmatter.get("process_name"),
                doc.frontmatter.get("vendor") or doc.frontmatter.get("vendor_name"),
                doc.frontmatter.get("category"),
                doc.frontmatter.get("risk_level"),
                doc.frontmatter.get("confidence"),
                doc.path,
                json_dumps(doc.frontmatter),
            ),
        )
        for i, sec in enumerate(doc.sections, start=1):
            conn.execute(
                "INSERT INTO sections(id,doc_id,level,heading,content,content_text,sort_order) VALUES(?,?,?,?,?,?,?)",
                (f"sec_{doc.id}_{i:04d}", doc.id, sec["level"], sec["heading"], sec["content"], sec["content_text"], sec["sort_order"]),
            )
        for tag in doc.tags:
            conn.execute("INSERT OR IGNORE INTO tags(tag,doc_id) VALUES(?,?)", (tag, doc.id))
        for key, value in doc.frontmatter.items():
            conn.execute(
                "INSERT OR REPLACE INTO frontmatter_kv(doc_id,key,value_json,value_text) VALUES(?,?,?,?)",
                (doc.id, key, json_dumps(value), _value_text(value)),
            )
    # Insert links after all document nodes are present, otherwise resolved target_doc_id
    # may violate the foreign key while the target document has not been inserted yet.
    LOG.debug("insert Obsidian links after document/entity rows")
    for doc in docs:
        for i, occ in enumerate(doc.link_occurrences, start=1):
            target_doc_id = resolve_link(occ["target_text"], title_index)
            conn.execute(
                """
                INSERT INTO links(id,source_doc_id,source_path,target_text,target_doc_id,target_resolved,raw_link,context_heading,line_no,line_text)
                VALUES(?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    f"lnk_{doc.id}_{i:04d}",
                    doc.id,
                    doc.path,
                    occ["target_text"],
                    target_doc_id,
                    1 if target_doc_id else 0,
                    occ["raw_link"],
                    occ.get("context_heading"),
                    occ.get("line_no"),
                    occ.get("line_text"),
                ),
            )
    # Populate FTS, if available.
    try:
        LOG.debug("populate FTS index")
        conn.execute("DELETE FROM documents_fts")
        conn.execute(
            """
            INSERT INTO documents_fts(doc_id,title,path,type,name,body_text,frontmatter_json)
            SELECT id,title,path,type,name,body_text,frontmatter_json FROM documents
            """
        )
    except sqlite3.OperationalError as exc:
        LOG.warning("skip FTS population: %s", exc)


def insert_metadata(conn: sqlite3.Connection, docs: list[Document], vault: Path) -> None:
    rows = {
        "generated_at": now_iso(),
        "vault_path": str(vault.resolve()),
        "document_count": str(len(docs)),
        "tool": "kb_to_sqlite.py",
        "schema_version": "1.1.0",
    }
    for k, v in rows.items():
        conn.execute("INSERT OR REPLACE INTO metadata(key,value) VALUES(?,?)", (k, v))


def export_jsonl(docs: list[Document], out: Path) -> None:
    LOG.info("export jsonl: %s", out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for doc in docs:
            row = {
                "id": doc.id,
                "path": doc.path,
                "title": doc.title,
                "type": doc.type,
                "os": doc.os,
                "name": doc.name,
                "frontmatter": doc.frontmatter,
                "tags": doc.tags,
                "aliases": doc.aliases,
                "links": doc.links,
                "body_text": doc.body_text,
            }
            f.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")


def build_sqlite(vault: Path, out: Path, rebuild: bool, export_jsonl_path: Path | None) -> None:
    docs = load_documents(vault)
    conn = open_sqlite(out)
    try:
        create_schema(conn)
        if rebuild:
            clear_schema(conn)
        with conn:
            insert_documents(conn, docs)
            insert_metadata(conn, docs, vault)
        if export_jsonl_path:
            export_jsonl(docs, export_jsonl_path)
        LOG.info("SQLite build finished: %s", out)
        LOG.info("stats documents=%d links=%d", len(docs), sum(len(d.link_occurrences) for d in docs))
    finally:
        conn.close()


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Convert Windows App Security Baseline Markdown vault to SQLite.")
    p.add_argument("--vault", default="kb", help="Obsidian vault root path (knowledge base)")
    p.add_argument("--out", default="out/windows_app_baseline.db", help="Output SQLite database path")
    p.add_argument("--rebuild", action="store_true", help="Clear existing rows before import")
    p.add_argument("--export-jsonl", default=None, help="Optional JSONL export path")
    p.add_argument("--debug", action="store_true", help="Enable debug logs")
    p.add_argument("--log-file", default=None, help="Write logs to file as well as stderr")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    configure_logging(args.debug, args.log_file)
    build_sqlite(Path(args.vault), Path(args.out), args.rebuild, Path(args.export_jsonl) if args.export_jsonl else None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
