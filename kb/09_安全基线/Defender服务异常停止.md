---
type: security_baseline
os: windows
baseline_id: base_defender_service_stopped
object_type: service
normality: suspicious
risk_level: high
confidence: medium
status: active
tags:
  - baseline/security-product
  - defender
  - risk/high
---

# Defender服务异常停止

## 1. 基线说明

Microsoft Defender 相关服务异常停止或配置被篡改，可能是正常策略调整，也可能是攻击链中的防御规避步骤。

## 2. 关联对象

- [[Microsoft Defender]]
- [[WinDefend]]
- [[Sense]]
- [[MsMpEng.exe]]

## 3. 高风险条件

```text
服务被停止或禁用
实时防护被关闭
增加异常排除路径
攻击链中存在关闭安全产品命令
随后出现下载、执行、持久化、横向移动
```

## 4. 误报条件

```text
企业安全策略切换
第三方杀毒接管
维护窗口内管理员操作
```

## 5. 证据需求

```text
操作账户
执行进程
命令行
策略来源
变更时间
后续行为链
```

## 6. 结构化生命周期规则

```yaml
lifecycle_baseline:
  version: 1
  applies_to: security_baseline
  phase: lifecycle
  creation:
    required_evidence:
      - parent_process
      - child_process
      - command_line
      - user
      - service_name
    child_process_any:
      - sc.exe
      - powershell.exe
      - cmd.exe
      - reg.exe
      - MpCmdRun.exe
    command_line_contains_any:
      - WinDefend
      - Sense
      - Set-MpPreference
      - DisableRealtimeMonitoring
      - Add-MpPreference
      - sc stop
      - sc config
  runtime:
    required_evidence:
      - service_state_change
      - registry_or_config_activity
      - process_events
      - network_connections
    risk_escalates_when:
      - downloaded_file
      - persistence_change
      - lateral_movement
      - abnormal_external_connection
  false_positive:
    allowed_contexts:
      - approved_security_policy_change
      - third_party_av_takeover
      - maintenance_window_admin_operation
```
