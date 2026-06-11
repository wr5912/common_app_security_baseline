---
type: app
os: windows
app_name_cn: "Microsoft OneDrive"
app_name_en: "Microsoft OneDrive"
vendor: "Microsoft OneDrive"
category: "云盘 / 文件同步"
confidence: medium
status: active
source_row_ids:
  - third-party-service-022
tags:
  - app/windows-source-full-coverage
---

# Microsoft OneDrive

<!-- generated: windows-source-full-coverage -->

## 1. 基本说明

本页由 `/tmp/windows系统上常见应用.md` 的规范化覆盖清单生成，用于把来源中的应用、组件或厂商服务纳入终端安全基线画像。

## 2. 相关服务

- [[Microsoft OneDrive - OneDrive Updater* 服务模式]]

## 3. 相关进程

- [[OneDriveUpdater.exe]]

## 4. 常见启动方式

- [[Windows Service]]
- [[Scheduled Task]]
- [[Run Key]]

## 5. 常见父子进程关系

- [[services.exe -> OneDriveUpdater.exe]]

## 6. 常见文件与数据

- [[Microsoft OneDrive 文件与数据画像]]

## 7. 常见注册表信息

- [[Microsoft OneDrive 注册表画像]]
- [[HKLM_SYSTEM_CurrentControlSet_Services]]

## 8. 常见网络行为

- [[Microsoft OneDrive 网络行为]]

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

- [[Microsoft OneDrive 画像证据记录]]
- [[Windows常见应用全量覆盖清单]]
