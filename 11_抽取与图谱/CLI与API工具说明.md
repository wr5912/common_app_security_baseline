---
type: extract_spec
tags:
  - tools/sqlite
  - tools/neo4j
  - tools/api
  - llm-wiki
---

# CLI与API工具说明

## 1. 目标

本工具集用于把“终端应用安全基线画像库”的 Markdown Wiki 中间产物转成三类可消费形态：

```text
Markdown Wiki -> SQLite 结构化数据
Markdown Wiki -> Neo4j 图数据
SQLite -> API 检索服务
```

## 2. 工具一：SQLite 转换

脚本：

```text
tools/kb_to_sqlite.py
```

功能：

```text
解析 YAML frontmatter
解析 Markdown 标题章节
解析 Obsidian [[双链]]
构建 documents/entities/sections/links/tags/frontmatter_kv 表
构建 SQLite FTS5 全文索引
打印详细 debug 日志
```

命令：

```bash
python tools/kb_to_sqlite.py --vault . --out out/windows_app_baseline.db --rebuild --debug
```

## 3. 工具二：Neo4j 图转换

脚本：

```text
tools/kb_to_neo4j.py
```

功能：

```text
把每个 Markdown 文档转为 KbDocument 节点
按照 type 追加 App/Service/Process/ProcessRelation 等标签
把 Obsidian [[双链]] 转为 LINKS_TO 边
未解析链接可保留为 UnresolvedTarget 节点
默认生成 Cypher 文件
可选直连 Neo4j 执行导入
```

命令：

```bash
python tools/kb_to_neo4j.py --vault . --out out/windows_app_baseline.cypher --debug
```

## 4. 工具三：API 检索服务

脚本：

```text
tools/api_service.py
```

功能：

```text
提供 /health 健康检查
提供 /stats 统计接口
提供 /search 检索接口
提供 /documents/{doc_id} 文档详情接口
支持 exact/fuzzy/fts/like 四种模式
打印请求、SQL、参数、结果数量等 debug 日志
```

命令：

```bash
python tools/api_service.py --db out/windows_app_baseline.db --host 0.0.0.0 --port 8000 --debug
```

## 5. 与 LLM Wiki 理念的关系

这些工具不是要替代 Markdown Wiki，而是把 Wiki 变成可被程序、AI、图数据库和检索服务消费的派生产物。

```text
人类维护 Markdown
AI 读取 Markdown + AGENTS.md 进行可控编辑
SQLite 支撑统计和 API 检索
Neo4j 支撑关系推理和路径分析
```

## 6. 推荐流水线

```bash
python tools/kb_to_sqlite.py --vault . --out out/windows_app_baseline.db --rebuild --debug
python tools/kb_to_neo4j.py --vault . --out out/windows_app_baseline.cypher --debug
python tools/api_service.py --db out/windows_app_baseline.db --host 0.0.0.0 --port 8000 --debug
```
