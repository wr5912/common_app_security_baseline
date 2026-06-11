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
- [[Windows系统组件异常启动链路]]
- [[浏览器拉起脚本解释器]]

## 4. 异常关注点

```text
由 Office、浏览器、PDF 阅读器等用户应用拉起
隐藏窗口、绕过执行策略或 Base64 编码执行
下载并执行远程脚本
创建服务、计划任务或 Run Key
```

## 5. 证据与来源

- 来源页面：[[Windows常见应用服务基线清单]]
- 验收证据：[[Windows PowerShell 画像证据记录]]
- 完整画像验收：[[Windows常见应用完整画像验收清单]]
- 可信度：medium
- 待补强：官方文档、企业终端真实 ImagePath、签名、命令行、网络目的地址和授权状态。

## 常见父子进程关系

- [[explorer.exe -> powershell.exe]]

## 常见文件与数据

- [[Windows PowerShell 文件与数据画像]]
- 重点核验安装目录、配置、日志、缓存和用户态数据落点。

## 常见注册表信息

- [[Windows PowerShell 注册表画像]]
- [[HKLM_SYSTEM_CurrentControlSet_Services]]
- [[Uninstall Registry]]

## 常见网络行为

- [[Windows PowerShell 网络行为]]
- 精确域名、IP 和租户标识必须来自官方文档或企业网络观测。

## 常见启动方式

- [[Scheduled Task]]
- [[Run Key]]
- [[Windows Service]]
