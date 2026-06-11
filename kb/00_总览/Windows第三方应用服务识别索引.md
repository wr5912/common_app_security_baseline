---
type: index
os: windows
title: Windows第三方应用服务识别索引
status: active
tags:
  - index/service
  - windows/service
---

# Windows第三方应用服务识别索引

## 1. 使用说明

本索引用于从服务名、厂商、路径和进程特征快速识别常见第三方应用服务。服务名模式只作为候选信号，最终判断必须结合签名、ImagePath、启动账户、命令行、资产角色和网络目的地址。

来源页面：[[Windows常见应用服务基线清单]]

## 2. 详细画像入口

### 浏览器 / 文档 / 办公

- [[Mozilla Firefox]]
- [[Brave Browser]]
- [[Adobe Acrobat]]
- [[Foxit Reader]]
- [[WPS Office]]

### 远控 / 运维

- [[TeamViewer]]
- [[RustDesk]]
- [[ToDesk]]
- [[向日葵远控]]
- [[Chrome Remote Desktop]]

### VPN / 组网 / 代理

- [[OpenVPN]]
- [[WireGuard]]
- [[Tailscale]]
- [[ZeroTier]]
- [[GlobalProtect]]
- [[Cisco AnyConnect]]

### 虚拟化 / 开发 / 数据库

- [[Docker Desktop]]
- [[VMware Workstation]]
- [[VirtualBox]]
- [[Microsoft SQL Server]]
- [[MySQL]]
- [[PostgreSQL]]
- [[MongoDB]]
- [[Redis for Windows]]

### 安全 / 日志采集

- [[Microsoft Defender]]
- [[CrowdStrike Falcon]]
- [[SentinelOne]]
- [[Wazuh Agent]]
- [[Splunk Universal Forwarder]]
- [[Elastic Agent]]

## 3. 服务模式清单

下面这部分更适合做“应用服务识别字典”。第三方服务的 ServiceName 经常随版本、安装方式、企业定制包变化，所以建议按 **精确名 + 前缀/包含规则 + 签名厂商 + 路径** 组合识别。

### 浏览器 / 更新器

| ServiceName / 模式              | 应用 / 厂商                              | 常见进程 / 路径特征                              |
| ------------------------------- | ---------------------------------------- | ------------------------------------------------ |
| `edgeupdate`                    | Microsoft Edge Update                    | `MicrosoftEdgeUpdate.exe`                        |
| `edgeupdatem`                   | Microsoft Edge Update                    | `MicrosoftEdgeUpdate.exe /medsvc`                |
| `MicrosoftEdgeElevationService` | Microsoft Edge                           | `elevation_service.exe`                          |
| `gupdate`                       | Google Update Service                    | `GoogleUpdate.exe /svc`                          |
| `gupdatem`                      | Google Update Service                    | `GoogleUpdate.exe /medsvc`                       |
| `GoogleUpdaterService*`         | Google Updater 新版                      | `GoogleUpdaterService.exe`                       |
| `GoogleUpdaterInternalService*` | Google Updater 新版                      | `GoogleUpdater.exe` / `GoogleUpdaterService.exe` |
| `MozillaMaintenance`            | Mozilla Maintenance Service              | `maintenanceservice.exe`                         |
| `BraveElevationService`         | Brave Browser                            | `elevation_service.exe`                          |
| `brave` / `bravem`              | Brave Update Service                     | `BraveUpdate.exe`                                |
| `AdobeARMservice`               | Adobe Acrobat Update Service             | `armsvc.exe`                                     |
| `AdobeUpdateService`            | Adobe Update Service                     | Adobe 更新组件                                   |
| `AGMService`                    | Adobe Genuine Monitor Service            | Adobe Genuine                                    |
| `AGSService`                    | Adobe Genuine Software Integrity Service | Adobe Genuine                                    |

### Office / 协作办公

| ServiceName / 模式                                | 应用 / 厂商                         | 说明                                 |
| ------------------------------------------------- | ----------------------------------- | ------------------------------------ |
| `ClickToRunSvc`                                   | Microsoft Office Click-to-Run       | Office 安装、流式传输、更新          |
| `osppsvc`                                         | Office Software Protection Platform | Office 授权                          |
| `ose`                                             | Office Source Engine，旧版          | Office 安装源维护                    |
| `TeamsUpdater*`                                   | Microsoft Teams，部分安装方式       | 更新器，更多情况下是计划任务         |
| `OneSyncSvc*`                                     | Windows Mail/Calendar/People 同步   | 用户级服务                           |
| `AdobeARMservice`                                 | Adobe Acrobat Reader / Acrobat      | PDF 更新                             |
| `AGSService`                                      | Adobe Genuine                       | 正版校验                             |
| `AGMService`                                      | Adobe Genuine Monitor               | 正版监控                             |
| `FoxitReaderUpdateService` / `FoxitUpdateService` | Foxit Reader                        | PDF 更新                             |
| `Kingsoft*` / `WPS*`                              | WPS Office                          | 更新 / 云同步，名称随版本变化        |
| `Youdao*`                                         | 有道                                | 词典 / 云同步 / 更新，名称随版本变化 |

### 云盘 / 文件同步

| ServiceName / 模式            | 应用 / 厂商                    | 说明                             |
| ----------------------------- | ------------------------------ | -------------------------------- |
| `DbxSvc`                      | Dropbox Service                | Dropbox 同步服务                 |
| `dbupdate`                    | Dropbox Update Service         | Dropbox 更新                     |
| `dbupdatem`                   | Dropbox Update Service Machine | Dropbox 更新                     |
| `GoogleDriveFS`               | Google Drive for desktop       | Google Drive 文件流              |
| `Apple Mobile Device Service` | Apple / iTunes                 | iPhone/iPad 设备通信             |
| `Bonjour Service`             | Apple Bonjour                  | mDNS / 局域网发现                |
| `iPod Service`                | Apple 旧版                     | iPod / iTunes                    |
| `OneDrive Updater*`           | Microsoft OneDrive             | 多数场景是计划任务，不一定是服务 |
| `BaiduNetdisk*`               | 百度网盘                       | 名称随版本变化                   |
| `AliyunDrive*`                | 阿里云盘                       | 名称随版本变化                   |
| `Nutstore*`                   | 坚果云                         | 名称随版本变化                   |

### 远程控制 / 运维工具 / RMM

| ServiceName / 模式                             | 应用 / 厂商           | 说明                     |
| ---------------------------------------------- | --------------------- | ------------------------ |
| `TeamViewer`                                   | TeamViewer            | 远程控制 / 无人值守      |
| `TeamViewer_Service`                           | TeamViewer，部分版本  | 远程控制服务             |
| `AnyDesk Service` / `AnyDesk*Service*`         | AnyDesk               | 远程控制                 |
| `RustDesk` / `RustDesk Service`                | RustDesk              | 远程控制                 |
| `SplashtopRemoteService`                       | Splashtop             | 远程控制                 |
| `SplashtopSoftwareUpdater`                     | Splashtop             | 更新                     |
| `ScreenConnect Client*`                        | ConnectWise Control   | RMM / 远控               |
| `LogMeIn` / `LogMeIn Hamachi Tunneling Engine` | LogMeIn / Hamachi     | 远控 / 虚拟网络          |
| `GoToAssist*`                                  | GoToAssist            | 远程支持                 |
| `Chrome Remote Desktop Service` / `chromoting` | Chrome Remote Desktop | 远程桌面                 |
| `AweSun*`                                      | 向日葵远控            | 远程控制，名称随版本变化 |
| `ToDesk*`                                      | ToDesk                | 远程控制，名称随版本变化 |

### VPN / 组网 / 代理

| ServiceName / 模式                               | 应用 / 厂商                            | 说明                             |
| ------------------------------------------------ | -------------------------------------- | -------------------------------- |
| `OpenVPNService`                                 | OpenVPN                                | VPN                              |
| `OpenVPNServiceInteractive`                      | OpenVPN                                | 交互式 VPN 服务                  |
| `WireGuardTunnel$*`                              | WireGuard                              | 每个隧道一个服务                 |
| `tailscaled`                                     | Tailscale                              | Mesh VPN                         |
| `ZeroTierOneService`                             | ZeroTier                               | Mesh VPN                         |
| `CloudflareWARP`                                 | Cloudflare WARP                        | VPN / Zero Trust                 |
| `PanGPS`                                         | Palo Alto GlobalProtect                | 企业 VPN                         |
| `vpnagent`                                       | Cisco AnyConnect Secure Mobility Agent | 企业 VPN                         |
| `PulseSecureService` / `PulseSecure*`            | Ivanti / Pulse Secure                  | 企业 VPN                         |
| `FortiClient Service Scheduler` / `FA_Scheduler` | Fortinet FortiClient                   | 企业 VPN / 安全                  |
| `Sangfor*`                                       | 深信服 VPN / EDR                       | 名称随组件变化                   |
| `Clash*`                                         | Clash Verge / Clash for Windows        | 代理，很多是用户进程，不一定服务 |
| `v2ray*` / `xray*`                               | V2Ray / Xray                           | 代理，常由 NSSM 注册为服务       |
| `sing-box*`                                      | sing-box                               | 代理，常由用户自定义服务名       |

### 虚拟化 / 容器 / 开发环境

| ServiceName / 模式              | 应用 / 厂商                                | 说明                       |
| ------------------------------- | ------------------------------------------ | -------------------------- |
| `com.docker.service`            | Docker Desktop Service                     | Docker Desktop 后台服务    |
| `LxssManager`                   | Windows Subsystem for Linux                | WSL 管理                   |
| `vmcompute`                     | Hyper-V Host Compute Service               | 容器 / Hyper-V             |
| `hns`                           | Host Network Service                       | Windows 容器网络           |
| `vmms`                          | Hyper-V Virtual Machine Management         | Hyper-V                    |
| `VMAuthdService`                | VMware Authorization Service               | VMware Workstation         |
| `VMnetDHCP`                     | VMware DHCP Service                        | VMware 虚拟网络            |
| `VMware NAT Service`            | VMware NAT                                 | VMware 虚拟网络            |
| `VMUSBArbService`               | VMware USB Arbitration Service             | USB 透传                   |
| `VGAuthService`                 | VMware Alias Manager and Ticket Service    | VMware Tools               |
| `VMTools`                       | VMware Tools                               | VMware Guest               |
| `VBoxSDS`                       | VirtualBox System Service                  | VirtualBox                 |
| `VBoxNetDHCP`                   | VirtualBox DHCP                            | VirtualBox 网络            |
| `VBoxNetLwf`                    | VirtualBox NDIS6 Bridged Networking Driver | VirtualBox 网络驱动        |
| `VSStandardCollectorService150` | Visual Studio Standard Collector           | VS 诊断                    |
| `VSInstallerElevationService`   | Visual Studio Installer Elevation Service  | VS 安装提权                |
| `JetBrainsEtwHost*`             | JetBrains IDE                              | ETW / 诊断，名称随版本变化 |

### 数据库 / 中间件 / 开发服务

| ServiceName / 模式              | 应用 / 厂商                        | 说明       |
| ------------------------------- | ---------------------------------- | ---------- |
| `MSSQLSERVER`                   | Microsoft SQL Server 默认实例      | 数据库     |
| `MSSQL$<INSTANCE>`              | SQL Server 命名实例                | 数据库     |
| `SQLSERVERAGENT`                | SQL Server Agent 默认实例          | 调度       |
| `SQLAgent$<INSTANCE>`           | SQL Server Agent 命名实例          | 调度       |
| `SQLBrowser`                    | SQL Server Browser                 | 实例发现   |
| `SQLWriter`                     | SQL Server VSS Writer              | 备份       |
| `MySQL` / `MySQL80` / `MySQL57` | MySQL                              | 数据库     |
| `MariaDB`                       | MariaDB                            | 数据库     |
| `postgresql-x64-*`              | PostgreSQL                         | 数据库     |
| `MongoDB`                       | MongoDB                            | 数据库     |
| `Redis` / `Redis64`             | Redis for Windows                  | 缓存       |
| `RabbitMQ`                      | RabbitMQ                           | 消息队列   |
| `elasticsearch-service-x64`     | Elasticsearch                      | 搜索       |
| `logstash`                      | Logstash                           | 日志管道   |
| `kibana`                        | Kibana                             | 可视化     |
| `zookeeper`                     | ZooKeeper                          | 协调服务   |
| `kafka`                         | Kafka                              | 消息流     |
| `nats-server`                   | NATS                               | 消息系统   |
| `MinIO`                         | MinIO                              | 对象存储   |
| `influxdb`                      | InfluxDB                           | 时序数据库 |
| `telegraf`                      | Telegraf                           | 指标采集   |
| `grafana`                       | Grafana                            | 可视化     |
| `prometheus`                    | Prometheus                         | 监控       |
| `nginx`                         | Nginx，常由 NSSM 注册              | Web 服务   |
| `Apache2.4`                     | Apache HTTP Server                 | Web 服务   |
| `Tomcat*`                       | Apache Tomcat                      | Java Web   |
| `W3SVC`                         | World Wide Web Publishing Service  | IIS        |
| `WAS`                           | Windows Process Activation Service | IIS        |
| `IISADMIN`                      | IIS Admin Service，旧版            | IIS        |
| `AppHostSvc`                    | Application Host Helper Service    | IIS        |

### 安全软件 / EDR / 杀毒

| ServiceName / 模式                | 应用 / 厂商                     | 说明                     |
| --------------------------------- | ------------------------------- | ------------------------ |
| `WinDefend`                       | Microsoft Defender Antivirus    | 内置杀毒                 |
| `WdNisSvc`                        | Defender Network Inspection     | 网络检查                 |
| `Sense`                           | Microsoft Defender for Endpoint | EDR                      |
| `SecurityHealthService`           | Windows Security Service        | 安全中心                 |
| `wscsvc`                          | Security Center                 | 安全状态聚合             |
| `CSFalconService`                 | CrowdStrike Falcon              | EDR                      |
| `SentinelAgent`                   | SentinelOne                     | EDR                      |
| `CbDefense` / `CarbonBlack`       | VMware Carbon Black             | EDR                      |
| `cyserver` / `CyveraService`      | Palo Alto Cortex XDR，部分版本  | EDR                      |
| `SepMasterService`                | Symantec Endpoint Protection    | 杀毒 / EDR               |
| `ekrn`                            | ESET Service                    | 杀毒                     |
| `AVP`                             | Kaspersky                       | 杀毒                     |
| `VSSERV`                          | Bitdefender                     | 杀毒                     |
| `Sophos Endpoint Defense Service` | Sophos                          | EDR                      |
| `Sophos AutoUpdate Service`       | Sophos                          | 更新                     |
| `ntrtscan`                        | Trend Micro OfficeScan          | 杀毒                     |
| `TmPfw`                           | Trend Micro Firewall            | 防火墙                   |
| `TMBMSRV`                         | Trend Micro                     | 行为监控                 |
| `McAfee Framework Service`        | McAfee Agent                    | 管理代理                 |
| `mfemms`                          | McAfee                          | 安全服务                 |
| `osqueryd`                        | osquery                         | 主机资产 / 安全采集      |
| `WazuhSvc`                        | Wazuh Agent                     | HIDS                     |
| `ossec` / `ossecsvc`              | OSSEC Agent                     | HIDS                     |
| `Zabbix Agent`                    | Zabbix Agent                    | 监控                     |
| `DatadogAgent`                    | Datadog Agent                   | 监控                     |
| `nxlog`                           | NXLog                           | 日志采集                 |
| `WinCollect`                      | IBM QRadar WinCollect           | 日志采集                 |
| `SplunkForwarder`                 | Splunk Universal Forwarder      | 日志采集                 |
| `Elastic Agent`                   | Elastic Agent                   | 安全 / 日志              |
| `filebeat`                        | Filebeat                        | 日志采集                 |
| `packetbeat`                      | Packetbeat                      | 网络采集                 |
| `auditbeat`                       | Auditbeat                       | 审计采集                 |
| `QHActiveDefense` / `360*`        | 360 安全卫士 / 天擎             | 安全防护，名称随版本变化 |
| `HipsDaemon` / `Huorong*`         | 火绒                            | HIPS / 安全防护          |
| `TWatch*` / `TAV*`                | 腾讯电脑管家                    | 安全防护，名称随版本变化 |

### 备份 / 存储 / 终端管理

| ServiceName / 模式               | 应用 / 厂商                            | 说明            |
| -------------------------------- | -------------------------------------- | --------------- |
| `VeeamEndpointBackupSvc`         | Veeam Agent                            | 备份            |
| `VeeamTransportSvc`              | Veeam Transport                        | 备份传输        |
| `AcronisActiveProtectionService` | Acronis                                | 备份 / 勒索防护 |
| `AcronisCyberProtectionService`  | Acronis Cyber Protect                  | 备份 / 安全     |
| `MacriumService`                 | Macrium Reflect                        | 备份            |
| `CcmExec`                        | Microsoft Configuration Manager Client | SCCM 客户端     |
| `IntuneManagementExtension`      | Microsoft Intune Management Extension  | Intune          |
| `HealthService`                  | SCOM / Microsoft Monitoring Agent      | 监控            |
| `WSearch`                        | Windows Search                         | 索引            |
| `LanmanServer`                   | SMB Server                             | 文件共享        |
| `LanmanWorkstation`              | SMB Client                             | 文件访问        |

### 硬件厂商 / 驱动辅助服务

| ServiceName / 模式                          | 应用 / 厂商                                                  | 说明           |
| ------------------------------------------- | ------------------------------------------------------------ | -------------- |
| `NVDisplay.ContainerLocalSystem`            | NVIDIA Display Container LS                                  | NVIDIA 显卡    |
| `NvContainerLocalSystem`                    | NVIDIA Container                                             | NVIDIA         |
| `NvTelemetryContainer`                      | NVIDIA Telemetry，旧版常见                                   | 遥测           |
| `AMD External Events Utility`               | AMD                                                          | 显卡事件       |
| `RtkAudioUniversalService`                  | Realtek Audio Universal Service                              | 声卡           |
| `jhi_service`                               | Intel Dynamic Application Loader Host Interface              | Intel          |
| `LMS`                                       | Intel Management and Security Application Local Management Service | Intel ME       |
| `igfxCUIService*`                           | Intel Graphics Control Panel Service                         | Intel 显卡     |
| `DellClientManagementService`               | Dell Client Management                                       | Dell           |
| `Dell SupportAssist` / `SupportAssistAgent` | Dell SupportAssist                                           | Dell 维护      |
| `LenovoVantageService`                      | Lenovo Vantage                                               | Lenovo         |
| `Lenovo.Modern.ImController`                | Lenovo System Interface Foundation                           | Lenovo         |
| `HPAppHelperCap`                            | HP App Helper                                                | HP             |
| `HPNetworkCap`                              | HP Network HSA Service                                       | HP             |
| `HPPrintScanDoctorService`                  | HP Print and Scan Doctor                                     | HP 打印        |
| `Epson*`                                    | Epson 打印 / 扫描                                            | 名称随驱动变化 |
| `Brother*`                                  | Brother 打印 / 扫描                                          | 名称随驱动变化 |
| `Canon*`                                    | Canon 打印 / 扫描                                            | 名称随驱动变化 |
