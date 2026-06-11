---
type: source_evidence
os: windows
source_id: src_windows_app_complete_profile_acceptance
title: Windows常见应用完整画像验收清单
source_type: acceptance_manifest
confidence: medium
status: active
tags:
  - evidence/acceptance
  - windows/app-baseline
---

# Windows常见应用完整画像验收清单

## 1. 适用范围

本页约束 `2026-06-11` 批次从 `/tmp/windows系统上常见应用.md` 补充的 Windows 应用画像，范围以提交 `69edfe5` 新增的 `kb/01_应用/*.md` 为准。

## 2. 完整画像定义

单个应用只有同时满足下列链路，才可称为完成：

```text
应用 -> 服务/启动方式 -> 进程 -> 父子进程关系 -> 文件/注册表/网络行为 -> 安全基线 -> 证据
```

最小验收项：

```text
app
service
process
process_relation
startup_method
registry_pattern
file_artifact
network_behavior
security_baseline
source_evidence
```

进程与父子关系页面还必须满足：

```text
process: 进程创建基线 / 启动参数基线 / 运行时行为基线 / 安全关注点 / 证据需求 / 关联安全基线
process_relation: 创建链路基线 / 高风险参数与命令行关注 / 证据需求 / 关联画像
```

其中，应用页自身不得继续停留在 `status: needs_review` 或 `confidence: low`；如某应用确实没有某一类实体，必须有专门证据页说明“不适用”的判断依据。

## 3. 机器验收入口

使用仓库工具生成当前覆盖矩阵：

```bash
.venv/bin/python tools/audit_profile_completeness.py \
  --vault kb \
  --scope-git-range HEAD^..HEAD \
  --out-md out/profile_completeness.md \
  --out-json out/profile_completeness.json
```

阻断式验收：

```bash
.venv/bin/python tools/audit_profile_completeness.py \
  --vault kb \
  --scope-git-range HEAD^..HEAD \
  --fail

.venv/bin/python tools/audit_process_behavior_baseline.py \
  --vault kb \
  --fail
```

## 4. 当前缺口判断

`2026-06-11` 初次审计显示，该批次 `32` 个应用均未满足完整画像定义。主要缺口是：

```text
缺少 process_relation 页面
缺少 file_artifact 页面
缺少 network_behavior 页面
部分系统组件缺少 service / startup_method / registry_pattern / security_baseline / source_evidence 链路
多数应用页仍为 confidence: low / status: needs_review
```

## 5. 证据使用原则

- `/tmp/windows系统上常见应用.md` 只能证明“服务名 / 应用场景在本批次清单中出现”，不能单独证明完整画像。
- 官方文档、厂商安装包说明、企业终端观测、EDR/Sysmon 事件和人工复核结果应逐步进入 `kb/10_来源与证据/`。
- 不得无来源填充精确域名、哈希或特定版本路径。
- 不得把具体签名、hash、证书指纹、信誉、首次出现时间或样本流行度写成 Markdown 白名单；这些动态情报由专门系统提供。
- 对于版本、安装方式或企业定制导致的差异，保留“模式化画像 + 待观测字段”，但不能把该状态称为最终完成。

## 6. 关联对象

- [[Windows常见应用服务基线清单]]
- [[Windows第三方应用服务识别索引]]
- [[应用分类索引]]
- [[服务分类索引]]
- [[进程分类索引]]
- [[文件与数据索引]]
- [[网络行为索引]]
- [[注册表关键位置索引]]
- [[高风险父子进程关系索引]]
