---
type: service
os: windows
service_name: com.docker.service
display_name: Docker Desktop Service
app: "[[Docker Desktop]]"
vendor: Docker Inc.
service_type: Win32OwnProcess
start_type: auto
start_account: LocalSystem
image_name: com.docker.service.exe
risk_level: medium
confidence: medium
status: active
tags:
  - service/container
  - app/developer-tool
  - vendor/docker
source_row_ids:
  - third-party-service-026
---
# com.docker.service

## 1. 服务说明

`com.docker.service` 是 Docker Desktop 的后台服务，常用于容器生命周期、网络和权限相关管理。

## 2. 所属应用

- [[Docker Desktop]]

## 3. 常见进程

- [[Docker Desktop.exe]]

## 4. 正常行为

- 管理 Docker Desktop 后台能力。
- 配合 WSL2 / Hyper-V。
- 管理容器网络和镜像。

## 5. 异常关注点

```text
服务出现在非开发终端
服务路径异常
Docker API 暴露或被滥用
容器内运行异常工具
```

## 全量来源覆盖

<!-- generated: windows-source-full-coverage -->

- 来源行：`third-party-service-026`，第 379 行
- 所属应用：[[Docker Desktop]]
- 进程：[[com.docker.service.exe]]
- 父子关系：[[services.exe -> com.docker.service.exe]]
- 注册表：[[Windows 服务注册表画像]]
- 文件：[[Windows 服务文件与数据画像]]
- 网络：[[Windows 服务网络行为]]
- 证据：[[Windows常见应用全量覆盖清单]]
