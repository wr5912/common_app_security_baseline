---
type: process_relation
os: windows
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

## 4. 创建链路基线
<!-- baseline:process-creation-runtime -->
- 结构化关系：本页 `父进程 -> 子进程` 是可抽取的父子关系事实，判断时优先使用本页 frontmatter、标题和双链，不只依赖正文自然语言。
- 正常性判断：结合父进程来源、子进程路径、完整命令行、启动账户、服务/启动方式、所属应用和资产授权确认。
- 上下文边界：同一父子关系在服务启动、用户交互、更新器、插件、脚本执行或攻击链上下文中的风险等级可能不同。

## 5. 可能正常场景
```text
用户通过浏览器下载脚本后手动执行
企业网页管理工具触发本地协议
开发者测试场景
```

## 6. 高风险场景
```text
浏览器漏洞利用
恶意扩展
钓鱼页面诱导执行
PowerShell 下载器
```

## 7. 高风险参数与命令行关注
<!-- baseline:process-creation-runtime -->
- 命令行与子进程角色不匹配，例如服务进程携带隐藏执行、下载执行、内联脚本、异常代理、异常配置目录或凭据相关参数。
- 子进程路径位于用户可写目录、临时目录、下载目录、网络共享或与所属应用不一致的位置。
- 父进程与业务上下文不匹配，例如 Office、浏览器、PDF 阅读器或远控进程拉起脚本解释器、系统管理工具或未知二进制。

## 8. 证据需求
```text
Chrome 标签页/URL 上下文
下载文件路径
PowerShell 完整命令行
是否存在用户点击
是否外联
是否写入持久化位置
```

<!-- baseline:process-creation-runtime -->
- 进程创建事件：父子进程 GUID/PID、完整命令行、启动用户、当前目录、镜像路径、会话 ID 和完整时间线。
- 关联上下文：服务注册表或 systemd unit、启动方式、文件落地、网络连接、持久化写入、用户交互和资产授权记录。
- 外部核验：签名、哈希、信誉和流行度由情报/EDR/资产系统提供，本页只记录需要核验这些字段。
## 9. 关联安全基线
- [[浏览器拉起脚本解释器]]

## 10. 关联画像
- [[进程创建与运行时异常]]
