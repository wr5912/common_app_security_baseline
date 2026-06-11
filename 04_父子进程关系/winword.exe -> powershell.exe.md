---
type: process_relation
parent_process: "[[winword.exe]]"
child_process: "[[powershell.exe]]"
relation: spawn
normality: rare
risk_level: high
attack_techniques:
  - T1059
  - T1204
confidence: medium
status: active
tags:
  - relation/process-spawn
  - risk/high
  - office
  - powershell
---

# winword.exe -> powershell.exe

## 1. 关系说明

`winword.exe` 拉起 `powershell.exe` 在普通办公场景中并不常见。它可能来自企业宏、办公插件或自动化流程，也可能是恶意文档攻击链。

## 2. 父进程

- [[winword.exe]]

## 3. 子进程

- [[powershell.exe]]

## 4. 可能正常场景

```text
企业签名宏
内部办公插件
文档自动化模板
IT 管理脚本
```

## 5. 高风险场景

```text
钓鱼文档
宏下载器
混淆 PowerShell
隐藏窗口执行
下载并执行远程脚本
落地可执行文件
```

## 6. 高风险参数

```text
-EncodedCommand
-ExecutionPolicy Bypass
-NoProfile
-WindowStyle Hidden
-IEX
DownloadString
FromBase64String
```

## 7. 需要补充的证据

```text
Word 文档来源
是否启用宏
PowerShell 完整命令行
是否外联
是否落地文件
是否创建服务/计划任务/Run Key
用户是否主动打开文档
```

## 8. 检测建议

```text
父进程为 winword.exe
子进程为 powershell.exe/cmd.exe/wscript.exe/mshta.exe
且命令行包含高风险参数
或随后发生网络连接/文件落地/持久化写入
```

## 9. 误报条件

```text
签名宏
固定办公插件
已知自动化模板
命令行固定且无外联
```

## 10. 推荐处置

默认进入疑似或高危队列，关联文档来源、网络行为、文件落地、注册表持久化证据后再定性。

## 11. 关联画像

- [[Microsoft Office]]
- [[Office拉起脚本解释器]]
