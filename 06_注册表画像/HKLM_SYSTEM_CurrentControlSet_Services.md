---
type: registry_pattern
hive: HKLM
key_pattern: HKLM\SYSTEM\CurrentControlSet\Services\*
purpose:
  - service_registration
  - driver_registration
risk_level: high
confidence: high
tags:
  - registry/service
  - persistence
  - windows
---

# HKLM\SYSTEM\CurrentControlSet\Services\*

## 1. 注册表用途

该位置保存 Windows 服务和驱动服务配置，包括服务名、启动类型、ImagePath、运行账户、依赖关系等。

## 2. 常见字段

```text
ImagePath
DisplayName
Description
ObjectName
Start
Type
ErrorControl
DependOnService
FailureActions
DelayedAutoStart
```

## 3. 正常写入来源

- 软件安装程序
- 驱动安装程序
- Windows Update
- 企业终端管理软件
- 安全软件

## 4. 高风险变化

```text
新建服务
修改 ImagePath
服务路径指向 Temp、Downloads、Public 或用户目录
服务程序无签名
服务名伪装系统服务
启动类型改为 Auto
驱动服务异常新增
```

## 5. 关联启动方式

- [[Windows Service]]
- [[Driver Service]]

## 6. 关联安全基线

- [[异常服务创建]]
- [[服务ImagePath篡改]]
