---
type: process_relation
os: windows
parent_process: "[[services.exe]]"
child_process: "[[MsMpEng.exe]]"
relation: service_start
normality: normal
risk_level: low
confidence: medium
status: active
tags:
  - relation/service-start
  - service/security
  - vendor/microsoft
---

# services.exe -> MsMpEng.exe

## 1. 关系说明
`services.exe` 启动 `MsMpEng.exe` 通常对应 Microsoft Defender Antivirus 服务启动。

## 2. 正常条件
```text
服务为 WinDefend
路径为 Windows Defender 常见目录
签名为 Microsoft
服务启动类型符合策略
```

## 3. 异常条件
```text
MsMpEng.exe 路径异常
签名异常
服务配置异常
被攻击链尝试停止或禁用
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
- [[Microsoft Defender]]
- [[WinDefend]]
- [[MsMpEng.exe]]
- [[Defender服务异常停止]]
- [[进程创建与运行时异常]]
