---
type: source_evidence
os: windows
evidence_id: evidence_sysmon_process_spawn_sample
source_type: sysmon_sample
confidence: low
status: example
tags:
  - evidence/sysmon
  - process-spawn
---

# Sysmon样例-父子进程

## 1. 说明

这是一个脱敏样例，用于说明如何记录父子进程证据。真实环境中应保留事件 ID、时间、主机、用户、进程 GUID、命令行等字段。

## 2. 样例

```json
{
  "EventID": 1,
  "UtcTime": "2026-06-11T00:00:00Z",
  "Image": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
  "CommandLine": "powershell.exe -NoProfile -ExecutionPolicy Bypass -EncodedCommand <redacted>",
  "ParentImage": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
  "ParentCommandLine": "\"C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE\" C:\\Users\\user\\Downloads\\invoice.docm",
  "User": "DOMAIN\\user"
}
```

## 3. 关联画像

- [[winword.exe -> powershell.exe]]
- [[Office拉起脚本解释器]]
