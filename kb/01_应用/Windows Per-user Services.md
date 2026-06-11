---
type: app
os: windows
app_name_cn: "Windows Per-user Services"
app_name_en: "Windows Per-user Services"
vendor: "Windows Per-user Services"
category: "2. Windows 用户级服务 / Per-user services"
confidence: medium
status: active
source_row_ids:
  - win-per-user-001
  - win-per-user-002
  - win-per-user-003
  - win-per-user-004
  - win-per-user-005
  - win-per-user-006
  - win-per-user-007
  - win-per-user-008
  - win-per-user-009
  - win-per-user-010
  - win-per-user-011
  - win-per-user-012
  - win-per-user-013
  - win-per-user-014
  - win-per-user-015
  - win-per-user-016
  - win-per-user-017
  - win-per-user-018
  - win-per-user-019
  - win-per-user-020
  - win-per-user-021
  - win-per-user-022
  - win-per-user-023
  - win-per-user-024
tags:
  - app/windows-source-full-coverage
---

# Windows Per-user Services

<!-- generated: windows-source-full-coverage -->

## 1. 基本说明

本页由 `/tmp/windows系统上常见应用.md` 的规范化覆盖清单生成，用于把来源中的应用、组件或厂商服务纳入终端安全基线画像。

## 2. 相关服务

- [[AarSvc]]
- [[BcastDVRUserService]]
- [[BluetoothUserService]]
- [[CDPUserSvc]]
- [[CaptureService]]
- [[CloudBackupRestoreSvc]]
- [[ConsentUxUserSvc]]
- [[CredentialEnrollmentManagerUserSvc]]
- [[DeviceAssociationBroker]]
- [[DevicePickerUserSvc]]
- [[DevicesFlowUserSvc]]
- [[MessagingService]]
- [[NPSMSvc]]
- [[OneSyncSvc]]
- [[PenService]]
- [[PimIndexMaintenanceSvc]]
- [[PrintWorkflowUserSvc]]
- [[UdkUserSvc]]
- [[UnistoreSvc]]
- [[UserDataSvc]]
- [[Windows Per-user Services - P9RdrSvc / P9RdrService 服务模式]]
- [[WpnUserService]]
- [[cbdhsvc]]
- [[webthreatdefusersvc]]

## 3. 相关进程

- [[svchost.exe]]

## 4. 常见启动方式

- [[Windows Service]]
- [[Scheduled Task]]
- [[Run Key]]

## 5. 常见父子进程关系

- [[services.exe -> svchost.exe]]

## 6. 常见文件与数据

- [[Windows Per-user Services 文件与数据画像]]

## 7. 常见注册表信息

- [[Windows Per-user Services 注册表画像]]
- [[HKLM_SYSTEM_CurrentControlSet_Services]]

## 8. 常见网络行为

- [[Windows Per-user Services 网络行为]]

## 9. 异常关注点

```text
服务二进制或主程序位于用户可写目录、临时目录、下载目录或网络共享
服务启动账户、ImagePath、签名、命令行或网络目的地址与企业授权不一致
安装、服务创建、首次外联、异常登录或权限提升在时间线上接近
```

## 10. 关联安全基线

- [[第三方服务异常常驻]]
- [[应用异常网络外联行为]]
- [[应用敏感文件与配置访问异常]]

## 11. 证据与来源

- [[Windows Per-user Services 画像证据记录]]
- [[Windows常见应用全量覆盖清单]]
