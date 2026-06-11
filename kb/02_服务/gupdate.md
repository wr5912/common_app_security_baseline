---
type: service
os: windows
service_name: gupdate
display_name: Google Update Service
app: "[[Google Chrome]]"
vendor: Google LLC
service_type: Win32OwnProcess
start_type: auto
start_account: LocalSystem
image_name: GoogleUpdate.exe
risk_level: low
confidence: medium
status: active
tags:
  - service/update
  - vendor/google
  - windows/service
source_row_ids:
  - third-party-service-004
---
# gupdate

## 1. 服务说明

`gupdate` 通常是 Google 软件更新服务，用于 Chrome 等 Google 软件的自动更新。

## 2. 所属应用

- [[Google Chrome]]

## 3. 常见 ImagePath

```text
"C:\Program Files (x86)\Google\Update\GoogleUpdate.exe" /svc
```

## 4. 常见启动参数

```text
/svc
```

## 5. 常见启动账户

```text
LocalSystem
```

## 6. 常见父进程

- [[services.exe]]

## 7. 常见进程

- [[GoogleUpdate.exe]]

## 8. 常见注册表位置

```text
HKLM\SYSTEM\CurrentControlSet\Services\gupdate
HKLM\Software\Google\Update
HKLM\Software\WOW6432Node\Google\Update
```

## 9. 常见网络行为

- [[Google Update Network]]

## 10. 正常行为

- 周期性检查更新。
- 下载更新包。
- 写入更新配置和日志。

## 11. 异常关注点

```text
ImagePath 指向非 Google 官方目录
GoogleUpdate.exe 无签名或签名异常
服务参数不是 /svc
服务访问非预期域名
服务 ImagePath 被篡改
```

## 12. 关联关系

- [[services.exe -> GoogleUpdate.exe]]
- [[更新器外联行为]]

## 全量来源覆盖

<!-- generated: windows-source-full-coverage -->

- 来源行：`third-party-service-004`，第 293 行
- 所属应用：[[Google Chrome]]
- 进程：[[GoogleUpdate.exe]]
- 父子关系：[[services.exe -> GoogleUpdate.exe]]
- 注册表：[[Windows 服务注册表画像]]
- 文件：[[Windows 服务文件与数据画像]]
- 网络：[[Windows 服务网络行为]]
- 证据：[[Windows常见应用全量覆盖清单]]
