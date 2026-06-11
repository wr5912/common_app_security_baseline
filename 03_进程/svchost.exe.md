---
type: process
os: windows
process_name: svchost.exe
app: "[[Windows Service Host]]"
vendor: Microsoft Corporation
role:
  - 服务宿主进程
risk_level: high
confidence: medium
status: active
tags:
  - process/system
  - windows/svchost
---

# svchost.exe

## 1. 进程说明

`svchost.exe` 是 Windows 服务宿主进程，用于承载共享进程模式的服务。

## 2. 常见启动参数

```text
-k <service_group>
-p
-s <service_name>
```

## 3. 安全关注点

```text
svchost.exe 路径异常
缺少正常 -k/-s 参数
由非系统父进程启动
命令行与服务注册表不匹配
非 Microsoft 签名
```

## 4. 关联注册表

- [[HKLM_SYSTEM_CurrentControlSet_Services]]
