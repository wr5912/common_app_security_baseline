---
type: startup_method
name: Scheduled Task
risk_level: high
confidence: medium
tags:
  - startup/scheduled-task
  - persistence
---

# Scheduled Task

## 1. 启动方式说明

计划任务常用于软件更新、周期任务、企业运维，也常被攻击者用于持久化和延迟执行。

## 2. 常见触发器

```text
开机
登录
定时
空闲
事件触发
```

## 3. 异常关注点

```text
任务名伪装系统任务
执行程序位于用户目录或临时目录
以 SYSTEM 或最高权限运行
任务触发频率异常
执行 PowerShell/cmd/wscript/mshta
```
