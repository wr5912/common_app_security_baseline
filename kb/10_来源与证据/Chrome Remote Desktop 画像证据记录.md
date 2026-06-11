---
type: source_evidence
os: windows
source_id: src_chrome-remote-desktop_profile_evidence
title: "Chrome Remote Desktop 画像证据记录"
source_type: profile_acceptance_record
app: "[[Chrome Remote Desktop]]"
not_applicable_types:
  []
confidence: medium
status: active
tags:
  - evidence/windows-app-profile
source_row_ids:
  - third-party-rmm-010
---
# Chrome Remote Desktop 画像证据记录

<!-- generated: windows-complete-profile-backfill -->

## 1. 来源说明

本页用于记录 [[Chrome Remote Desktop]] 在完整画像补齐中的证据边界。当前画像来源包括：

- `/tmp/windows系统上常见应用.md` 中的场景应用和服务基线清单。
- 既有 KB 页面之间的应用、服务、进程和安全基线双链。
- Windows 服务、注册表、父子进程、文件落点和网络行为的模式化安全分析要求。

## 2. 本轮验收用途

- 证明该应用纳入 `2026-06-11` Windows 常见应用完整画像补齐范围。
- 记录哪些画像类型已经建页，哪些类型因系统组件属性不适用。
- 为后续官方文档、EDR/Sysmon、资产台账和企业终端观测补证据提供落点。

## 3. 不适用类型

```text
无
```

## 4. 待补强证据

```text
官方安装路径或服务说明
企业终端真实 ImagePath、启动账户、签名和版本
EDR/Sysmon 父子进程、文件、注册表和网络观测样例
资产授权、业务角色和变更记录
```

## 5. 关联验收

- [[Windows常见应用完整画像验收清单]]
- [[Windows常见应用服务基线清单]]
- [[Windows第三方应用服务识别索引]]
