---
type: process_relation
parent_process: "[[chrome.exe]]"
child_process: "[[powershell.exe]]"
relation: spawn
normality: rare
risk_level: high
attack_techniques:
  - T1059
  - T1204
confidence: medium
status: active
tags:
  - relation/process-spawn
  - risk/high
  - browser
  - powershell
---

# chrome.exe -> powershell.exe

## 1. 关系说明

浏览器进程拉起 PowerShell 通常需要高关注。可能来自用户下载脚本后执行、浏览器协议处理器、恶意扩展、漏洞利用或社会工程攻击。

## 2. 父进程

- [[chrome.exe]]

## 3. 子进程

- [[powershell.exe]]

## 4. 可能正常场景

```text
用户通过浏览器下载脚本后手动执行
企业网页管理工具触发本地协议
开发者测试场景
```

## 5. 高风险场景

```text
浏览器漏洞利用
恶意扩展
钓鱼页面诱导执行
PowerShell 下载器
```

## 6. 需要补充的证据

```text
Chrome 标签页/URL 上下文
下载文件路径
PowerShell 完整命令行
是否存在用户点击
是否外联
是否写入持久化位置
```

## 7. 关联安全基线

- [[浏览器拉起脚本解释器]]
