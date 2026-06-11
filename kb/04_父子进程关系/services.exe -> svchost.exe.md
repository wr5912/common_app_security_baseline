---
type: process_relation
os: windows
parent_process: "[[services.exe]]"
child_process: "[[svchost.exe]]"
relation: service_start
normality: normal
risk_level: medium
confidence: medium
status: active
source_row_ids:
  - win-per-user-001
  - win-per-user-002
  - win-per-user-003
  - win-per-user-004
  - win-per-user-005
  - win-per-user-006
  - win-per-user-007
  - win-per-user-008
  - win-per-user-009
  - win-per-user-010
  - win-per-user-011
  - win-per-user-012
  - win-per-user-013
  - win-per-user-014
  - win-per-user-015
  - win-per-user-016
  - win-per-user-017
  - win-per-user-018
  - win-per-user-019
  - win-per-user-020
  - win-per-user-021
  - win-per-user-022
  - win-per-user-023
  - win-per-user-024
tags:
  - relation/windows-source-full-coverage
---

# services.exe -> svchost.exe

<!-- generated: windows-source-full-coverage -->

## 1. 关系说明

`services.exe` 启动 [[svchost.exe]] 是 [[Windows Per-user Services]] 或其服务组件的常见服务启动链路。具体是否正常必须结合服务注册表、ImagePath、签名、启动账户、命令行和资产授权判断。

## 2. 高风险场景

```text
子进程路径位于用户可写目录、临时目录、下载目录或网络共享
服务项新建或 ImagePath 变化后立即外联
服务进程与应用授权、签名厂商或资产角色不一致
```

## 3. 关联画像

- [[services.exe]]
- [[svchost.exe]]
- [[Windows Per-user Services]]
- [[第三方服务异常常驻]]
