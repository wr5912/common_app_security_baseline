---
type: process
os: windows
process_name: winword.exe
app: "[[Microsoft Office]]"
vendor: Microsoft Corporation
role:
  - Office文档进程
risk_level: medium
confidence: medium
status: active
tags:
  - process/office
  - vendor/microsoft
---

# winword.exe

## 1. 进程说明

`winword.exe` 是 Microsoft Word 进程。安全分析中，Word 拉起脚本解释器、下载器、系统工具时需要重点关注。

## 2. 所属应用

- [[Microsoft Office]]

## 3. 常见父进程

- [[explorer.exe]]
- `outlook.exe`，邮件附件打开场景
- 浏览器进程，下载后打开场景

## 4. 常见子进程

正常情况下，Word 不应频繁拉起脚本解释器。

高关注关系：

- [[winword.exe -> powershell.exe]]

## 5. 异常行为

```text
winword.exe -> powershell.exe
winword.exe -> cmd.exe
winword.exe -> wscript.exe
winword.exe -> mshta.exe
winword.exe 写入启动项或服务
winword.exe 下载并执行文件
```

## 6. 关联安全基线

- [[Office拉起脚本解释器]]
