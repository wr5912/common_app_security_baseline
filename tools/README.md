# 终端应用安全基线画像库 CLI / API 工具集

本目录提供 3 类工具：

1. `kb_to_sqlite.py`：将 Obsidian/Markdown 画像库转为结构化 SQLite 数据。
2. `kb_to_neo4j.py`：将 Obsidian/Markdown 双链关系转为 Neo4j 图数据，默认生成 Cypher 文件，可选直连执行。
3. `api_service.py`：基于 SQLite 数据库提供 API 检索服务，支持全匹配、模糊匹配、FTS 全文检索、LIKE 检索。

所有工具均支持：

```bash
--debug
--log-file logs/tool.log
```

用于打印详细 debug 日志，方便排查解析、抽取、入库、检索问题。

---

## 1. 安装依赖

建议在画像库根目录执行（团队规范要求使用 `.venv` + `uv`，禁止直接 `pip`）：

```bash
uv venv .venv
uv pip install -r tools/requirements.txt
```

后续运行工具统一使用 `.venv/bin/python`（Windows 为 `.venv\Scripts\python.exe`），除非当前 shell 已激活 `.venv`。

如果只需要生成 SQLite，最低只需要：

```bash
uv pip install PyYAML
```

如果只生成 Neo4j Cypher 文件，不直连 Neo4j，也可以不安装 `neo4j` Python driver。

---

## 2. Markdown 画像库转 SQLite

```bash
.venv/bin/python tools/kb_to_sqlite.py \
  --vault . \
  --out out/windows_app_baseline.db \
  --rebuild \
  --debug \
  --log-file logs/kb_to_sqlite.debug.log
```

可选导出 JSONL：

```bash
.venv/bin/python tools/kb_to_sqlite.py \
  --vault . \
  --out out/windows_app_baseline.db \
  --rebuild \
  --export-jsonl out/documents.jsonl \
  --debug
```

### SQLite 主要表

| 表名 | 说明 |
|---|---|
| `documents` | 每个 Markdown 文档一条记录，保留 frontmatter、正文、纯文本、hash、路径 |
| `entities` | 从文档归一化出的实体视图，例如 app/service/process/security_baseline |
| `sections` | Markdown 标题章节抽取结果 |
| `links` | Obsidian `[[双链]]` 抽取结果，包含已解析和未解析目标 |
| `tags` | YAML tags 拆分表 |
| `frontmatter_kv` | frontmatter key-value 展开表 |
| `documents_fts` | SQLite FTS5 全文索引，若当前 SQLite 支持 FTS5 会自动创建 |
| `metadata` | 生成时间、schema 版本、文档数量等元数据 |

### 常见 debug 日志

```text
DEBUG [wabk] loaded doc path=01_应用/Google Chrome.md type=app title=Google Chrome links=12 sections=13
DEBUG [wabk.sqlite] insert document path=02_服务/gupdate.md type=service title=gupdate
DEBUG [wabk.sqlite] populate FTS index
INFO  [wabk.sqlite] SQLite build finished: out/windows_app_baseline.db
```

---

## 3. Markdown 画像库转 Neo4j 图数据

### 3.1 生成 Cypher 文件

```bash
.venv/bin/python tools/kb_to_neo4j.py \
  --vault . \
  --out out/windows_app_baseline.cypher \
  --debug \
  --log-file logs/kb_to_neo4j.debug.log
```

生成结果可以复制到 Neo4j Browser 执行，也可以用 `cypher-shell` 执行。

```bash
cypher-shell -a bolt://localhost:7687 -u neo4j -p password -f out/windows_app_baseline.cypher
```

### 3.2 直连 Neo4j 执行

```bash
.venv/bin/python tools/kb_to_neo4j.py \
  --vault . \
  --out out/windows_app_baseline.cypher \
  --execute \
  --uri bolt://localhost:7687 \
  --user neo4j \
  --password password \
  --database neo4j \
  --debug
```

### Neo4j 图模型

节点：

```cypher
(:KbDocument)
(:KbDocument:App)
(:KbDocument:Service)
(:KbDocument:Process)
(:KbDocument:ProcessRelation)
(:KbDocument:SecurityBaseline)
(:KbDocument:RegistryPattern)
(:KbDocument:NetworkBehavior)
(:KbDocument:UnresolvedTarget)
```

边：

```cypher
(:KbDocument)-[:LINKS_TO]->(:KbDocument)
```

边属性会保留：

```text
raw_link
context_heading
line_no
line_text
target_text
```

这样可以从 Obsidian 双链追踪到知识图谱关系来源。

---

## 4. API 检索服务

先构建 SQLite：

```bash
.venv/bin/python tools/kb_to_sqlite.py --vault . --out out/windows_app_baseline.db --rebuild
```

启动服务：

```bash
.venv/bin/python tools/api_service.py \
  --db out/windows_app_baseline.db \
  --host 0.0.0.0 \
  --port 8000 \
  --debug \
  --log-file logs/api_service.debug.log
```

### API 端点

| API | 说明 |
|---|---|
| `GET /health` | 健康检查 |
| `GET /stats` | 按文档类型统计、链接解析统计 |
| `GET /search?q=chrome&mode=fuzzy&limit=20` | 模糊匹配 |
| `GET /search?q=Google Chrome&mode=exact&type=app` | 全匹配 |
| `GET /search?q=chrome&mode=fts` | SQLite FTS 全文检索 |
| `GET /search?q=chrome&mode=like` | SQL LIKE 检索 |
| `GET /documents/{doc_id}` | 获取文档详情、章节、链接 |

### 检索模式说明

| mode | 说明 |
|---|---|
| `exact` | 全匹配；匹配 title/name/path/service_name/process_name/vendor/type |
| `fuzzy` | 模糊匹配；使用 rapidfuzz，未安装时降级到 difflib |
| `fts` | SQLite FTS5 全文检索；不可用时自动降级 LIKE |
| `like` | SQL LIKE 包含匹配 |

示例：

```bash
curl "http://127.0.0.1:8000/search?q=chrome&mode=fuzzy&limit=5"
curl "http://127.0.0.1:8000/search?q=Google%20Chrome&mode=exact&type=app"
curl "http://127.0.0.1:8000/stats"
```

---

## 5. 推荐工作流

```bash
# 1. 在 Obsidian 中维护 Markdown 画像
# 2. 转 SQLite
.venv/bin/python tools/kb_to_sqlite.py --vault . --out out/windows_app_baseline.db --rebuild --debug

# 3. 转 Neo4j Cypher
.venv/bin/python tools/kb_to_neo4j.py --vault . --out out/windows_app_baseline.cypher --debug

# 4. 启动 API 服务
.venv/bin/python tools/api_service.py --db out/windows_app_baseline.db --host 0.0.0.0 --port 8000 --debug
```

---

## 6. 设计原则

本工具集遵循“Markdown Wiki 是源头，结构化数据是派生产物”的原则：

```text
Markdown/Obsidian：给人和 AI 维护知识
SQLite：给检索、统计、API 服务使用
Neo4j：给关系推理、可视化、路径分析使用
```

不要手工修改 SQLite 或 Neo4j 作为主数据源。所有正式修改都应回写到 Markdown 画像库，再重新生成结构化数据。
