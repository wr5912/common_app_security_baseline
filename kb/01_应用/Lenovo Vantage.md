---
type: app
os: windows
app_name_cn: "Lenovo Vantage"
app_name_en: "Lenovo Vantage"
vendor: "Lenovo Vantage"
category: "硬件厂商 / 驱动辅助服务"
confidence: medium
status: active
source_row_ids:
  - third-party-service-094
tags:
  - app/windows-source-full-coverage
---

# Lenovo Vantage

<!-- generated: windows-source-full-coverage -->

## 1. 基本说明

本页由 `/tmp/windows系统上常见应用.md` 的规范化覆盖清单生成，用于把来源中的应用、组件或厂商服务纳入终端安全基线画像。

## 2. 相关服务

- [[LenovoVantageService]]

## 3. 相关进程

- [[LenovoVantageService.exe]]

## 4. 常见启动方式

- [[Windows Service]]
- [[Scheduled Task]]
- [[Run Key]]

## 5. 常见父子进程关系

- [[services.exe -> LenovoVantageService.exe]]

## 6. 常见文件与数据

- [[Lenovo Vantage 文件与数据画像]]

## 7. 常见注册表信息

- [[Lenovo Vantage 注册表画像]]
- [[HKLM_SYSTEM_CurrentControlSet_Services]]

## 8. 常见网络行为

- [[Lenovo Vantage 网络行为]]

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

- [[Lenovo Vantage 画像证据记录]]
- [[Windows常见应用全量覆盖清单]]
