---
type: file_artifact
os: windows
confidence: medium
status: active
tags:
  - generated/windows-source-full-coverage
source_row_ids:
  - third-party-service-069
  - third-party-service-070
  - third-party-service-071
  - third-party-service-072
---
# IIS 文件与数据画像

<!-- generated: windows-source-full-coverage -->

## 1. 数据说明

[[IIS]] 的安装目录、配置、日志、缓存或用户态数据位置模式。

## 2. 相关进程

- [[AppHostSvc.exe]]
- [[IISADMIN.exe]]
- [[W3SVC.exe]]
- [[WAS.exe]]

## 3. 安全关注点

```text
二进制、配置或日志位于用户可写目录
配置中出现凭据、令牌、远控会话或数据库连接串
文件落地时间与异常服务创建、外联或登录接近
```

## 4. 来源行

```text
third-party-service-069, third-party-service-070, third-party-service-071, third-party-service-072
```
