---
type: process
os: windows
process_name: MsMpEng.exe
app: "[[Microsoft Defender]]"
vendor: Microsoft Corporation
role:
  - 反恶意软件服务进程
risk_level: high
confidence: medium
status: active
tags:
  - process/security
  - vendor/microsoft
---

# MsMpEng.exe

## 1. 进程说明

`MsMpEng.exe` 是 Microsoft Defender Antivirus 相关核心进程之一。

## 2. 所属应用

- [[Microsoft Defender]]

## 3. 相关服务

- [[WinDefend]]

## 4. 常见父进程

- [[services.exe]]

## 5. 常见父子关系

- [[services.exe -> MsMpEng.exe]]

## 6. 正常行为

- 文件扫描。
- 实时防护。
- 安全情报更新。

## 7. 异常关注点

```text
路径异常
签名异常
服务异常停止
攻击链中出现排除路径、关闭防护、禁用服务等动作
```
