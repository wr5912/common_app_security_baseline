---
type: service
os: windows
service_name: Sense
display_name: Microsoft Defender for Endpoint Service
app: "[[Microsoft Defender]]"
vendor: Microsoft Corporation
service_type: Win32OwnProcess
start_type: auto
start_account: LocalSystem
image_name: SenseIR.exe
risk_level: high
confidence: low
status: needs_review
tags:
  - service/edr
  - service/security
  - vendor/microsoft
---

# Sense

## 1. 服务说明

`Sense` 通常与 Microsoft Defender for Endpoint 相关，用于 EDR 传感器和响应能力。

## 2. 所属应用

- [[Microsoft Defender]]

## 3. 异常关注点

```text
Sense 服务异常停止
EDR 组件无法启动
服务配置被篡改
攻击链中存在关闭 EDR 的迹象
```

## 4. 待验证项

不同 Windows 版本、MDE 部署方式下进程和路径可能不同，需要企业环境观测补充。
