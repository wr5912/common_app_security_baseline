---
type: process
os: windows
process_name: winword.exe
app: "[[Microsoft Office]]"
vendor: Microsoft Corporation
role:
  - Office文档进程
risk_level: medium
confidence: medium
status: active
tags:
  - process/office
  - vendor/microsoft
---

# winword.exe

## 1. 进程说明
`winword.exe` 是 Microsoft Word 进程。安全分析中，Word 拉起脚本解释器、下载器、系统工具时需要重点关注。

## 2. 所属应用
- [[Microsoft Office]]

## 3. 常见父进程
- [[explorer.exe]]
- `outlook.exe`，邮件附件打开场景
- 浏览器进程，下载后打开场景

## 4. 常见子进程
正常情况下，Word 不应频繁拉起脚本解释器。

高关注关系：

- [[winword.exe -> powershell.exe]]
- [[winword.exe -> cmd.exe]]

## 5. 进程创建基线
<!-- baseline:process-creation-runtime -->
- 父进程基线：优先参考“常见父进程”和已建 `process_relation` 页面；服务型进程通常由 [[services.exe]] 启动，用户交互型进程通常由 [[explorer.exe]]、主程序或更新器启动。
- 启动账户基线：服务型进程需与服务画像中的启动账户、ImagePath、资产角色和授权范围一致；用户态进程需与登录用户、交互动作和启动来源一致。
- 路径基线：可执行文件应位于系统目录、厂商安装目录或企业授权部署目录；从用户可写目录、临时目录、下载目录、网络共享或异常挂载路径启动需要提高关注。

## 6. 启动参数基线
<!-- baseline:process-creation-runtime -->
- 常见参数：记录服务模式、更新模式、用户交互模式、配置文件路径、插件/扩展路径等稳定参数类别；不要把单一版本样本写成全局白名单。
- 高风险参数：隐藏窗口、绕过策略、内联脚本、下载执行、异常代理、异常配置目录、调试/注入、凭据或令牌相关参数需要结合上下文研判。
- 动态情报边界：签名、哈希、信誉、首次出现时间和样本流行度由 EDR、资产台账或情报系统提供，本库只记录应核验的字段和异常条件。

## 7. 运行时行为基线
<!-- baseline:process-creation-runtime -->
- 子进程：运行时拉起的子进程应符合“常见子进程”和父子关系画像；拉起脚本解释器、系统管理工具、下载器或未知二进制需要提高关注。
- 文件与注册表/配置：文件落点、配置读取、日志写入、注册表或 Linux 配置路径访问应与对应画像一致；新增持久化位置、敏感文件访问或异常写入需要补证据。
- 网络行为：监听端口、目的域名/IP、协议和代理设置应与网络行为画像一致；异常外联、非授权代理、数据上传或与命令执行相邻出现需要提高关注。

## 8. 安全关注点
```text
winword.exe -> powershell.exe
winword.exe -> cmd.exe
winword.exe -> wscript.exe
winword.exe -> mshta.exe
winword.exe 写入启动项或服务
winword.exe 下载并执行文件
```

<!-- baseline:process-creation-runtime -->
- 进程创建链路与画像不一致：父进程、启动账户、路径、命令行或启动方式偏离常见画像。
- 运行时行为与画像不一致：子进程、文件、注册表/配置、网络目的地址或持久化行为无法由所属应用解释。
- 与高风险上下文相邻：新服务创建、权限提升、异常登录、下载落地、脚本解释器执行、数据打包或横向移动同时出现。
- 误报降级条件：资产已授权、路径和账户符合部署规范、命令行固定可解释、网络目的地址符合业务用途且无异常相邻事件。

## 9. 证据需求
<!-- baseline:process-creation-runtime -->
- 进程创建证据：时间、主机、用户、进程 GUID/PID、父进程 GUID/PID、完整命令行、当前目录、启动账户、完整镜像路径。
- 运行时证据：子进程链路、文件/注册表/配置访问、网络连接、监听端口、模块加载、服务/计划任务/Run Key 或 systemd/cron 变化。
- 外部核验：签名、哈希、证书链、信誉、首次出现时间、资产授权和变更单由 EDR、资产台账、软件分发或情报系统核验；不要把这些动态值沉淀为 Markdown 白名单。

## 10. 关联安全基线
- [[Office拉起脚本解释器]]
- [[进程创建与运行时异常]]
