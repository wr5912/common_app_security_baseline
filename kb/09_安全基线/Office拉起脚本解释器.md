---
type: security_baseline
os: windows
baseline_id: base_office_spawn_script
object_type: process_relation
normality: rare
risk_level: high
confidence: medium
status: active
tags:
  - baseline/office
  - baseline/script-execution
  - risk/high
---

# Office拉起脚本解释器

## 1. 基线说明

Office 进程拉起脚本解释器是高关注行为，常见于宏攻击、恶意文档、下载器，也可能出现在企业自动化插件中。

## 2. 关联关系

- [[winword.exe -> powershell.exe]]
- [[winword.exe -> cmd.exe]]

## 3. 高风险子进程

```text
powershell.exe
cmd.exe
wscript.exe
cscript.exe
mshta.exe
rundll32.exe
regsvr32.exe
```

## 4. 高风险参数

```text
-EncodedCommand
-ExecutionPolicy Bypass
-NoProfile
-WindowStyle Hidden
IEX
DownloadString
FromBase64String
```

## 5. 误报条件

```text
企业签名宏
内部办公插件
固定自动化模板
无外联、无落地、命令固定
```

## 6. 证据需求

```text
Office 文档来源
宏启用状态
完整命令行
网络连接
落地文件
注册表/服务/计划任务写入
用户交互
```

## 7. 推荐处置

默认进入疑似/高危核验队列，结合证据提升或降级。
