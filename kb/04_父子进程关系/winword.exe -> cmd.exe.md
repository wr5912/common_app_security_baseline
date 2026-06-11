---
type: process_relation
os: windows
parent_process: "[[winword.exe]]"
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
  - office
  - cmd
---

# winword.exe -> cmd.exe

## 1. 关系说明
Word 拉起 Windows 命令解释器通常需要高关注，常见于宏、恶意文档、下载器、企业自动化插件或用户手动触发脚本。

## 2. 父进程
- [[winword.exe]]

## 3. 子进程
- [[cmd.exe]]

## 4. 创建链路基线
<!-- baseline:process-creation-runtime -->
- 结构化关系：本页 `父进程 -> 子进程` 是可抽取的父子关系事实，判断时优先使用本页 frontmatter、标题和双链，不只依赖正文自然语言。
- 正常性判断：结合父进程来源、子进程路径、完整命令行、启动账户、服务/启动方式、所属应用和资产授权确认。
- 上下文边界：企业签名宏或办公插件可能合法触发，但必须能由模板、插件、用户动作和变更记录解释。

## 5. 可能正常场景
```text
企业签名宏调用固定批处理
内部办公插件执行受控命令
用户明确触发的自动化模板
```

## 6. 高风险场景
```text
宏启用后立即执行命令
命令链下载远程脚本或可执行文件
写入服务、计划任务、Run Key 或启动目录
紧邻异常外联、数据打包或横向移动
```

## 7. 高风险参数与命令行关注
<!-- baseline:process-creation-runtime -->
- `/c` 后接下载执行、编码混淆、脚本解释器、系统管理工具或持久化命令。
- 子进程路径位于用户可写目录、临时目录、下载目录、网络共享或与所属应用不一致的位置。
- 父进程与业务上下文不匹配，例如 Office 拉起脚本解释器、系统管理工具或未知二进制。

## 8. 证据需求
<!-- baseline:process-creation-runtime -->
- 进程创建事件：父子进程 GUID/PID、完整命令行、启动用户、当前目录、镜像路径、会话 ID 和完整时间线。
- 关联上下文：文档来源、宏启用状态、模板/插件、文件落地、网络连接、持久化写入、用户交互和资产授权记录。
- 外部核验：签名、哈希、信誉和流行度由情报/EDR/资产系统提供，本页只记录需要核验这些字段。

## 9. 关联画像
- [[winword.exe]]
- [[cmd.exe]]
- [[Office拉起脚本解释器]]
- [[进程创建与运行时异常]]
