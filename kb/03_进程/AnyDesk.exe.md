---
type: process
os: windows
process_name: AnyDesk.exe
app: "[[AnyDesk]]"
vendor: AnyDesk Software GmbH
role:
  - 远程控制
risk_level: medium
confidence: medium
status: active
tags:
  - process/remote-control
  - app/remote-control
---

# AnyDesk.exe

## 1. 进程说明

`AnyDesk.exe` 是 AnyDesk 远程控制主进程，可作为用户进程或服务进程运行。

## 2. 所属应用

- [[AnyDesk]]

## 3. 常见父进程

- [[explorer.exe]]
- [[services.exe]]

## 4. 常见父子关系

- [[services.exe -> AnyDesk.exe]]

## 5. 正常行为

- 远程桌面连接。
- 屏幕、键鼠、剪贴板访问。
- 写入配置和日志。
- 网络连接远控基础设施。

## 6. 异常关注点

```text
从临时目录运行
静默安装后服务化
与异常账户登录、数据打包、横向移动同时出现
非授权终端上运行
```
