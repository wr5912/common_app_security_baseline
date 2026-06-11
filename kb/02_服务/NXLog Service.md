---
type: service
os: windows
service_name: "nxlog"
display_name: "nxlog"
app: "[[NXLog]]"
vendor: "NXLog"
service_type: windows_service
start_type: auto_or_manual
start_account: LocalSystem_or_service_account
image_name: "nxlog.exe"
risk_level: medium
confidence: medium
status: active
source_row_ids:
  - third-party-edr-026
tags:
  - service/windows-source-full-coverage
---

# NXLog Service

<!-- generated: windows-source-full-coverage -->

## 1. 服务说明

本页用于承载 `/tmp/windows系统上常见应用.md` 中 `nxlog` 服务或服务模式的规范化画像。

## 2. 所属应用

- [[NXLog]]

## 3. 常见启动方式

- [[Windows Service]]

## 4. 常见父进程与进程

- [[services.exe]]
- [[nxlog.exe]]
- [[services.exe -> nxlog.exe]]

## 5. 常见注册表位置

- [[Windows 服务注册表画像]]
- [[HKLM_SYSTEM_CurrentControlSet_Services]]

## 6. 常见文件与数据

- [[Windows 服务文件与数据画像]]
- [[NXLog 文件与数据画像]]

## 7. 常见网络行为

- [[Windows 服务网络行为]]
- [[NXLog 网络行为]]

## 8. 关联安全基线

- [[Windows服务ImagePath异常]]
- [[第三方服务异常常驻]]
- [[Windows常见应用全量覆盖清单]]
