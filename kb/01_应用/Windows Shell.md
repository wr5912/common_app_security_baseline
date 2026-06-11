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

- 来源类型：系统组件基线
- 可信度：medium
- 待验证：结合终端镜像和版本补充路径、签名和父子进程样例。
