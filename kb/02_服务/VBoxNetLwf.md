---
type: service
os: windows
service_name: "VirtualBox NDIS6 Bridged Networking Driver"
display_name: "VBoxNetLwf"
app: "[[VirtualBox]]"
vendor: "Oracle"
service_type: Win32OwnProcess
start_type: unknown
start_account: LocalSystem
image_name: "VBoxNetLwf.sys"
risk_level: medium
confidence: medium
status: active
tags:
  - windows/service
  - service/scenario-baseline
source_row_ids:
  - third-party-service-039
---
# VBoxNetLwf

## 1. 服务说明

`VirtualBox NDIS6 Bridged Networking Driver` 是 `VirtualBox` 相关的常见 Windows 服务名或服务名模式。第三方服务名可能随版本、安装方式和企业定制包变化，应结合路径、签名、启动账户和资产授权共同识别。

## 2. 所属应用

- [[VirtualBox]]

## 3. 常见 ImagePath

```text
C:\Windows\System32\drivers\VBoxNetLwf.sys
```

## 4. 常见启动参数

```text
未统一；以终端服务注册表 ImagePath 为准。
```

## 5. 常见启动账户

```text
LocalSystem 或厂商安装器配置的服务账户；需以终端观测为准。
```

## 6. 常见父进程

- [[services.exe]]

## 7. 常见进程 / 驱动镜像

- [[VBoxNetLwf.sys]]

## 8. 常见注册表位置

```text
HKLM\SYSTEM\CurrentControlSet\Services\VirtualBox NDIS6 Bridged Networking Driver
```

## 9. 常见网络行为

- 更新、远程管理、VPN 隧道、日志转发或管理端通信，取决于应用类别。

## 10. 正常行为

- 与 [[VirtualBox]] 的授权安装、更新、管理或业务功能一致。

## 11. 异常关注点

```text
服务名命中但 ImagePath 不在厂商目录
二进制签名与厂商不一致
未授权资产出现该服务
服务创建时间与异常登录、外联、横向移动接近
服务启动账户权限高于业务需要
```

## 12. 关联关系

- [[VirtualBox]]
- [[服务ImagePath篡改]]
- [[异常服务创建]]
- [[Windows常见应用服务基线清单]]

## 全量来源覆盖

<!-- generated: windows-source-full-coverage -->

- 来源行：`third-party-service-039`，第 392 行
- 所属应用：[[VirtualBox]]
- 进程：[[VBoxNetLwf.exe]]
- 父子关系：[[services.exe -> VBoxNetLwf.exe]]
- 注册表：[[Windows 服务注册表画像]]
- 文件：[[Windows 服务文件与数据画像]]
- 网络：[[Windows 服务网络行为]]
- 证据：[[Windows常见应用全量覆盖清单]]
