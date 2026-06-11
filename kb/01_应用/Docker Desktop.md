---
type: app
os: windows
app_id: app_docker_desktop
app_name_cn: Docker Desktop
app_name_en: Docker Desktop
vendor: Docker Inc.
category: 开发工具
subcategory: 容器
is_system_builtin: false
confidence: medium
status: active
tags:
  - app/developer-tool
  - app/container
  - vendor/docker
---

# Docker Desktop

## 1. 基本说明

Docker Desktop 是 Windows 上常见容器开发环境，通常依赖 WSL2、Hyper-V、虚拟网络、后台服务等组件。

## 2. 相关服务

- [[com.docker.service]]

## 3. 相关进程

- [[Docker Desktop.exe]]

## 4. 常见行为画像

- 启动后台服务。
- 管理容器和镜像。
- 访问 WSL / Hyper-V 相关组件。
- 创建虚拟网络。
- 访问本地 Docker API / 命名管道。

## 5. 异常关注点

```text
生产终端异常安装 Docker Desktop
容器内启动代理、扫描、挖矿类进程
Docker API 暴露到不可信网络
服务路径或签名异常
```
