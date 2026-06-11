---
type: process
os: linux
process_name: nginx
app: "[[nginx]]"
vendor: nginx / F5
role:
  - web-server
  - reverse-proxy
risk_level: medium
confidence: medium
status: active
tags:
  - process/web-server
  - linux/process
---

# nginx (进程)

## 1. 进程说明

nginx 以一个 master 进程 + 多个 worker 进程运行。master 由 [[nginx.service]] 启动，worker 由 master fork。

## 2. 常见路径

```text
/usr/sbin/nginx
```

## 3. 常见父进程

- [[systemd]]（master）
- nginx master（worker 的父进程）

## 4. 常见子进程

```text
正常情况下 nginx 不应拉起 shell / 解释器
```

## 5. 异常行为

```text
nginx -> sh / bash / python / perl（疑似 webshell 或命令注入）
nginx 进程外联非业务目标
worker 以 root 长期运行且对外暴露
```

## 6. 关联安全基线

- [[服务持久化机制对比]]
