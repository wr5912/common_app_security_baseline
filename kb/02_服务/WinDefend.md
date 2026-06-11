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
source_row_ids:
  - third-party-edr-001
  - win-builtin-089
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

## 全量来源覆盖

<!-- generated: windows-source-full-coverage -->

- 来源行：`win-builtin-089`，第 101 行
- 所属应用：[[Windows Service Host]]
- 进程：[[svchost.exe]]
- 父子关系：[[services.exe -> svchost.exe]]
- 注册表：[[Windows 服务注册表画像]]
- 文件：[[Windows 服务文件与数据画像]]
- 网络：[[Windows 服务网络行为]]
- 证据：[[Windows常见应用全量覆盖清单]]
