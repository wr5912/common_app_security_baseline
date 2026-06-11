---
type: registry_pattern
os: windows
confidence: medium
status: active
tags:
  - generated/windows-source-full-coverage
source_row_ids:
  - win-per-user-001
  - win-per-user-002
  - win-per-user-003
  - win-per-user-004
  - win-per-user-005
  - win-per-user-006
  - win-per-user-007
  - win-per-user-008
  - win-per-user-009
  - win-per-user-010
  - win-per-user-011
  - win-per-user-012
  - win-per-user-013
  - win-per-user-014
  - win-per-user-015
  - win-per-user-016
  - win-per-user-017
  - win-per-user-018
  - win-per-user-019
  - win-per-user-020
  - win-per-user-021
  - win-per-user-022
  - win-per-user-023
  - win-per-user-024
---
# Windows Per-user Services 注册表画像

<!-- generated: windows-source-full-coverage -->

## 1. 注册表用途

[[Windows Per-user Services]] 的服务配置、应用配置和卸载信息注册表位置模式。

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
win-per-user-001, win-per-user-002, win-per-user-003, win-per-user-004, win-per-user-005, win-per-user-006, win-per-user-007, win-per-user-008, win-per-user-009, win-per-user-010, win-per-user-011, win-per-user-012, win-per-user-013, win-per-user-014, win-per-user-015, win-per-user-016, win-per-user-017, win-per-user-018, win-per-user-019, win-per-user-020, win-per-user-021, win-per-user-022, win-per-user-023, win-per-user-024
```
