---
type: security_baseline
os: windows
baseline_id: base_windows_imagepath
object_type: service_behavior
normality: suspicious
risk_level: medium
confidence: medium
status: active
tags:
  - baseline/windows-source-full-coverage
---

# Windows服务ImagePath异常

<!-- generated: windows-source-full-coverage -->

## 1. 基线说明

本基线用于全量来源覆盖中的类别级异常判断，避免为缺少精确观测的来源行编造域名、IP、hash 或 ImagePath。

## 2. 异常条件

```text
服务路径、签名、启动账户、父子进程、文件落点、注册表变化或网络目的地址与画像不一致
行为出现在未授权资产、异常登录、服务创建、权限提升或数据访问事件附近
```

## 3. 证据需求

```text
服务注册表、进程命令行、文件签名、网络连接、EDR/Sysmon 时间线、资产授权和变更记录
```

## 4. 关联对象

- [[Windows常见应用全量覆盖清单]]

## 5. 结构化生命周期规则

```yaml
lifecycle_baseline:
  version: 1
  applies_to: security_baseline
  phase: lifecycle
  creation:
    required_evidence:
      - service_name
      - image_path
      - command_line
      - user
      - registry_activity
    image_location_any:
      - user_writable_dir
      - temp_dir
      - downloads_dir
      - network_share
    command_line_contains_any:
      - powershell.exe
      - cmd.exe
      - wscript.exe
      - mshta.exe
      - rundll32.exe
  runtime:
    required_evidence:
      - service_state_change
      - child_processes
      - network_connections
      - file_activity
    risk_escalates_when:
      - service_creation
      - network_after_spawn
      - file_drop_after_spawn
      - persistence_after_spawn
  false_positive:
    allowed_contexts:
      - approved_software_install
      - approved_service_upgrade
      - endpoint_management_deployment
```
