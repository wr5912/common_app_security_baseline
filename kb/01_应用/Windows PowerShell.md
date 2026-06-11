---
type: app
os: windows
app_id: windows-powershell
app_name_cn: Windows PowerShell
app_name_en: Windows PowerShell
vendor: Microsoft Corporation
category: 系统组件
subcategory: 脚本与自动化
is_system_builtin: true
confidence: medium
status: active
tags:
  - app/system
  - windows/powershell
---

# Windows PowerShell

## 1. 基本说明

Windows PowerShell 是 Windows 内置脚本解释器和自动化管理环境，常用于系统管理、运维脚本和配置变更，也常被攻击链滥用。

## 2. 相关进程

- [[powershell.exe]]

## 3. 关联安全基线

- [[Office拉起脚本解释器]]
- [[浏览器拉起脚本解释器]]

## 4. 异常关注点

```text
由 Office、浏览器、PDF 阅读器等用户应用拉起
隐藏窗口、绕过执行策略或 Base64 编码执行
下载并执行远程脚本
创建服务、计划任务或 Run Key
```

## 5. 证据与来源

- 来源类型：系统组件基线
- 可信度：medium
- 待验证：结合企业 PowerShell 日志策略和命令行样例补强。
