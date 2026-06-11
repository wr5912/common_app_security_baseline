---
type: extract_spec
title: Obsidian链接到知识图谱映射
status: draft
tags:
  - extract/graph
  - neo4j
---

# Obsidian链接到知识图谱映射

## 1. 基本思路

Obsidian 双链表达实体之间的显式关系。抽取时可以结合页面类型、标题位置和 frontmatter 判断边类型。

## 2. 推荐边类型

```text
(:App)-[:HAS_SERVICE]->(:Service)
(:App)-[:HAS_PROCESS]->(:Process)
(:Service)-[:STARTS_PROCESS]->(:Process)
(:ProcessRelation)-[:HAS_PARENT]->(:Process)
(:ProcessRelation)-[:HAS_CHILD]->(:Process)
(:ProcessRelation)-[:RELATED_TO_BASELINE]->(:SecurityBaseline)
(:Process)-[:ACCESSES_REGISTRY]->(:RegistryPattern)
(:Process)-[:ACCESSES_FILE]->(:FileArtifact)
(:Process)-[:CONNECTS_TO]->(:NetworkBehavior)
(:Evidence)-[:SUPPORTS]->(:SecurityBaseline)
```

## 3. 关系页特殊处理

父子关系页的标题通常为：

```text
parent.exe -> child.exe
```

frontmatter 中必须包含：

```yaml
parent_process: "[[parent.exe]]"
child_process: "[[child.exe]]"
relation: spawn | service_start | user_launch
```

## 4. Neo4j 导入建议

第一阶段不要过度复杂，可以先导入：

```text
App
Service
Process
ProcessRelation
SecurityBaseline
```

跑通后再扩展注册表、文件、网络、证据。
