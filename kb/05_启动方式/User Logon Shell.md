---
type: startup_method
os: windows
name: User Logon Shell
risk_level: medium
confidence: medium
status: active
tags:
  - startup/user-logon
---

# User Logon Shell

<!-- generated: windows-complete-profile-backfill -->

## 1. 启动方式说明

用户登录后，Windows Shell 通常由系统登录链路启动并承担桌面、任务栏、文件资源管理器和用户交互应用启动入口。

## 2. 关键注册表

- [[Windows Shell 注册表画像]]
- [[Run Key]]

## 3. 常见父进程

```text
winlogon.exe / userinit.exe / explorer.exe，具体链路随 Windows 版本和登录方式变化。
```

## 4. 异常关注点

```text
Shell 配置被改为非预期二进制
explorer.exe 从非系统目录启动
登录后立即拉起脚本解释器、远控、代理或未知二进制
```

## 5. 关联安全基线

- [[Windows系统组件异常启动链路]]
