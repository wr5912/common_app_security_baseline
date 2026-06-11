---
type: process_relation
os: windows
parent_process: "[[winword.exe]]"
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
  - office
  - powershell
---

# winword.exe -> powershell.exe

## 1. 关系说明
`winword.exe` 拉起 `powershell.exe` 在普通办公场景中并不常见。它可能来自企业宏、办公插件或自动化流程，也可能是恶意文档攻击链。

## 2. 父进程
- [[winword.exe]]

## 3. 子进程
- [[powershell.exe]]

## 4. 创建链路基线
<!-- baseline:process-creation-runtime -->
- 结构化关系：本页 `父进程 -> 子进程` 是可抽取的父子关系事实，判断时优先使用本页 frontmatter、标题和双链，不只依赖正文自然语言。
- 正常性判断：结合父进程来源、子进程路径、完整命令行、启动账户、服务/启动方式、所属应用和资产授权确认。
- 上下文边界：同一父子关系在服务启动、用户交互、更新器、插件、脚本执行或攻击链上下文中的风险等级可能不同。

## 5. 可能正常场景
```text
企业签名宏
内部办公插件
文档自动化模板
IT 管理脚本
```

## 6. 高风险场景
```text
钓鱼文档
宏下载器
混淆 PowerShell
隐藏窗口执行
下载并执行远程脚本
落地可执行文件
```

## 7. 高风险参数与命令行关注
```text
-EncodedCommand
-ExecutionPolicy Bypass
-NoProfile
-WindowStyle Hidden
-IEX
DownloadString
FromBase64String
```

<!-- baseline:process-creation-runtime -->
- 命令行与子进程角色不匹配，例如服务进程携带隐藏执行、下载执行、内联脚本、异常代理、异常配置目录或凭据相关参数。
- 子进程路径位于用户可写目录、临时目录、下载目录、网络共享或与所属应用不一致的位置。
- 父进程与业务上下文不匹配，例如 Office、浏览器、PDF 阅读器或远控进程拉起脚本解释器、系统管理工具或未知二进制。
## 8. 证据需求
```text
Word 文档来源
是否启用宏
PowerShell 完整命令行
是否外联
是否落地文件
是否创建服务/计划任务/Run Key
用户是否主动打开文档
```

<!-- baseline:process-creation-runtime -->
- 进程创建事件：父子进程 GUID/PID、完整命令行、启动用户、当前目录、镜像路径、会话 ID 和完整时间线。
- 关联上下文：服务注册表或 systemd unit、启动方式、文件落地、网络连接、持久化写入、用户交互和资产授权记录。
- 外部核验：签名、哈希、信誉和流行度由情报/EDR/资产系统提供，本页只记录需要核验这些字段。
## 9. 检测建议
```text
父进程为 winword.exe
子进程为 powershell.exe/cmd.exe/wscript.exe/mshta.exe
且命令行包含高风险参数
或随后发生网络连接/文件落地/持久化写入
```

## 10. 误报条件
```text
签名宏
固定办公插件
已知自动化模板
命令行固定且无外联
```

## 11. 推荐处置
默认进入疑似或高危队列，关联文档来源、网络行为、文件落地、注册表持久化证据后再定性。

## 12. 关联画像
- [[Microsoft Office]]
- [[Office拉起脚本解释器]]
- [[进程创建与运行时异常]]
