---
type: process
os: windows
process_name: services.exe
app: "[[Windows Service Control Manager]]"
vendor: Microsoft Corporation
role:
  - 服务控制管理器
risk_level: high
confidence: medium
status: active
tags:
  - process/system
  - windows/service-control-manager
---

# services.exe

## 1. 进程说明

`services.exe` 是 Windows Service Control Manager 相关核心进程，常作为 Windows 服务进程的父进程。

## 2. 常见子进程

- [[GoogleUpdate.exe]]
- [[AnyDesk.exe]]
- [[MsMpEng.exe]]
- `svchost.exe`

## 3. 常见父子关系

- [[services.exe -> GoogleUpdate.exe]]
- [[services.exe -> AnyDesk.exe]]
- [[services.exe -> MsMpEng.exe]]

## 4. 安全关注

`services.exe` 拉起服务进程本身正常，但需要结合服务注册表、ImagePath、签名和启动账户判断风险。

## 5. 关联注册表

- [[HKLM_SYSTEM_CurrentControlSet_Services]]
