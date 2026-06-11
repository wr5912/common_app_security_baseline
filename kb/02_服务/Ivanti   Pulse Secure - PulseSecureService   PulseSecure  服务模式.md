---
type: service
os: windows
service_name: "PulseSecureService / PulseSecure*"
display_name: "Ivanti / Pulse Secure"
app: "[[Ivanti / Pulse Secure]]"
vendor: "Ivanti / Pulse Secure"
service_type: windows_service
start_type: auto_or_manual
start_account: LocalSystem_or_service_account
image_name: "PulseSecureService.exe"
risk_level: medium
confidence: medium
status: active
source_row_ids:
  - third-party-vpn-009
tags:
  - service/windows-source-full-coverage
aliases:
  - "Ivanti / Pulse Secure - PulseSecureService / PulseSecure* 服务模式"

---
# Ivanti / Pulse Secure - PulseSecureService / PulseSecure* 服务模式

<!-- generated: windows-source-full-coverage -->

## 1. 服务说明

来源行 `third-party-vpn-009`（第 368 行）记录了 `PulseSecureService / PulseSecure*`，说明为：企业 VPN。

## 2. 所属应用

- [[Ivanti / Pulse Secure]]

## 3. 常见 ImagePath

```text
来源清单未提供完整 ImagePath；应以后续终端服务注册表、EDR 或资产扫描结果补强。
```

## 4. 常见启动方式

- [[Windows Service]]

## 5. 常见父进程与进程

- [[services.exe]]
- [[PulseSecureService.exe]]
- [[services.exe -> PulseSecureService.exe]]

## 6. 常见注册表位置

- [[Windows 服务注册表画像]]
- [[HKLM_SYSTEM_CurrentControlSet_Services]]

## 7. 常见文件与数据

- [[Windows 服务文件与数据画像]]
- [[Ivanti / Pulse Secure 文件与数据画像]]

## 8. 常见网络行为

- [[Windows 服务网络行为]]
- [[Ivanti / Pulse Secure 网络行为]]

## 9. 异常关注点

```text
ImagePath 指向用户目录、临时目录、下载目录或网络共享
启动账户权限高于业务需要
服务创建、ImagePath 修改、首次外联和异常登录在时间线上接近
服务名与系统服务或常见软件服务相似但路径、签名或厂商不一致
```

## 10. 关联安全基线

- [[Windows服务ImagePath异常]]
- [[第三方服务异常常驻]]
- [[Windows常见应用全量覆盖清单]]
