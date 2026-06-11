---
type: registry_pattern
os: windows
confidence: medium
status: active
tags:
  - generated/windows-source-full-coverage
---

# Windows 服务注册表画像

<!-- generated: windows-source-full-coverage -->

## 1. 注册表用途

Windows 服务统一配置位置，覆盖内置服务、per-user service 和第三方服务。

## 2. 关键位置

```text
HKLM\SYSTEM\CurrentControlSet\Services\*
```

## 3. 关联安全基线

- [[Windows服务ImagePath异常]]
- [[服务ImagePath篡改]]
