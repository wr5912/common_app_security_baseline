---
type: process_relation
os: windows
parent_process: "[[services.exe]]"
child_process: "[[SophosEndpointDefenseService.exe]]"
relation: service_start
normality: normal
risk_level: medium
confidence: medium
status: active
source_row_ids:
  - third-party-edr-014
  - third-party-edr-015
tags:
  - relation/windows-source-full-coverage
---

# services.exe -> SophosEndpointDefenseService.exe

<!-- generated: windows-source-full-coverage -->

## 1. 关系说明

`services.exe` 启动 [[SophosEndpointDefenseService.exe]] 是 [[Sophos]] 或其服务组件的常见服务启动链路。具体是否正常必须结合服务注册表、ImagePath、签名、启动账户、命令行和资产授权判断。

## 2. 高风险场景

```text
子进程路径位于用户可写目录、临时目录、下载目录或网络共享
服务项新建或 ImagePath 变化后立即外联
服务进程与应用授权、签名厂商或资产角色不一致
```

## 3. 关联画像

- [[services.exe]]
- [[SophosEndpointDefenseService.exe]]
- [[Sophos]]
- [[第三方服务异常常驻]]
