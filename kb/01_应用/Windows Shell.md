---
type: app
os: windows
app_id: windows-shell
app_name_cn: Windows Shell
app_name_en: Windows Shell
vendor: Microsoft Corporation
category: 系统组件
subcategory: 用户界面
is_system_builtin: true
confidence: medium
status: active
tags:
  - app/system
  - windows/shell
---

# Windows Shell

## 1. 基本说明

Windows Shell 是 Windows 图形桌面、文件资源管理器和用户交互入口相关的系统组件。

## 2. 相关进程

- [[explorer.exe]]
- [[cmd.exe]]

## 3. 正常行为画像

- 用户登录后启动桌面和任务栏。
- 作为用户交互启动应用时的常见父进程。

## 4. 异常关注点

```text
explorer.exe 路径异常
explorer.exe 拉起脚本解释器或未知二进制
explorer.exe 被注入后产生异常网络连接或持久化写入
```

## 5. 证据与来源

- 来源页面：[[Windows常见应用服务基线清单]]
- 验收证据：[[Windows Shell 画像证据记录]]
- 完整画像验收：[[Windows常见应用完整画像验收清单]]
- 可信度：medium
- 待补强：官方文档、企业终端真实 ImagePath、签名、命令行、网络目的地址和授权状态。

## 常见父子进程关系

- [[explorer.exe -> explorer.exe]]

## 常见文件与数据

- [[Windows Shell 文件与数据画像]]
- 重点核验安装目录、配置、日志、缓存和用户态数据落点。

## 常见注册表信息

- [[Windows Shell 注册表画像]]
- [[HKLM_SYSTEM_CurrentControlSet_Services]]
- [[Uninstall Registry]]

## 常见网络行为

- [[Windows Shell 网络行为]]
- 精确域名、IP 和租户标识必须来自官方文档或企业网络观测。

## 常见启动方式

- [[User Logon Shell]]

## 关联安全基线

- [[Windows系统组件异常启动链路]]
