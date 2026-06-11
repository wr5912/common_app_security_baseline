---
type: service
os: windows
service_name: WinDefend
display_name: Microsoft Defender Antivirus Service
app: "[[Microsoft Defender]]"
vendor: Microsoft Corporation
service_type: Win32OwnProcess
start_type: auto
start_account: LocalSystem
image_name: MsMpEng.exe
risk_level: high
confidence: medium
status: active
tags:
  - service/security
  - vendor/microsoft
  - windows/builtin
---

# WinDefend

## 1. 服务说明

`WinDefend` 是 Microsoft Defender Antivirus Service，负责防病毒和实时防护能力。

## 2. 所属应用

- [[Microsoft Defender]]

## 3. 常见进程

- [[MsMpEng.exe]]

## 4. 常见父进程

- [[services.exe]]

## 5. 常见父子关系

- [[services.exe -> MsMpEng.exe]]

## 6. 正常行为

- 启动反恶意软件服务进程。
- 实时扫描文件和进程。
- 更新安全情报。

## 7. 异常关注点

```text
WinDefend 被停止或禁用
服务启动类型被修改
MsMpEng.exe 路径异常
服务配置被篡改
与关闭安全产品命令同时出现
```

## 8. 关联安全基线

- [[Defender服务异常停止]]
