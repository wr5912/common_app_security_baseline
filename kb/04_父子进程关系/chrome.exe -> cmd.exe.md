---
type: process_relation
os: windows
parent_process: "[[chrome.exe]]"
child_process: "[[cmd.exe]]"
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
  - cmd
---

# chrome.exe -> cmd.exe

## 1. 关系说明
浏览器拉起 `cmd.exe` 通常需要高关注。它可能来自用户下载脚本后执行、协议处理器、企业管理网页、恶意扩展或漏洞利用。

## 2. 父进程
- [[chrome.exe]]

## 3. 子进程
- [[cmd.exe]]

## 4. 创建链路基线
<!-- baseline:process-creation-runtime -->
- 结构化关系：本页 `父进程 -> 子进程` 是可抽取的父子关系事实，判断时优先使用本页 frontmatter、标题和双链，不只依赖正文自然语言。
- 正常性判断：结合父进程来源、子进程路径、完整命令行、启动账户、服务/启动方式、所属应用和资产授权确认。
- 上下文边界：企业网页管理工具或本地协议可能合法触发，但必须能由 URL、用户动作、下载文件和授权记录解释。

## 5. 可能正常场景
```text
用户通过浏览器下载脚本后手动执行
企业管理网页触发本地协议
开发者本地测试
```

## 6. 高风险场景
```text
浏览器漏洞利用或恶意扩展
钓鱼页面诱导执行命令
命令链下载执行远程内容
紧邻异常外联、落地文件或持久化写入
```

## 7. 高风险参数与命令行关注
<!-- baseline:process-creation-runtime -->
- `/c` 后接下载执行、编码混淆、脚本解释器、系统管理工具或持久化命令。
- 子进程路径位于用户可写目录、临时目录、下载目录、网络共享或与所属应用不一致的位置。
- 父进程与业务上下文不匹配，例如浏览器拉起脚本解释器、系统管理工具或未知二进制。

## 8. 证据需求
<!-- baseline:process-creation-runtime -->
- 进程创建事件：父子进程 GUID/PID、完整命令行、启动用户、当前目录、镜像路径、会话 ID 和完整时间线。
- 关联上下文：URL、标签页、下载文件、浏览器扩展、本地协议、网络连接、文件落地、用户交互和资产授权记录。
- 外部核验：签名、哈希、信誉和流行度由情报/EDR/资产系统提供，本页只记录需要核验这些字段。

## 9. 关联画像
- [[chrome.exe]]
- [[cmd.exe]]
- [[浏览器拉起脚本解释器]]
- [[进程创建与运行时异常]]
