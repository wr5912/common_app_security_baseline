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

## 4. 最小 JSON 结构

```json
{
  "path": "01_应用/Google Chrome.md",
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
```
