---
type: process
os: windows
process_name: vmware-usbarbitrator64.exe
app: "[[VMware Workstation]]"
vendor: VMware
role:
  - USB 透传仲裁
  - 虚拟化辅助服务
risk_level: medium
confidence: low
status: needs_review
tags:
  - process/virtualization
  - windows/service-process
---

# vmware-usbarbitrator64.exe

## 1. 进程说明

`vmware-usbarbitrator64.exe` 是 [[VMware Workstation]] USB Arbitration Service 常见进程名，用于虚拟机 USB 设备透传相关场景。

## 2. 所属应用

- [[VMware Workstation]]

## 3. 常见路径

```text
C:\Program Files (x86)\Common Files\VMware\USB\vmware-usbarbitrator64.exe
```

## 4. 常见父进程

- [[services.exe]]

## 5. 异常行为

```text
路径不在 VMware 官方目录
签名厂商不一致
非虚拟化资产出现该服务或进程
USB 透传服务与异常外设访问、数据拷贝或横向移动时间接近
```

## 6. 证据与来源

- 来源类型：[[Windows常见应用服务基线清单]]
- 可信度：low
- 待验证：需用真实终端样本确认 VMware 版本、路径和签名。
