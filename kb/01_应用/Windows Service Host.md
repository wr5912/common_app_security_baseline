---
type: app
os: windows
app_id: windows-service-host
app_name_cn: Windows 服务宿主
app_name_en: Windows Service Host
vendor: Microsoft Corporation
category: 系统组件
subcategory: 服务宿主
is_system_builtin: true
confidence: medium
status: active
tags:
  - app/system
  - windows/service-host
---

# Windows Service Host

## 1. 基本说明

Windows Service Host 是承载共享进程模式 Windows 服务的系统组件，常见进程为 `svchost.exe`。

## 2. 相关进程

- [[svchost.exe]]

## 3. 异常关注点

```text
svchost.exe 不在系统目录
命令行缺少合理的 -k 或 -s 参数
承载服务与注册表配置不一致
非 Microsoft 签名或由异常父进程启动
```

## 4. 证据与来源

- 来源类型：系统组件基线
- 可信度：medium
- 待验证：结合服务组、命令行和签名样例补强。
