---
type: registry_pattern
os: windows
hive: HKLM
key_pattern: HKLM\Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\*
purpose:
  - debugger_hijack
  - troubleshooting
risk_level: critical
confidence: medium
tags:
  - registry/ifeo
  - persistence
  - hijack
---

# IFEO

## 1. 注册表用途

Image File Execution Options 可用于调试器配置，也可能被滥用于进程劫持、持久化或阻断安全工具。

## 2. 高风险字段

```text
Debugger
GlobalFlag
SilentProcessExit
```

## 3. 异常关注点

```text
为安全软件、浏览器、系统工具设置 Debugger
Debugger 指向非可信路径
用于阻断安全软件启动
与持久化或防御规避同时出现
```
