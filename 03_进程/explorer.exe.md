---
type: process
process_name: explorer.exe
app: "[[Windows Shell]]"
vendor: Microsoft Corporation
role:
  - 用户Shell
risk_level: medium
confidence: medium
status: active
tags:
  - process/system
  - windows/shell
---

# explorer.exe

## 1. 进程说明

`explorer.exe` 是 Windows 用户 Shell，常作为用户手动启动应用的父进程。

## 2. 常见子进程

- [[chrome.exe]]
- [[winword.exe]]
- [[AnyDesk.exe]]

## 3. 常见父子关系

- [[explorer.exe -> chrome.exe]]

## 4. 安全关注点

```text
explorer.exe 拉起脚本解释器需要结合用户交互判断
explorer.exe 从异常路径运行
explorer.exe 被注入后拉起异常进程
```
