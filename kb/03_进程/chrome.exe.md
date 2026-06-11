---
type: process
os: windows
process_name: chrome.exe
app: "[[Google Chrome]]"
vendor: Google LLC
role:
  - 主进程
  - 渲染进程
  - GPU进程
  - 网络进程
risk_level: medium
confidence: medium
status: active
tags:
  - process/browser
  - process/multiprocess
  - vendor/google
---

# chrome.exe

## 1. 进程说明
`chrome.exe` 是 Google Chrome 的主进程和子进程名称。不同角色通常通过命令行参数区分。

## 2. 所属应用
- [[Google Chrome]]

## 3. 常见路径
```text
C:\Program Files\Google\Chrome\Application\chrome.exe
C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe
```

## 4. 常见父进程
- [[explorer.exe]]
- [[chrome.exe]]

## 5. 常见子进程
- [[chrome.exe]]
- `crashpad_handler.exe`，待建页面
- [[cmd.exe]]
- [[powershell.exe]]

## 6. 进程创建基线
<!-- baseline:process-creation-runtime -->
- 父进程基线：优先参考“常见父进程”和已建 `process_relation` 页面；服务型进程通常由 [[services.exe]] 启动，用户交互型进程通常由 [[explorer.exe]]、主程序或更新器启动。
- 启动账户基线：服务型进程需与服务画像中的启动账户、ImagePath、资产角色和授权范围一致；用户态进程需与登录用户、交互动作和启动来源一致。
- 路径基线：可执行文件应位于系统目录、厂商安装目录或企业授权部署目录；从用户可写目录、临时目录、下载目录、网络共享或异常挂载路径启动需要提高关注。

## 7. 启动参数基线
```text
--type=renderer
--type=gpu-process
--type=utility
--type=crashpad-handler
--profile-directory=
--user-data-dir=
--disable-features=
--load-extension=
--proxy-server=
```

<!-- baseline:process-creation-runtime -->
- 常见参数：记录服务模式、更新模式、用户交互模式、配置文件路径、插件/扩展路径等稳定参数类别；不要把单一版本样本写成全局白名单。
- 高风险参数：隐藏窗口、绕过策略、内联脚本、下载执行、异常代理、异常配置目录、调试/注入、凭据或令牌相关参数需要结合上下文研判。
- 动态情报边界：签名、哈希、信誉、首次出现时间和样本流行度由 EDR、资产台账或情报系统提供，本库只记录应核验的字段和异常条件。

## 8. 运行时行为基线
<!-- baseline:process-creation-runtime -->
- 子进程：运行时拉起的子进程应符合“常见子进程”和父子关系画像；拉起脚本解释器、系统管理工具、下载器或未知二进制需要提高关注。
- 文件与注册表/配置：文件落点、配置读取、日志写入、注册表或 Linux 配置路径访问应与对应画像一致；新增持久化位置、敏感文件访问或异常写入需要补证据。
- 网络行为：监听端口、目的域名/IP、协议和代理设置应与网络行为画像一致；异常外联、非授权代理、数据上传或与命令执行相邻出现需要提高关注。

## 9. 安全关注点
| 参数 | 常见含义 | 关注点 |
|---|---|---|
| `--type=renderer` | 渲染进程 | 正常 |
| `--type=gpu-process` | GPU 进程 | 正常 |
| `--user-data-dir=` | 指定用户数据目录 | 指向异常目录需关注 |
| `--load-extension=` | 加载扩展 | 可能加载恶意扩展 |
| `--proxy-server=` | 指定代理 | 异常代理需关注 |

<!-- baseline:process-creation-runtime -->
- 进程创建链路与画像不一致：父进程、启动账户、路径、命令行或启动方式偏离常见画像。
- 运行时行为与画像不一致：子进程、文件、注册表/配置、网络目的地址或持久化行为无法由所属应用解释。
- 与高风险上下文相邻：新服务创建、权限提升、异常登录、下载落地、脚本解释器执行、数据打包或横向移动同时出现。
- 误报降级条件：资产已授权、路径和账户符合部署规范、命令行固定可解释、网络目的地址符合业务用途且无异常相邻事件。
## 10. 异常行为
```text
chrome.exe -> powershell.exe
chrome.exe -> cmd.exe
chrome.exe 从 Temp / Downloads / Public 目录启动
chrome.exe 使用异常代理或异常扩展目录
```

高关注关系：

- [[chrome.exe -> powershell.exe]]
- [[chrome.exe -> cmd.exe]]

## 11. 证据需求
<!-- baseline:process-creation-runtime -->
- 进程创建证据：时间、主机、用户、进程 GUID/PID、父进程 GUID/PID、完整命令行、当前目录、启动账户、完整镜像路径。
- 运行时证据：子进程链路、文件/注册表/配置访问、网络连接、监听端口、模块加载、服务/计划任务/Run Key 或 systemd/cron 变化。
- 外部核验：签名、哈希、证书链、信誉、首次出现时间、资产授权和变更单由 EDR、资产台账、软件分发或情报系统核验；不要把这些动态值沉淀为 Markdown 白名单。

## 12. 关联安全基线
- [[浏览器拉起脚本解释器]]
- [[进程创建与运行时异常]]
