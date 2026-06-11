---
type: startup_method
os: linux
name: Cron Job
risk_level: high
confidence: high
tags:
  - startup/cron
  - linux/startup
  - persistence
---

# Cron Job

## 1. 启动方式说明

cron 是 Linux 上常见的定时任务机制，对应 Windows 的 [[Scheduled Task]]。常被用于运维定时作业，也常被攻击者用作持久化与定时回连。

## 2. 关键位置

- [[Crontab 持久化]]
- `/etc/crontab`、`/etc/cron.d/`、`/etc/cron.{daily,hourly,weekly,monthly}/`、`crontab -l`（用户级）

## 3. 常见父进程

- `cron` / `crond` 守护进程

## 4. 关键字段

```text
分 时 日 月 周  用户  命令
*/5 * * * * root /path/to/command
```

## 5. 异常关注点

```text
命令为 curl|bash、base64 解码、反弹 shell
写入用户目录 / 临时目录的脚本
高频（每分钟）回连
@reboot 维持开机持久化
普通用户 crontab 中的可疑外联
```

## 6. 关联安全基线

- [[服务持久化机制对比]]
