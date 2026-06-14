---
type: security_baseline
os: windows
baseline_id: base_service_imagepath_tamper
object_type: registry/service
normality: suspicious
risk_level: high
confidence: medium
status: active
tags:
  - baseline/service
  - registry
  - persistence
  - risk/high
---

# 服务ImagePath篡改

## 1. 基线说明

服务 `ImagePath` 决定服务启动的可执行文件和参数。篡改 ImagePath 可导致合法服务启动恶意程序。

## 2. 关联对象

- [[Windows Service]]
- [[HKLM_SYSTEM_CurrentControlSet_Services]]

## 3. 高风险变化

```text
ImagePath 从系统目录变为用户目录
ImagePath 增加脚本解释器
ImagePath 指向无签名程序
ImagePath 参数被追加异常命令
```

## 4. 推荐处置

对比历史配置，关联修改进程、修改账户、服务重启事件和后续行为。

## 5. 结构化生命周期规则

```yaml
lifecycle_baseline:
  version: 1
  applies_to: security_baseline
  phase: lifecycle
  creation:
    required_evidence:
      - service_name
      - registry_activity
      - image_path
      - command_line
      - user
    image_location_any:
      - user_writable_dir
      - temp_dir
      - downloads_dir
      - network_share
    command_line_contains_any:
      - ImagePath
      - CurrentControlSet\\Services
      - powershell.exe
      - cmd.exe
      - wscript.exe
      - mshta.exe
  runtime:
    required_evidence:
      - service_state_change
      - child_processes
      - network_connections
      - file_activity
    risk_escalates_when:
      - persistence_change
      - network_after_spawn
      - file_drop_after_spawn
      - unknown_child_process
  false_positive:
    allowed_contexts:
      - approved_service_repair
      - approved_software_upgrade
      - endpoint_management_deployment
```
