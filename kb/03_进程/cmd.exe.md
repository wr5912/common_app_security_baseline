---
type: process
os: windows
process_name: cmd.exe
app: "[[Windows Shell]]"
vendor: Microsoft Corporation
role:
  - 命令解释器
  - 系统管理工具
risk_level: high
confidence: medium
status: active
tags:
  - process/script
  - process/cmd
  - risk/high
---

# cmd.exe

## 1. 进程说明
`cmd.exe` 是 Windows 命令解释器，常用于交互式命令、批处理脚本和系统管理。安全分析中，Office、浏览器、PDF 阅读器、远控进程或服务进程异常拉起 `cmd.exe` 需要重点关注。

## 2. 所属应用
- [[Windows Shell]]

## 3. 常见路径
```text
C:\Windows\System32\cmd.exe
C:\Windows\SysWOW64\cmd.exe
```

## 4. 常见父进程
- [[explorer.exe]]
- [[powershell.exe]]
- [[services.exe]]

高关注父进程：

- [[winword.exe]]
- [[chrome.exe]]

## 5. 常见子进程
```text
批处理脚本、系统工具、解释器或业务程序。拉起 powershell、wscript、mshta、rundll32、regsvr32、certutil、bitsadmin 等需要结合上下文研判。
```

## 6. 进程创建基线
<!-- baseline:process-creation-runtime -->
- 父进程基线：交互式打开命令提示符通常由 [[explorer.exe]] 或终端工具启动；服务或脚本链路中出现需结合服务、计划任务、批处理来源和授权状态确认。
- 启动账户基线：用户交互场景应与登录用户一致；服务、计划任务或远程管理场景应与授权账号和变更记录一致。
- 路径基线：应来自 Windows 系统目录；从用户可写目录、临时目录、下载目录或网络共享出现 `cmd.exe` 同名文件需要提高关注。

## 7. 启动参数基线
```text
/c
/k
/s
/q
```

<!-- baseline:process-creation-runtime -->
- 常见参数：`/c` 执行后退出，`/k` 执行后保留窗口；批处理、安装脚本和运维脚本常见。
- 高风险参数：链式命令、重定向、base64/十六进制解码、下载执行、隐藏窗口、绕过策略、异常代理、凭据或令牌相关命令需要提高关注。
- 动态情报边界：签名、哈希、信誉、首次出现时间和样本流行度由 EDR、资产台账或情报系统提供，本库只记录应核验的字段和异常条件。

## 8. 运行时行为基线
<!-- baseline:process-creation-runtime -->
- 子进程：应能由批处理脚本、安装器、运维任务或用户交互解释；拉起脚本解释器、下载器、凭据工具或未知二进制需要提高关注。
- 文件与注册表：临时脚本落地、Run Key、服务创建、计划任务写入或敏感文件访问需要补证据。
- 网络行为：`cmd.exe` 自身通常不直接承载业务外联；若紧邻下载器、代理、隧道或数据上传行为，需要按攻击链上下文研判。

## 9. 安全关注点
```text
Office / 浏览器 / PDF 阅读器拉起 cmd.exe
cmd.exe 链式执行 powershell / wscript / mshta / rundll32 / regsvr32
命令中出现下载执行、编码混淆、凭据访问、服务创建或持久化写入
从非系统路径出现 cmd.exe 同名文件
```

<!-- baseline:process-creation-runtime -->
- 进程创建链路与画像不一致：父进程、启动账户、路径、命令行或启动方式偏离常见画像。
- 运行时行为与画像不一致：子进程、文件、注册表/配置、网络目的地址或持久化行为无法由所属应用解释。
- 与高风险上下文相邻：新服务创建、权限提升、异常登录、下载落地、脚本解释器执行、数据打包或横向移动同时出现。
- 误报降级条件：资产已授权、路径和账户符合部署规范、命令行固定可解释、网络目的地址符合业务用途且无异常相邻事件。

## 10. 证据需求
<!-- baseline:process-creation-runtime -->
- 进程创建证据：时间、主机、用户、进程 GUID/PID、父进程 GUID/PID、完整命令行、当前目录、启动账户、完整镜像路径。
- 运行时证据：子进程链路、文件/注册表/配置访问、网络连接、监听端口、模块加载、服务/计划任务/Run Key 变化。
- 外部核验：签名、哈希、证书链、信誉、首次出现时间、资产授权和变更单由 EDR、资产台账、软件分发或情报系统核验；不要把这些动态值沉淀为 Markdown 白名单。

## 11. 关联安全基线
- [[Office拉起脚本解释器]]
- [[浏览器拉起脚本解释器]]
- [[进程创建与运行时异常]]
