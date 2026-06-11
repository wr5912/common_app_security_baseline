---
type: extract_spec
title: Windows应用画像到威胁分析系统映射
status: draft
tags:
  - threat-analysis
  - baseline
  - graph
---

# Windows应用画像到威胁分析系统映射

## 1. 定位

本画像库是威胁分析系统的“静态常识层”，用于解释真实观测事件是否符合常见应用行为。

## 2. 和观测事实的关系

```text
画像库：GoogleUpdate.exe 通常由 services.exe 通过 gupdate 服务启动
观测事实：某主机上 services.exe 启动了 C:\Users\Public\GoogleUpdate.exe
判断：父子关系看似相同，但路径和签名偏离基线
```

## 3. 可用于核验的字段

```text
process_name
parent_process_name
command_line
image_path
signer
service_name
registry_key
dst_domain
dst_port
normality
risk_level
allowlist_condition
false_positive_condition
```

## 4. 可生成的测试用例

```text
正常更新器启动
更新器路径异常
Office 拉起 PowerShell
远控服务新建
Defender 服务停止
```

## 5. 和反馈闭环的关系

当误报/漏报发生时，反馈可以沉淀为：

```text
新的误报条件
新的异常条件
新的父子进程关系
新的服务参数模式
新的回归测试用例
```
