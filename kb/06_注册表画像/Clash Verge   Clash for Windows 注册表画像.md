---
type: registry_pattern
os: windows
confidence: medium
status: active
tags:
  - generated/windows-source-full-coverage
source_row_ids:
  - third-party-vpn-012
aliases:
  - "Clash Verge / Clash for Windows 注册表画像"

---
# Clash Verge / Clash for Windows 注册表画像

<!-- generated: windows-source-full-coverage -->

## 1. 注册表用途

[[Clash Verge / Clash for Windows]] 的服务配置、应用配置和卸载信息注册表位置模式。

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
third-party-vpn-012
```
