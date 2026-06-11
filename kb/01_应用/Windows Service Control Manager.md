---
type: app
os: windows
app_id: windows-service-control-manager
app_name_cn: Windows 服务控制管理器
app_name_en: Windows Service Control Manager
vendor: Microsoft Corporation
category: 系统组件
subcategory: 服务管理
is_system_builtin: true
confidence: medium
status: active
tags:
  - app/system
  - windows/service-control-manager
---

# Windows Service Control Manager

## 1. 基本说明

Windows Service Control Manager 负责管理 Windows 服务的注册、启动、停止和状态控制，是服务画像链路中的核心系统组件。

## 2. 相关进程

- [[services.exe]]

## 3. 相关启动方式

- [[Windows Service]]

## 4. 异常关注点

```text
services.exe 拉起未知路径服务进程
服务 ImagePath 指向用户目录、临时目录或可写目录
服务创建时间与异常登录、横向移动或权限提升接近
```

## 5. 证据与来源

- 来源类型：系统组件基线
- 可信度：medium
- 待验证：结合服务注册表和系统事件日志补充事件 ID 映射。
