---
type: app
app_id: app_microsoft_defender
app_name_cn: Microsoft Defender
app_name_en: Microsoft Defender
vendor: Microsoft Corporation
category: 安全软件
subcategory: 杀毒/EDR
is_system_builtin: true
confidence: medium
status: active
tags:
  - app/security
  - vendor/microsoft
  - windows/builtin
---

# Microsoft Defender

## 1. 基本说明

Microsoft Defender 是 Windows 内置安全能力，包括防病毒、网络检查、安全中心以及 Defender for Endpoint 相关服务。

## 2. 相关服务

- [[WinDefend]]
- [[Sense]]

## 3. 相关进程

- [[MsMpEng.exe]]

## 4. 常见父子进程关系

- [[services.exe -> MsMpEng.exe]]

## 5. 正常行为画像

- 实时扫描文件。
- 更新病毒库。
- 监控进程、文件、注册表、网络行为。
- 与安全中心或云端保护能力通信。

## 6. 异常关注点

```text
WinDefend 服务异常停止
MsMpEng.exe 路径或签名异常
安全服务被关闭或配置被篡改
攻击链中出现关闭 Defender 的命令
```

## 7. 关联安全基线

- [[Defender服务异常停止]]
