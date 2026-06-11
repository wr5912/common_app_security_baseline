---
type: process_relation
os: windows
parent_process: "[[explorer.exe]]"
child_process: "[[chrome.exe]]"
relation: user_launch
normality: normal
risk_level: low
confidence: medium
status: active
tags:
  - relation/user-launch
  - browser
---

# explorer.exe -> chrome.exe

## 1. 关系说明
`explorer.exe` 拉起 `chrome.exe` 通常表示用户通过桌面、开始菜单、快捷方式或文件关联启动浏览器。

## 2. 正常条件
```text
chrome.exe 路径位于 Google 官方安装目录
签名正常
命令行参数符合浏览器启动场景
存在用户交互上下文
```

## 3. 异常条件
```text
chrome.exe 位于临时目录、下载目录或公共目录
签名异常
命令行包含异常代理、扩展或调试参数
启动后立即拉起脚本解释器
```

## 4. 创建链路基线
<!-- baseline:process-creation-runtime -->
- 结构化关系：本页 `父进程 -> 子进程` 是可抽取的父子关系事实，判断时优先使用本页 frontmatter、标题和双链，不只依赖正文自然语言。
- 正常性判断：结合父进程来源、子进程路径、完整命令行、启动账户、服务/启动方式、所属应用和资产授权确认。
- 上下文边界：同一父子关系在服务启动、用户交互、更新器、插件、脚本执行或攻击链上下文中的风险等级可能不同。

## 5. 高风险参数与命令行关注
<!-- baseline:process-creation-runtime -->
- 命令行与子进程角色不匹配，例如服务进程携带隐藏执行、下载执行、内联脚本、异常代理、异常配置目录或凭据相关参数。
- 子进程路径位于用户可写目录、临时目录、下载目录、网络共享或与所属应用不一致的位置。
- 父进程与业务上下文不匹配，例如 Office、浏览器、PDF 阅读器或远控进程拉起脚本解释器、系统管理工具或未知二进制。

## 6. 证据需求
<!-- baseline:process-creation-runtime -->
- 进程创建事件：父子进程 GUID/PID、完整命令行、启动用户、当前目录、镜像路径、会话 ID 和完整时间线。
- 关联上下文：服务注册表或 systemd unit、启动方式、文件落地、网络连接、持久化写入、用户交互和资产授权记录。
- 外部核验：签名、哈希、信誉和流行度由情报/EDR/资产系统提供，本页只记录需要核验这些字段。

## 7. 关联画像
- [[Google Chrome]]
- [[chrome.exe]]
- [[进程创建与运行时异常]]
