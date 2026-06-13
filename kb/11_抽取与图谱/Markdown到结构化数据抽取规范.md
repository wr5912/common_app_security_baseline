---
type: extract_spec
title: Markdown到结构化数据抽取规范
status: draft
tags:
  - extract/json
  - extract/csv
---

# Markdown到结构化数据抽取规范

## 1. 抽取目标

将 Obsidian Markdown Wiki 转为结构化数据，用于：

```text
CSV / JSON / SQLite / Neo4j / 威胁分析系统知识库
```

## 2. 抽取对象

```text
YAML Frontmatter -> node properties
Obsidian Links -> graph edges
固定标题正文 -> long_text fields
代码块 -> examples / evidence
标签 -> classification fields
```

## 3. 节点类型映射

| Markdown type | 图谱节点 |
|---|---|
| app | App |
| service | Service |
| process | Process |
| process_relation | ProcessRelation |
| registry_pattern | RegistryPattern |
| file_artifact | FileArtifact |
| network_behavior | NetworkBehavior |
| security_baseline | SecurityBaseline |
| source_evidence | Evidence |
| process section: 进程创建基线 | ProcessCreationBaselineSection |
| process section: 启动参数基线 | ProcessArgumentBaselineSection |
| process section: 运行时行为基线 | ProcessRuntimeBaselineSection |
| process section: 证据需求 | EvidenceRequirementSection |
| section: 结构化生命周期基线 / 结构化生命周期规则 | KbLifecycleRule |

> 进程创建与运行时基线暂不新增独立 Markdown `type`。抽取器通过固定章节标题进入 `sections` 表 / 图谱 section 属性，避免把每个参数模式拆成过细的实体。需要规则化时由下游系统从 section 文本、代码块和链接中二次加工。
>
> 面向 STIX 行为事实图的条件判断规则使用固定 YAML 代码块表达，并由 `tools/kb_lifecycle_rules_to_cypher.py` 转换为 `KbLifecycleRule` 派生节点。Markdown 页面仍是主数据源，规则节点和 Cypher 文件都是派生产物。

## 4. 最小 JSON 结构

```json
{
  "path": "kb/01_应用/Google Chrome.md",
  "title": "Google Chrome",
  "type": "app",
  "frontmatter": {},
  "links": ["gupdate", "chrome.exe"],
  "headings": {},
  "tags": ["app/browser"]
}
```

## 5. 质量校验

```text
每个页面必须有 type
每个页面必须有一级标题
关键页面必须有 confidence
关系页必须有 parent_process 和 child_process
安全基线页必须有 normality 和 risk_level
进程页必须有 进程创建基线 / 启动参数基线 / 运行时行为基线 / 安全关注点 / 证据需求 / 关联安全基线
父子关系页必须有 创建链路基线 / 高风险参数与命令行关注 / 证据需求 / 关联画像
需要进行自动化生命周期判断的页面应补充 结构化生命周期基线 或 结构化生命周期规则 YAML 块
签名、hash、信誉、首次出现时间和流行度只作为证据需求，不作为 Markdown 白名单字段
```
