---
type: extract_spec
tags:
  - tools/sqlite
  - tools/neo4j
  - tools/lifecycle-rule
  - tools/api
  - llm-wiki
---

# CLI与API工具说明

## 生命周期条件规则库

面向 STIX 行为事实图的进程全生命周期判断，使用 `tools/kb_lifecycle_rules_to_cypher.py` 从 Markdown KB 生成派生规则库：

```bash
.venv/bin/python tools/kb_lifecycle_rules_to_cypher.py \
  --vault kb \
  --out-jsonl out/lifecycle_rules.jsonl \
  --out-cypher out/lifecycle_rules.cypher \
  --out-query-cypher out/lifecycle_analysis_queries.cypher \
  --debug \
  --log-file kb/logs/kb_lifecycle_rules.debug.log
```

该工具不会修改 KB 主数据，只生成 `out/lifecycle_rules.jsonl`、`out/lifecycle_rules.cypher` 与 `out/lifecycle_analysis_queries.cypher`。规则来源包括：

- “结构化生命周期基线 / 结构化生命周期规则” YAML 代码块。
- 当前 `process_relation` 页面可派生的创建时父子进程规则。

导入 Neo4j 后，规则节点使用 `(:KbLifecycleRule)`，并通过 `(:KbDocument)-[:DEFINES_LIFECYCLE_RULE]->(:KbLifecycleRule)` 追踪来源文档。运行时事实图中的 STIX `Process` 节点必须与知识库 `(:KbDocument:Process)` 节点区分查询。

`out/lifecycle_analysis_queries.cypher` 提供创建时规则匹配、运行时证据摘要和证据完整性骨架查询，供分析服务按同一个 STIX `Process` 实例收敛生命周期判断结果。

端到端 smoke：

```bash
.venv/bin/python tools/smoke_lifecycle_e2e.py \
  --rules-jsonl out/lifecycle_rules.jsonl \
  --out out/lifecycle_e2e_smoke.json \
  --strict
```

该 smoke 使用 STIX/Neo4j 语义一致的进程生命周期 fixture，验证创建时规则命中、运行时证据命中、证据不足负例和最终 `risky / evidence_insufficient` 收敛结果。`out/lifecycle_e2e_smoke.json` 是派生验证报告，不是主知识源。

Neo4j 查询级端到端 smoke：

```bash
.venv/bin/python tools/smoke_lifecycle_neo4j_e2e.py \
  --rules-cypher out/lifecycle_rules.cypher \
  --query-cypher out/lifecycle_analysis_queries.cypher \
  --out out/lifecycle_neo4j_e2e_smoke.json \
  --strict
```

该 smoke 默认启动临时 Neo4j 容器，将 `KbLifecycleRule` 导入图数据库，再写入 STIX/Neo4j 风格进程生命周期 fixture，验证创建时命中、运行时窗口判断、证据完整性和知识节点 / 事实节点隔离。

## 1. 目标

本工具集用于把“终端应用安全基线画像库”的 Markdown Wiki 中间产物转成五类可消费形态：

```text
Markdown Wiki -> SQLite 结构化数据
Markdown Wiki -> Neo4j 图数据
Markdown Wiki -> 生命周期条件规则库
生命周期条件规则库 -> 端到端 smoke 验证
生命周期条件规则库 -> Neo4j 查询级 smoke 验证
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
解析 Obsidian 双链语法
构建 documents/entities/sections/links/tags/frontmatter_kv 表
构建 SQLite FTS5 全文索引
打印详细 debug 日志
```

命令：

```bash
python tools/kb_to_sqlite.py --vault kb --out out/windows_app_baseline.db --rebuild --debug
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
把 Obsidian 双链语法转为 LINKS_TO 边
未解析链接可保留为 UnresolvedTarget 节点
默认生成 Cypher 文件
可选直连 Neo4j 执行导入
```

命令：

```bash
python tools/kb_to_neo4j.py --vault kb --out out/windows_app_baseline.cypher --debug
```

## 4. 工具三：生命周期规则库与端到端 smoke

脚本：

```text
tools/kb_lifecycle_rules_to_cypher.py
tools/smoke_lifecycle_e2e.py
tools/smoke_lifecycle_neo4j_e2e.py
```

功能：

```text
从结构化生命周期基线 / 规则 YAML 块和 process_relation 页面生成 KbLifecycleRule 规则库
输出 lifecycle_rules.jsonl、lifecycle_rules.cypher 和 lifecycle_analysis_queries.cypher
使用 STIX/Neo4j 语义一致的进程生命周期 fixture 执行端到端 smoke
使用临时 Neo4j 行为事实图执行查询级端到端 smoke
验证创建时规则、运行时证据、证据不足负例和最终判断收敛
```

命令：

```bash
python tools/kb_lifecycle_rules_to_cypher.py --vault kb --out-jsonl out/lifecycle_rules.jsonl --out-cypher out/lifecycle_rules.cypher --out-query-cypher out/lifecycle_analysis_queries.cypher --strict
python tools/smoke_lifecycle_e2e.py --rules-jsonl out/lifecycle_rules.jsonl --out out/lifecycle_e2e_smoke.json --strict
python tools/smoke_lifecycle_neo4j_e2e.py --rules-cypher out/lifecycle_rules.cypher --query-cypher out/lifecycle_analysis_queries.cypher --out out/lifecycle_neo4j_e2e_smoke.json --strict
```

## 5. 工具四：API 检索服务

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

## 6. 工具五：完整画像覆盖审计

脚本：

```text
tools/audit_profile_completeness.py
```

功能：

```text
按应用范围检查 app -> service/startup -> process -> process_relation -> file/registry/network -> security_baseline -> source_evidence 链路
支持用 git range 锁定某一批新增应用
输出 Markdown / JSON 覆盖矩阵
支持 --fail 作为阻断式验收
支持由 source_evidence 声明不适用类型，避免为系统组件伪造服务页
```

命令：

```bash
python tools/audit_profile_completeness.py --vault kb --scope-git-range HEAD^..HEAD --out-md out/profile_completeness.md --out-json out/profile_completeness.json
python tools/audit_profile_completeness.py --vault kb --scope-git-range HEAD^..HEAD --fail
```

## 7. 工具六：Windows 全量来源覆盖审计

脚本：

```text
tools/windows_source_inventory.py
tools/audit_source_coverage.py
```

功能：

```text
解析 /tmp/windows系统上常见应用.md 中的 Windows 内置服务、per-user services 和第三方应用/服务表格
为每条来源行生成稳定 source_row_id
检查每条来源行是否映射到 KB 中的服务、应用/组件、启动方式、进程、父子关系、文件、注册表、网络、基线和证据链路
输出 Markdown / JSON 覆盖矩阵
支持 --fail 作为阻断式验收
```

命令：

```bash
python tools/windows_source_inventory.py /tmp/windows系统上常见应用.md
python tools/audit_source_coverage.py --vault kb --source /tmp/windows系统上常见应用.md --out-md out/source_coverage.md --out-json out/source_coverage.json
python tools/audit_source_coverage.py --vault kb --source /tmp/windows系统上常见应用.md --fail
```

注意：

```text
该工具直接读取 /tmp/windows系统上常见应用.md；本项目不要求把该原始文件复制到 kb/raw_sources/。
KB 内只保存规范化后的覆盖清单、证据摘要和画像页面。
```

## 8. 工具七：Obsidian 严格双链审计

脚本：

```text
tools/audit_obsidian_links.py
```

功能：

```text
按 Obsidian 实际跳转语义检查双链目标
只有命中文件 stem、相对路径或 YAML aliases 才算可解析
仅靠 H1 标题宽松命中的链接会标记为 title_only
检查重复 target key，避免 alias 或文件名造成歧义
输出 Markdown / JSON 报告
支持 --fail 作为阻断式验收
```

命令：

```bash
python tools/audit_obsidian_links.py --vault kb --out-md out/obsidian_links.md --out-json out/obsidian_links.json
python tools/audit_obsidian_links.py --vault kb --fail
```

注意：

```text
SQLite / Neo4j 转换器会按页面标题做宽松解析，适合图谱构建。
Obsidian 严格双链审计按文件名、相对路径和 aliases 判断，适合发现 Markdown 中真实不可跳转的链接。
发版前应优先运行严格双链审计，不能只依赖 Neo4j unresolved=0。
```

## 9. 工具八：进程创建与运行时基线审计

脚本：

```text
tools/audit_process_behavior_baseline.py
```

功能：

```text
检查 process 页面是否包含进程创建基线、启动参数基线、运行时行为基线、安全关注点、证据需求和关联安全基线
检查 process_relation 页面是否包含创建链路基线、高风险参数与命令行关注、证据需求和关联画像
检查父子关系标题 / 文件名是否使用 parent -> child 结构
输出 Markdown / JSON 报告
支持 --fail 作为阻断式验收
```

命令：

```bash
python tools/audit_process_behavior_baseline.py --vault kb --out-md out/process_behavior_baseline.md --out-json out/process_behavior_baseline.json
python tools/audit_process_behavior_baseline.py --vault kb --fail
```

配套回填脚本：

```text
tools/backfill_process_behavior_baselines.py
```

该脚本只用于把已有进程和父子关系页面补齐 canonical 章节；回填后仍以 Markdown Wiki 为正式知识源。

## 10. 与 LLM Wiki 理念的关系

这些工具不是要替代 Markdown Wiki，而是把 Wiki 变成可被程序、AI、图数据库和检索服务消费的派生产物。

```text
人类维护 Markdown
AI 读取 Markdown + AGENTS.md 进行可控编辑
SQLite 支撑统计和 API 检索
Neo4j 支撑关系推理和路径分析
```

## 11. 推荐流水线

```bash
python tools/audit_obsidian_links.py --vault kb --fail
python tools/audit_profile_completeness.py --vault kb --scope-git-range HEAD^..HEAD --fail
python tools/audit_source_coverage.py --vault kb --source /tmp/windows系统上常见应用.md --fail
python tools/audit_process_behavior_baseline.py --vault kb --fail
python tools/kb_to_sqlite.py --vault kb --out out/windows_app_baseline.db --rebuild --debug
python tools/kb_to_neo4j.py --vault kb --out out/windows_app_baseline.cypher --debug
python tools/kb_lifecycle_rules_to_cypher.py --vault kb --out-jsonl out/lifecycle_rules.jsonl --out-cypher out/lifecycle_rules.cypher --out-query-cypher out/lifecycle_analysis_queries.cypher --strict
python tools/smoke_lifecycle_e2e.py --rules-jsonl out/lifecycle_rules.jsonl --out out/lifecycle_e2e_smoke.json --strict
python tools/smoke_lifecycle_neo4j_e2e.py --rules-cypher out/lifecycle_rules.cypher --query-cypher out/lifecycle_analysis_queries.cypher --out out/lifecycle_neo4j_e2e_smoke.json --strict
python tools/api_service.py --db out/windows_app_baseline.db --host 0.0.0.0 --port 8000 --debug
```
