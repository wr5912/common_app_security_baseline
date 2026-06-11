---
type: startup_method
os: windows
name: Windows Service
risk_level: high
confidence: high
tags:
  - startup/service
  - persistence
---

# Windows Service

## 1. 启动方式说明

Windows Service 是 Windows 上最重要的常驻和持久化机制之一。系统服务、应用服务、安全软件、远控软件、数据库、驱动都可能通过服务启动。

## 2. 关键注册表

- [[HKLM_SYSTEM_CurrentControlSet_Services]]

## 3. 常见父进程

- [[services.exe]]

## 4. 关键字段

```text
ServiceName
DisplayName
ImagePath
ObjectName
Start
Type
DependOnService
FailureActions
DelayedAutoStart
```

## 5. 异常关注点

```text
新建服务
ImagePath 指向用户目录或临时目录
服务程序无签名
服务名伪装系统服务
启动类型被改为 Auto
服务启动后立即外联或落地文件
```

## 6. 关联安全基线

- [[异常服务创建]]
- [[服务ImagePath篡改]]
