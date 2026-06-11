---
type: process_relation
parent_process: "[[services.exe]]"
child_process: "[[MsMpEng.exe]]"
relation: service_start
normality: normal
risk_level: low
confidence: medium
status: active
tags:
  - relation/service-start
  - service/security
  - vendor/microsoft
---

# services.exe -> MsMpEng.exe

## 1. 关系说明

`services.exe` 启动 `MsMpEng.exe` 通常对应 Microsoft Defender Antivirus 服务启动。

## 2. 正常条件

```text
服务为 WinDefend
路径为 Windows Defender 常见目录
签名为 Microsoft
服务启动类型符合策略
```

## 3. 异常条件

```text
MsMpEng.exe 路径异常
签名异常
服务配置异常
被攻击链尝试停止或禁用
```

## 4. 关联画像

- [[Microsoft Defender]]
- [[WinDefend]]
- [[MsMpEng.exe]]
- [[Defender服务异常停止]]
