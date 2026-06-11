---
type: process
os: linux
process_name: systemd
app:
vendor: systemd project
role:
  - init
  - service-manager
risk_level: low
confidence: high
status: active
tags:
  - process/init
  - linux/process
---

# systemd

## 1. 进程说明

systemd 是大多数现代 Linux 发行版的 init 进程（PID 1）与服务管理器，对应 Windows 的 [[services.exe]] 角色。它启动并监管由 [[systemd Service]] 定义的守护进程。

## 2. 常见路径

```text
/usr/lib/systemd/systemd
/sbin/init -> systemd
```

## 3. 常见子进程

由各 unit 的 `ExecStart` 决定，例如 [[nginx.service]] 拉起的 [[nginx (进程)]] master。

## 4. 异常关注点

```text
非 PID 1 的进程伪装成 systemd
异常 unit 拉起 shell / 解释器或外联
用户级 systemd --user 拉起可疑常驻
```

## 5. 关联

- 启动方式：[[systemd Service]]
- 持久化：[[systemd unit 持久化]]
