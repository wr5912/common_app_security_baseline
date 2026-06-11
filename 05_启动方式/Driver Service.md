---
type: startup_method
os: windows
name: Driver Service
risk_level: critical
confidence: medium
tags:
  - startup/driver
  - kernel
  - persistence
---

# Driver Service

## 1. 启动方式说明

驱动服务用于内核驱动加载，常见于安全软件、VPN、虚拟化、硬件驱动。异常驱动加载风险极高。

## 2. 关联注册表

- [[HKLM_SYSTEM_CurrentControlSet_Services]]

## 3. 异常关注点

```text
新建内核驱动服务
驱动无签名或签名异常
驱动位于异常目录
Start 类型为 Boot/System
与安全软件绕过、Rootkit、内核权限提升相关
```
