---
type: config_persistence
os: linux
mechanism: cron
path_pattern: /etc/cron.d/*
purpose:
  - 定时任务
  - 定时持久化
risk_level: high
confidence: high
tags:
  - linux/persistence
  - persistence
---

# Crontab 持久化

> Linux 定时任务持久化位置，对应 Windows 的计划任务（见 [[Scheduled Task]]）。

## 1. 位置说明

cron 通过系统级和用户级 crontab 描述定时任务。正常用于运维定时作业，也常被用作定时回连与持久化。

## 2. 关键路径

```text
/etc/crontab
/etc/cron.d/*
/etc/cron.{daily,hourly,weekly,monthly}/
/var/spool/cron/crontabs/<user>   # 用户级 crontab -e
```

## 3. 正常写入场景

```text
日志轮转、备份、证书续期、监控采集
运维脚本定时执行
```

## 4. 异常关注点

```text
命令含 curl|bash、wget|sh、base64 -d、反弹 shell
@reboot 维持开机持久化
普通用户 crontab 中的可疑外联
指向用户目录 / 临时目录的脚本
高频（每分钟）执行
```

## 5. 关联

- 启动方式：[[Cron Job]]
- 安全基线：[[服务持久化机制对比]]
