---
type: registry_pattern
os: windows
hive: HKLM/HKCU
key_pattern: "Microsoft SQL Server 注册表画像"
purpose:
  - service_config
  - app_config
  - uninstall_inventory
risk_level: medium
confidence: medium
status: active
tags:
  - registry/windows-app-profile
source_row_ids:
  - third-party-service-043
  - third-party-service-044
  - third-party-service-045
  - third-party-service-046
  - third-party-service-047
  - third-party-service-048
---
# Microsoft SQL Server 注册表画像

<!-- generated: windows-complete-profile-backfill -->

## 1. 注册表用途

本页记录 [[Microsoft SQL Server]] 相关服务、应用配置和卸载信息的注册表位置模式。服务类应用优先核验 `ImagePath`、`ObjectName`、`Start`、`Type`、`FailureActions` 和 `DelayedAutoStart`。

## 2. 常见字段

```text
HKCU\SOFTWARE\Microsoft\*
HKLM\SOFTWARE\Microsoft\*
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*
HKLM\SYSTEM\CurrentControlSet\Services\MSSQLSERVER
HKLM\SYSTEM\CurrentControlSet\Services\SQL Server Agent
HKLM\SYSTEM\CurrentControlSet\Services\SQL Server Browser
HKLM\SYSTEM\CurrentControlSet\Services\SQL Server 默认实例
HKLM\SYSTEM\CurrentControlSet\Services\SQLBrowser
HKLM\SYSTEM\CurrentControlSet\Services\SQLSERVERAGENT
```

## 3. 正常写入来源

- 厂商安装器、更新器、企业软件分发系统或管理员变更。
- Windows 内置组件由系统安装、组件服务或组策略维护。

## 4. 高风险变化

```text
ImagePath 指向用户目录、临时目录、下载目录或网络共享
ObjectName 权限高于业务需要
Start 被改为 Auto 且缺少变更记录
服务项创建时间与异常登录、外联、横向移动或文件落地接近
卸载信息与实际二进制路径、签名厂商不一致
```

## 5. 关联启动方式

- [[Windows Service]]
- [[Run Key]]

## 6. 关联安全基线

- [[异常服务创建]]
- [[服务ImagePath篡改]]
- [[Windows常见应用完整画像验收清单]]
