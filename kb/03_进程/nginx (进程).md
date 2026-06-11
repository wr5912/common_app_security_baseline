---
type: process
os: linux
process_name: nginx
app: "[[nginx]]"
vendor: nginx / F5
role:
  - web-server
  - reverse-proxy
risk_level: medium
confidence: medium
status: active
tags:
  - process/web-server
  - linux/process
---

# nginx (进程)

## 1. 进程说明
nginx 以一个 master 进程 + 多个 worker 进程运行。master 由 [[nginx.service]] 启动，worker 由 master fork。

## 2. 常见路径
```text
/usr/sbin/nginx
```

## 3. 常见父进程
- [[systemd]]（master）
- nginx master（worker 的父进程）

## 4. 常见子进程
```text
正常情况下 nginx 不应拉起 shell / 解释器
```

## 5. 进程创建基线
<!-- baseline:process-creation-runtime -->
- 父进程基线：守护进程通常由 [[systemd]]、服务管理器或 supervisor 类组件启动；用户交互进程通常由 shell、桌面会话或管理工具启动。
- 启动账户基线：服务进程需与 unit、配置文件、运行用户和资产角色一致；长期 root 运行、异常 setuid 或容器逃逸上下文需要提高关注。
- 路径基线：可执行文件应位于系统包、厂商安装目录或授权部署目录；从 `/tmp`、用户家目录、网络挂载或异常可写目录启动需要提高关注。

## 6. 启动参数基线
<!-- baseline:process-creation-runtime -->
- 常见参数：记录配置文件、前台/后台模式、监听地址、日志路径、插件目录和服务管理参数类别；不要把单一发行版样本写成全局白名单。
- 高风险参数：直接执行 shell、内联脚本、异常下载、LD_PRELOAD/库劫持、异常配置目录、暴露调试端口或凭据参数需要结合上下文研判。
- 动态情报边界：包签名、哈希、信誉、首次出现时间和样本流行度由资产台账、包管理器或情报系统提供，本库只记录应核验的字段和异常条件。

## 7. 运行时行为基线
<!-- baseline:process-creation-runtime -->
- 子进程：运行时拉起的子进程应符合“常见子进程”和父子关系画像；拉起脚本解释器、系统管理工具、下载器或未知二进制需要提高关注。
- 文件与注册表/配置：文件落点、配置读取、日志写入、注册表或 Linux 配置路径访问应与对应画像一致；新增持久化位置、敏感文件访问或异常写入需要补证据。
- 网络行为：监听端口、目的域名/IP、协议和代理设置应与网络行为画像一致；异常外联、非授权代理、数据上传或与命令执行相邻出现需要提高关注。

## 8. 安全关注点
```text
nginx -> sh / bash / python / perl（疑似 webshell 或命令注入）
nginx 进程外联非业务目标
worker 以 root 长期运行且对外暴露
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
- [[服务持久化机制对比]]
- [[进程创建与运行时异常]]
