---
type: process
os: windows
process_name: vmware-usbarbitrator64.exe
app: "[[VMware Workstation]]"
vendor: VMware
role:
  - USB 透传仲裁
  - 虚拟化辅助服务
risk_level: medium
confidence: low
status: needs_review
tags:
  - process/virtualization
  - windows/service-process
---

# vmware-usbarbitrator64.exe

## 1. 进程说明
`vmware-usbarbitrator64.exe` 是 [[VMware Workstation]] USB Arbitration Service 常见进程名，用于虚拟机 USB 设备透传相关场景。

## 2. 所属应用
- [[VMware Workstation]]

## 3. 常见路径
```text
C:\Program Files (x86)\Common Files\VMware\USB\vmware-usbarbitrator64.exe
```

## 4. 常见父进程
- [[services.exe]]

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
路径不在 VMware 官方目录
签名厂商不一致
非虚拟化资产出现该服务或进程
USB 透传服务与异常外设访问、数据拷贝或横向移动时间接近
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

## 10. 证据与来源
- 来源类型：[[Windows常见应用服务基线清单]]
- 可信度：low
- 待验证：需用真实终端样本确认 VMware 版本、路径和签名。

## 11. 关联安全基线
- [[进程创建与运行时异常]]
