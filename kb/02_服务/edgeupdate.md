---
type: service
os: windows
service_name: edgeupdate
display_name: Microsoft Edge Update Service
app: "[[Microsoft Edge]]"
vendor: Microsoft Corporation
service_type: Win32OwnProcess
start_type: auto
start_account: LocalSystem
image_name: MicrosoftEdgeUpdate.exe
risk_level: low
confidence: medium
status: active
tags:
  - service/update
  - vendor/microsoft
  - windows/service
source_row_ids:
  - third-party-service-001
  - win-builtin-092
---
# edgeupdate

## 1. 服务说明

`edgeupdate` 是 Microsoft Edge 更新服务之一，用于维护 Edge 浏览器更新。

## 2. 所属应用

- [[Microsoft Edge]]

## 3. 常见 ImagePath

```text
C:\Program Files (x86)\Microsoft\EdgeUpdate\MicrosoftEdgeUpdate.exe /svc
```

## 4. 常见父进程

- [[services.exe]]

## 5. 异常关注点

```text
路径异常
签名异常
访问非预期域名
ImagePath 被篡改
```

## 6. 关联安全基线

- [[更新器外联行为]]

## 全量来源覆盖

<!-- generated: windows-source-full-coverage -->

- 来源行：`win-builtin-092`，第 104 行
- 所属应用：[[Windows Service Host]]
- 进程：[[svchost.exe]]
- 父子关系：[[services.exe -> svchost.exe]]
- 注册表：[[Windows 服务注册表画像]]
- 文件：[[Windows 服务文件与数据画像]]
- 网络：[[Windows 服务网络行为]]
- 证据：[[Windows常见应用全量覆盖清单]]
