---
type: registry_pattern
os: windows
confidence: medium
status: active
tags:
  - generated/windows-source-full-coverage
source_row_ids:
  - third-party-edr-018
---
# Trend Micro 注册表画像

<!-- generated: windows-source-full-coverage -->

## 1. 注册表用途

[[Trend Micro]] 的服务配置、应用配置和卸载信息注册表位置模式。

## 2. 常见字段

```text
HKLM\SYSTEM\CurrentControlSet\Services\*
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*
HKLM/HKCU\SOFTWARE\<Vendor>\*
```

## 3. 关联启动方式

- [[Windows Service]]
- [[Run Key]]

## 4. 来源行

```text
third-party-edr-018
```
