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

- 来源页面：[[Windows常见应用服务基线清单]]
- 验收证据：[[Windows Service Control Manager 画像证据记录]]
- 完整画像验收：[[Windows常见应用完整画像验收清单]]
- 可信度：medium
- 待补强：官方文档、企业终端真实 ImagePath、签名、命令行、网络目的地址和授权状态。

## 常见父子进程关系

- [[services.exe -> svchost.exe]]

## 常见文件与数据

- [[Windows Service Control Manager 文件与数据画像]]
- 重点核验安装目录、配置、日志、缓存和用户态数据落点。

## 常见注册表信息

- [[Windows Service Control Manager 注册表画像]]
- [[HKLM_SYSTEM_CurrentControlSet_Services]]
- [[Uninstall Registry]]

## 常见网络行为

- [[Windows Service Control Manager 网络行为]]
- 精确域名、IP 和租户标识必须来自官方文档或企业网络观测。

## 常见启动方式

- [[Windows Service]]

## 关联安全基线

- [[Windows系统组件异常启动链路]]
