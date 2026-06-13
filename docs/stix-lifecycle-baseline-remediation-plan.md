---
title: STIX 进程全生命周期基线整改计划
status: active
created: 2026-06-12
tags:
  - stix
  - lifecycle-baseline
  - remediation-plan
---

# STIX 进程全生命周期基线整改计划

## 1. 目标

本整改以服务基于 STIX 建模的威胁分析为目标，把当前 Markdown 安全基线知识库优化为可支撑“进程创建时 + 运行时”联合判断的条件规则库。

判断结论必须围绕同一个运行时进程实例，而不是只看单点事件：

```text
创建时：父进程、启动用户、镜像路径、命令行、启动方式是否可解释
运行时：子进程、网络、文件、注册表/配置、模块、持久化变化是否可解释
证据面：判断所需证据是否齐全
```

只有创建时和运行时都能被应用画像解释，且关键证据齐全，才允许输出生命周期符合基线。

## 2. 当前差距

- 现有画像已经有人可读的“进程创建基线 / 启动参数基线 / 运行时行为基线 / 证据需求”章节，但机器只能粗略抽取正文文本。
- `process_relation` 页面能表达父子关系、`normality` 和 `risk_level`，可直接生成第一版创建时规则。
- 服务启动账户、ImagePath、进程用户上下文、运行时跟随证据等条件还没有统一结构化字段。
- `kb_to_neo4j.py` 当前生成知识图谱节点和 `LINKS_TO` 边，不生成可直接用于威胁分析的条件规则节点。
- KB 图谱中的 `:KbDocument:Process` 与 STIX 行为图中的 `:Process` 标签存在潜在混淆，条件查询必须显式区分知识节点和事实节点。

## 3. 整改原则

- Markdown / Obsidian 继续是唯一主数据源；Cypher、JSONL、SQLite、Neo4j 均为派生产物。
- 不把 hash、证书指纹、信誉、首次出现时间、具体企业账号等动态情报沉淀为 Markdown 白名单。
- 用户校验以“用户上下文类型”为主，例如 `interactive_user`、`local_system`、`service_account`，不写死企业真实账号。
- 安全结论采用保守收敛：任一阶段证据不足时输出 `evidence_insufficient`，知识缺口输出 `baseline_gap`，不伪造安全结论。
- 结构化条件优先放在固定正文章节的 YAML 代码块中，frontmatter 只保留身份和粗粒度分类字段。

## 4. 数据模型调整

### 4.1 进程画像

新增固定章节“结构化生命周期基线”，表达：

- 创建时必需证据：父进程、镜像路径、命令行、用户、启动方式。
- 创建时期望条件：父进程名、用户上下文、路径类别、常见命令行参数。
- 创建时异常条件：用户可写目录、临时目录、下载目录、网络共享、高风险参数。
- 运行时必需证据：子进程、网络连接、文件行为、注册表/配置、持久化变化。
- 运行时期望条件：常见子进程、常见网络用途、常见文件/注册表路径。
- 运行时异常条件：脚本解释器、异常外联、文件落地、持久化写入、敏感文件访问。

### 4.2 服务画像

服务页补充可抽取的启动上下文：

- `start_account_type`
- `image_path_patterns`
- `expected_processes`
- `suspicious_image_locations`
- `required_creation_evidence`

这用于判断服务创建的进程是否符合服务画像，而不是只根据服务名做粗匹配。

### 4.3 父子进程关系画像

关系页成为创建时判断的核心规则来源：

- `parent_process_name`
- `child_process_name`
- `expected_relation`
- `normality`
- `risk_level`
- `command_line_contains_any`
- `required_followup_evidence`
- `risk_escalates_when`

当前已有关系页可以先自动派生创建时规则；后续逐步补充结构化块提升精度。

### 4.4 安全基线画像

安全基线页补充规则条件集合：

- `phase: creation | runtime | lifecycle`
- `creation` 条件：父进程、子进程、用户上下文、路径、命令行。
- `runtime` 条件：网络、文件、注册表、子进程、持久化。
- `false_positive` 条件：授权软件分发、企业宏、固定自动化模板、变更单等。
- `required_evidence`：判断该基线必须具备的证据。

## 5. 转换工具

新增 `tools/kb_lifecycle_rules_to_cypher.py`：

- 输入：`kb/` Markdown vault。
- 输出：
  - `out/lifecycle_rules.jsonl`：规则库 JSONL。
  - `out/lifecycle_rules.cypher`：导入 Neo4j 的条件规则 Cypher。
  - `out/lifecycle_analysis_queries.cypher`：面向 STIX 行为事实图的参数化分析查询模板。
- 支持两类规则来源：
  - 结构化 YAML 规则块：来自整改后的进程、服务、关系、安全基线页面。
  - 派生父子关系规则：从当前 `process_relation` frontmatter、标题和固定章节自动生成第一版创建时规则。

规则节点建议使用命名空间标签，避免与 STIX 行为事实图冲突：

```cypher
(:KbLifecycleRule)
(:KbDocument)-[:DEFINES_LIFECYCLE_RULE]->(:KbLifecycleRule)
```

运行时分析查询仍以 STIX 行为事实图中的 `Process` 为锚点，并通过规则节点进行条件匹配。

## 6. 判断结果

生命周期判断服务应输出：

```text
safe                  创建时和运行时均匹配，证据完整
risky                 命中高风险基线，但存在可核验误报条件
deviation             明确偏离已有基线
baseline_gap          KB 缺少对应实体、关系或运行时规则
evidence_insufficient 缺少创建时或运行时关键证据
```

推荐收敛顺序：

```text
evidence_insufficient > baseline_gap > deviation > risky > safe
```

## 7. 分阶段落地

### P0：规则契约和工具

- 固化结构化生命周期基线 YAML 格式。
- 增加模板章节和抽取规范。
- 提供 KB 到 JSONL / Cypher 条件规则库转换工具。
- 验证当前 `process_relation` 页面可派生创建时规则。

### P1：高价值规则补齐

- 优先补齐 Office、浏览器、远控、VPN、更新器、安全代理、数据库服务等高价值对象。
- 补齐用户上下文类型、路径类别、命令行高风险项和运行时跟随证据。
- 对 `Office拉起脚本解释器`、`浏览器拉起脚本解释器`、`进程创建与运行时异常` 等通用基线补结构化规则。

### P2：运行时行为扩展

- 将网络、文件、注册表、Linux 配置/持久化画像纳入生命周期规则。
- 支持运行时窗口内的“随后发生”判断，例如进程创建后外联、文件落地、持久化写入。
- 将缺口输出反向转为 KB 待补候选。

### P3：威胁分析系统接入

- 将规则 Cypher 导入威胁分析 Neo4j。
- 在分析服务中以 STIX `Process` 实例为锚点执行创建时和运行时联合查询。
- 将判断结果、命中规则、缺失证据和误报条件写入分析结果或证据 trace。

## 8. 验收标准

- `tools/kb_lifecycle_rules_to_cypher.py` 能从当前 KB 生成非空规则库。
- 至少 `process_relation` 页面可生成创建时规则，且保留来源文档、风险等级、置信度和证据需求。
- 至少若干通用安全基线页面提供结构化生命周期规则，证明整改后的知识能直接转为可查询条件。
- 工具能输出可复用 Cypher 查询模板，用于按 STIX `Process` 锚点匹配创建时规则、运行时证据和证据完整性。
- `tools/smoke_lifecycle_e2e.py` 能使用生成的规则库完成端到端 smoke：完整 Office 拉起 PowerShell 生命周期收敛为 `risky`，缺少运行时证据的负例收敛为 `evidence_insufficient`。
- 模板和抽取规范说明同一套结构化规则格式。
- 生成的 Cypher 不直接修改主知识库，只创建派生规则节点。
- 原有 SQLite / Neo4j 抽取命令仍可重复运行。
