---
type: process
process_name: powershell.exe
app: "[[Windows PowerShell]]"
vendor: Microsoft Corporation
role:
  - 脚本解释器
  - 自动化工具
risk_level: high
confidence: medium
status: active
tags:
  - process/script
  - process/powershell
  - risk/high
---

# powershell.exe

## 1. 进程说明

`powershell.exe` 是 Windows PowerShell 解释器，广泛用于系统管理和自动化，也常被攻击链滥用。

## 2. 常见父进程

- [[explorer.exe]]
- `cmd.exe`
- `powershell.exe`
- 管理工具

高关注父进程：

- [[winword.exe]]
- [[chrome.exe]]

## 3. 高风险参数

```text
-EncodedCommand
-ExecutionPolicy Bypass
-NoProfile
-WindowStyle Hidden
-IEX
DownloadString
FromBase64String
```

## 4. 异常关注点

```text
Office / 浏览器 / PDF 阅读器拉起 PowerShell
PowerShell 隐藏窗口执行
Base64 编码命令
下载并执行远程脚本
创建服务、计划任务、Run Key
```

## 5. 关联安全基线

- [[Office拉起脚本解释器]]
- [[浏览器拉起脚本解释器]]
