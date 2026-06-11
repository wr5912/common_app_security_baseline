---
type: registry_pattern
os: windows
hive: HKLM/HKCU
key_pattern: Software\Microsoft\Windows\CurrentVersion\Uninstall\*
purpose:
  - software_inventory
risk_level: medium
confidence: medium
tags:
  - registry/uninstall
  - software-inventory
---

# Uninstall Registry

## 1. 注册表用途

卸载注册表用于记录软件安装信息，是识别应用和版本的重要来源。

## 2. 常见字段

```text
DisplayName
DisplayVersion
Publisher
InstallLocation
UninstallString
QuietUninstallString
InstallDate
```

## 3. 安全用途

- 识别软件资产。
- 辅助判断应用是否正式安装。
- 与服务、进程路径进行交叉验证。

## 4. 异常关注点

```text
存在服务但无卸载信息
卸载信息伪装知名软件
Publisher 与签名厂商不一致
InstallLocation 指向异常目录
```
