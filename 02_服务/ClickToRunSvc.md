---
type: service
service_name: ClickToRunSvc
display_name: Microsoft Office Click-to-Run Service
app: "[[Microsoft Office]]"
vendor: Microsoft Corporation
service_type: Win32OwnProcess
start_type: auto
start_account: LocalSystem
image_name: OfficeClickToRun.exe
risk_level: low
confidence: medium
status: active
tags:
  - service/office
  - service/update
  - vendor/microsoft
---

# ClickToRunSvc

## 1. 服务说明

`ClickToRunSvc` 是 Microsoft Office Click-to-Run 相关服务，常用于 Office 安装、更新、虚拟化和修复。

## 2. 所属应用

- [[Microsoft Office]]

## 3. 常见进程

- `OfficeClickToRun.exe`，待建页面

## 4. 正常行为

- Office 更新。
- Office 安装和修复。
- 管理 Office Click-to-Run 组件。

## 5. 异常关注点

```text
服务路径异常
签名异常
与 Office 安装路径不匹配
短时间内伴随 Office 子进程异常执行
```
