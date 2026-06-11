---
type: startup_method
os: linux
name: systemd Service
risk_level: high
confidence: high
tags:
  - startup/systemd
  - linux/startup
  - persistence
---

# systemd Service

## 1. 启动方式说明

systemd 是现代 Linux 最主要的服务管理与持久化机制，对应 Windows 的 [[Windows Service]]。系统守护进程、应用服务、容器运行时大多通过 systemd unit 常驻。

## 2. 关键位置

- [[systemd unit 持久化]]
- 单元目录：`/etc/systemd/system/`、`/usr/lib/systemd/system/`、`~/.config/systemd/user/`

## 3. 常见父进程

- [[systemd]]（PID 1）

## 4. 关键字段

```ini
[Unit] Description / After / Requires
[Service] ExecStart / ExecStartPre / User / Restart / Type
[Install] WantedBy
```

## 5. 异常关注点

```text
ExecStart 指向用户目录 / 临时目录 / 解释器
unit 写入用户可写目录
新增 enabled 的可疑 unit
Restart=always 维持恶意常驻
启动后立即外联或落地文件
```

## 6. 关联安全基线

- [[服务持久化机制对比]]
