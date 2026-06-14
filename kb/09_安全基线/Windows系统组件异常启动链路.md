---
type: security_baseline
os: windows
baseline_id: base_windows
object_type: behavior
normality: suspicious
risk_level: high
confidence: medium
status: active
tags:
  - baseline/windows-app-profile
---

# Windows系统组件异常启动链路

<!-- generated: windows-complete-profile-backfill -->

## 1. 基线说明

Windows 系统组件被异常父进程拉起、从异常路径运行或承担与职责不符的外联/持久化行为时，应提高优先级。

## 2. 合法条件

```text
资产、用户、业务角色和变更记录能够解释该行为
路径、签名、服务注册表、父子进程和网络目的地址符合应用画像
行为发生在安装、更新、运维、备份、同步或授权业务窗口内
```

## 3. 异常条件

```text
未授权资产或普通用户终端出现该行为
路径位于用户可写目录、临时目录、下载目录或网络共享
伴随异常登录、服务创建、权限提升、凭据访问、数据打包或异常外联
```

## 4. 推荐处置

按应用完整画像链路核验：应用授权、服务 ImagePath、父子进程、文件落点、注册表变化、网络目的地址和证据记录。

## 5. 关联对象

- [[Windows常见应用完整画像验收清单]]

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
      - image_path
      - command_line
      - user
    child_process_any:
      - svchost.exe
      - rundll32.exe
      - regsvr32.exe
      - powershell.exe
      - cmd.exe
      - wscript.exe
      - mshta.exe
    image_location_any:
      - user_writable_dir
      - temp_dir
      - downloads_dir
      - network_share
  runtime:
    required_evidence:
      - child_processes
      - network_connections
      - file_activity
      - registry_or_config_activity
    risk_escalates_when:
      - unknown_child_process
      - abnormal_external_connection
      - persistence_write
      - credential_access
      - data_archive
  false_positive:
    allowed_contexts:
      - microsoft_signed_component
      - approved_admin_tooling
      - approved_change
```
