#!/usr/bin/env python3
"""FastAPI search service for the Windows App Security Baseline SQLite DB.

Features:
- Exact match search by title/name/path/service/process/vendor/type/tag.
- Fuzzy search over title/name/path/body text.
- Full-text search via SQLite FTS5 when available, fallback to LIKE.
- Verbose debug logs for query parsing, SQL, result ranking and errors.

Run:
  python tools/api_service.py --db out/windows_app_baseline.db --host 0.0.0.0 --port 8000 --debug

API examples:
  GET /health
  GET /stats
  GET /search?q=chrome&mode=fuzzy&limit=20
  GET /search?q=Google Chrome&mode=exact&type=app
  GET /documents/{doc_id}
"""
from __future__ import annotations

import argparse
import difflib
import json
import logging
import sqlite3
import sys
from pathlib import Path
from typing import Any

try:
    from .wabk_common import configure_logging
except ImportError:  # allow running as: python tools/api_service.py
    from wabk_common import configure_logging

LOG = logging.getLogger("wabk.api")

try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.middleware.cors import CORSMiddleware
    import uvicorn
except Exception as exc:  # pragma: no cover
    raise SystemExit("Missing dependencies. Run: pip install fastapi uvicorn") from exc

try:
    from rapidfuzz import fuzz  # type: ignore
except Exception:  # pragma: no cover
    fuzz = None


def open_db(db_path: Path) -> sqlite3.Connection:
    if not db_path.exists():
        raise FileNotFoundError(f"SQLite DB not found: {db_path}")
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    d = dict(row)
    for key in ["frontmatter_json", "tags_json", "aliases_json"]:
        if key in d and isinstance(d[key], str):
            try:
                d[key[:-5] if key.endswith("_json") else key] = json.loads(d[key])
            except Exception:
                pass
    return d


def fuzzy_score(query: str, row: sqlite3.Row) -> int:
    q = query.lower()
    haystacks = [row["title"] or "", row["name"] or "", row["path"] or "", row["type"] or "", row["body_text"] or ""]
    if fuzz:
        return max(fuzz.partial_ratio(q, str(h).lower()) for h in haystacks)
    return int(max(difflib.SequenceMatcher(None, q, str(h).lower()).ratio() for h in haystacks) * 100)


def create_app(db_path: Path, debug: bool = False) -> FastAPI:
    conn = open_db(db_path)
    app = FastAPI(
        title="Windows应用安全基线画像库 API",
        description="检索 Obsidian/Markdown 画像库转出的 SQLite 数据，支持 exact/fuzzy/fts 检索。",
        version="1.0.0",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health() -> dict[str, Any]:
        LOG.debug("health check")
        try:
            count = conn.execute("SELECT COUNT(*) AS c FROM documents").fetchone()["c"]
            return {"status": "ok", "db": str(db_path), "documents": count}
        except Exception as exc:
            LOG.exception("health check failed")
            raise HTTPException(status_code=500, detail=str(exc))

    @app.get("/stats")
    def stats() -> dict[str, Any]:
        LOG.debug("stats requested")
        rows = conn.execute("SELECT type, COUNT(*) AS count FROM documents GROUP BY type ORDER BY count DESC, type").fetchall()
        link_stats = conn.execute("SELECT target_resolved, COUNT(*) AS count FROM links GROUP BY target_resolved").fetchall()
        return {
            "by_type": [dict(r) for r in rows],
            "links": [{"resolved": bool(r["target_resolved"]), "count": r["count"]} for r in link_stats],
        }

    @app.get("/documents/{doc_id}")
    def document(doc_id: str) -> dict[str, Any]:
        LOG.debug("document lookup doc_id=%s", doc_id)
        row = conn.execute("SELECT * FROM documents WHERE id = ?", (doc_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="document not found")
        sections = conn.execute("SELECT level,heading,content,sort_order FROM sections WHERE doc_id=? ORDER BY sort_order", (doc_id,)).fetchall()
        links = conn.execute(
            "SELECT target_text,target_doc_id,target_resolved,raw_link,context_heading,line_no,line_text FROM links WHERE source_doc_id=? ORDER BY line_no",
            (doc_id,),
        ).fetchall()
        data = row_to_dict(row)
        data["sections"] = [dict(r) for r in sections]
        data["links"] = [dict(r) for r in links]
        return data

    @app.get("/search")
    def search(
        q: str = Query(..., description="检索关键词"),
        mode: str = Query("fuzzy", pattern="^(exact|fuzzy|fts|like)$"),
        type: str | None = Query(None, description="按文档类型过滤，如 app/service/process/process_relation"),
        limit: int = Query(20, ge=1, le=200),
        offset: int = Query(0, ge=0),
    ) -> dict[str, Any]:
        LOG.debug("search request q=%r mode=%s type=%s limit=%d offset=%d", q, mode, type, limit, offset)
        params: list[Any] = []
        type_clause = ""
        if type:
            type_clause = " AND d.type = ?"
            params.append(type)

        try:
            if mode == "exact":
                sql = (
                    "SELECT d.*, 100 AS score FROM documents d "
                    "LEFT JOIN entities e ON e.doc_id=d.id "
                    "WHERE (d.title = ? OR d.name = ? OR d.path = ? OR e.service_name = ? OR e.process_name = ? OR e.vendor = ? OR d.type = ?)"
                    + type_clause +
                    " ORDER BY d.type, d.title LIMIT ? OFFSET ?"
                )
                query_params = [q, q, q, q, q, q, q, *params, limit, offset]
                LOG.debug("exact sql=%s params=%s", sql, query_params)
                rows = conn.execute(sql, query_params).fetchall()
                results = [row_to_dict(r) for r in rows]
            elif mode == "fts":
                try:
                    sql = (
                        "SELECT d.*, bm25(documents_fts) AS score "
                        "FROM documents_fts JOIN documents d ON d.id = documents_fts.doc_id "
                        "WHERE documents_fts MATCH ?" + type_clause +
                        " ORDER BY score LIMIT ? OFFSET ?"
                    )
                    query_params = [q, *params, limit, offset]
                    LOG.debug("fts sql=%s params=%s", sql, query_params)
                    rows = conn.execute(sql, query_params).fetchall()
                    results = [row_to_dict(r) for r in rows]
                except sqlite3.OperationalError as exc:
                    LOG.warning("FTS unavailable or query invalid (%s), fallback to LIKE", exc)
                    return search(q=q, mode="like", type=type, limit=limit, offset=offset)
            elif mode == "like":
                like = f"%{q}%"
                sql = (
                    "SELECT d.*, 50 AS score FROM documents d WHERE "
                    "(d.title LIKE ? OR d.name LIKE ? OR d.path LIKE ? OR d.body_text LIKE ? OR d.frontmatter_json LIKE ?)"
                    + type_clause +
                    " ORDER BY d.type, d.title LIMIT ? OFFSET ?"
                )
                query_params = [like, like, like, like, like, *params, limit, offset]
                LOG.debug("like sql=%s params=%s", sql, query_params)
                rows = conn.execute(sql, query_params).fetchall()
                results = [row_to_dict(r) for r in rows]
            else:  # fuzzy
                sql = "SELECT d.* FROM documents d WHERE 1=1" + type_clause
                LOG.debug("fuzzy candidate sql=%s params=%s", sql, params)
                rows = conn.execute(sql, params).fetchall()
                ranked = []
                for r in rows:
                    score = fuzzy_score(q, r)
                    if score >= 30:
                        item = row_to_dict(r)
                        item["score"] = score
                        ranked.append(item)
                ranked.sort(key=lambda x: x["score"], reverse=True)
                results = ranked[offset:offset + limit]
            LOG.debug("search result count=%d", len(results))
            return {"query": q, "mode": mode, "type": type, "count": len(results), "results": results}
        except Exception as exc:
            LOG.exception("search failed")
            raise HTTPException(status_code=500, detail=str(exc))

    @app.on_event("shutdown")
    def shutdown() -> None:
        LOG.debug("closing db connection")
        conn.close()

    return app


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Serve Windows App Security Baseline SQLite DB search API.")
    p.add_argument("--db", default="out/windows_app_baseline.db", help="SQLite database path generated by kb_to_sqlite.py")
    p.add_argument("--host", default="127.0.0.1", help="Listen host")
    p.add_argument("--port", type=int, default=8000, help="Listen port")
    p.add_argument("--reload", action="store_true", help="Enable uvicorn reload")
    p.add_argument("--debug", action="store_true", help="Enable debug logs")
    p.add_argument("--log-file", default=None, help="Write logs to file as well as stderr")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    configure_logging(args.debug, args.log_file)
    LOG.info("start API service db=%s host=%s port=%s", args.db, args.host, args.port)
    app = create_app(Path(args.db), debug=args.debug)
    uvicorn.run(app, host=args.host, port=args.port, log_level="debug" if args.debug else "info", reload=args.reload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
