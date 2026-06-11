---
type: process
process_name: Docker Desktop.exe
app: "[[Docker Desktop]]"
vendor: Docker Inc.
role:
  - 容器管理
risk_level: medium
confidence: medium
status: active
tags:
  - process/container
  - app/developer-tool
---

# Docker Desktop.exe

## 1. 进程说明

`Docker Desktop.exe` 是 Docker Desktop 的用户界面和控制进程之一。

## 2. 所属应用

- [[Docker Desktop]]

## 3. 相关服务

- [[com.docker.service]]

## 4. 常见行为

- 管理容器。
- 与后台服务通信。
- 访问本地 Docker API。
- 与 WSL2 / Hyper-V 组件交互。

## 5. 异常关注点

```text
生产终端异常出现容器运行环境
容器内运行扫描、代理、挖矿或攻击工具
Docker API 对外暴露
```
