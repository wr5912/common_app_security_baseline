---
type: process_relation
os: windows
parent_process: "[[services.exe]]"
child_process: "[[splunkd.exe]]"
relation: service_start
normality: normal
risk_level: medium
confidence: medium
status: active
tags:
  - relation/windows-app-profile
---

# services.exe -> splunkd.exe

<!-- generated: windows-complete-profile-backfill -->

## 1. 关系说明
`services.exe` 启动 `splunkd.exe` 是 [[Splunk Universal Forwarder]] 画像中的常见进程链路之一。判断时必须结合路径、签名、命令行、启动账户、用户交互、服务注册表和网络行为。

## 2. 正常条件
```text
应用已授权安装
父进程、子进程路径和签名符合画像
命令行参数符合服务、更新、用户交互或管理场景
启动时间与用户操作、系统启动或企业变更记录一致
```

## 3. 异常条件
```text
子进程从用户目录、临时目录、下载目录或网络共享启动
命令行包含隐藏执行、下载执行、远程控制、凭据访问或异常代理参数
关系首次出现且伴随异常登录、服务创建、外联、文件落地或权限提升
签名、哈希、公司名或版本信息与应用不一致
```

## 4. 证据需求
<!-- baseline:process-creation-runtime -->
- 进程创建事件：父子进程 GUID/PID、完整命令行、启动用户、当前目录、镜像路径、会话 ID 和完整时间线。
- 关联上下文：服务注册表或 systemd unit、启动方式、文件落地、网络连接、持久化写入、用户交互和资产授权记录。
- 外部核验：签名、哈希、信誉和流行度由情报/EDR/资产系统提供，本页只记录需要核验这些字段。

## 5. 推荐处置
核验资产授权、服务 ImagePath、文件签名、父子进程时间线、网络目的地址和同主机相邻事件；不要只凭进程名定性。

## 6. 创建链路基线
<!-- baseline:process-creation-runtime -->
- 结构化关系：本页 `父进程 -> 子进程` 是可抽取的父子关系事实，判断时优先使用本页 frontmatter、标题和双链，不只依赖正文自然语言。
- 正常性判断：结合父进程来源、子进程路径、完整命令行、启动账户、服务/启动方式、所属应用和资产授权确认。
- 上下文边界：同一父子关系在服务启动、用户交互、更新器、插件、脚本执行或攻击链上下文中的风险等级可能不同。

## 7. 高风险参数与命令行关注
<!-- baseline:process-creation-runtime -->
- 命令行与子进程角色不匹配，例如服务进程携带隐藏执行、下载执行、内联脚本、异常代理、异常配置目录或凭据相关参数。
- 子进程路径位于用户可写目录、临时目录、下载目录、网络共享或与所属应用不一致的位置。
- 父进程与业务上下文不匹配，例如 Office、浏览器、PDF 阅读器或远控进程拉起脚本解释器、系统管理工具或未知二进制。

## 8. 关联画像
- [[Splunk Universal Forwarder]]
- [[services.exe]]
- [[splunkd.exe]]
- [[SplunkForwarder]]
- [[进程创建与运行时异常]]
## 9. 关联安全基线
- [[企业安全代理服务常驻]]
