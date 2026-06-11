---
type: service
os: windows
service_name: "Elastic Agent"
display_name: "Elastic Agent"
app: "[[Elastic Agent]]"
vendor: "Elastic"
service_type: Win32OwnProcess
start_type: unknown
start_account: LocalSystem
image_name: "elastic-agent.exe"
risk_level: medium
confidence: low
status: needs_review
tags:
  - windows/service
  - service/scenario-baseline
---

# Elastic Agent

## 1. 服务说明

`Elastic Agent` 是 `Elastic Agent` 相关的常见 Windows 服务名或服务名模式。第三方服务名可能随版本、安装方式和企业定制包变化，应结合路径、签名、启动账户和资产授权共同识别。

## 2. 所属应用

- [[Elastic Agent]]

## 3. 常见 ImagePath

```text
C:\Program Files\Elastic\Agent\elastic-agent.exe
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

## 7. 常见进程

- [[elastic-agent.exe]]

## 8. 常见注册表位置

```text
HKLM\SYSTEM\CurrentControlSet\Services\Elastic Agent
```

## 9. 常见网络行为

- 更新、远程管理、VPN 隧道、日志转发或管理端通信，取决于应用类别。

## 10. 正常行为

- 与 [[Elastic Agent]] 的授权安装、更新、管理或业务功能一致。

## 11. 异常关注点

```text
服务名命中但 ImagePath 不在厂商目录
二进制签名与厂商不一致
未授权资产出现该服务
服务创建时间与异常登录、外联、横向移动接近
服务启动账户权限高于业务需要
```

## 12. 关联关系

- [[Elastic Agent]]
- [[服务ImagePath篡改]]
- [[异常服务创建]]
- [[Windows常见应用服务基线清单]]
