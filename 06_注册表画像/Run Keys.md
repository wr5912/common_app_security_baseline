---
type: registry_pattern
hive: HKLM/HKCU
key_pattern: Software\Microsoft\Windows\CurrentVersion\Run*
purpose:
  - autostart
risk_level: high
confidence: high
tags:
  - registry/run-key
  - persistence
---

# Run Keys

## 1. 注册表用途

Run Key 用于用户登录时自动启动程序。

## 2. 常见位置

```text
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
HKLM\Software\Microsoft\Windows\CurrentVersion\Run
HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

## 3. 正常写入来源

- 输入法
- 云盘
- IM 工具
- 驱动辅助程序
- 安全软件托盘程序
- 更新器

## 4. 异常关注点

```text
值名伪装系统组件
路径位于 Temp/Downloads/Public/AppData 随机目录
命令行启动 powershell/cmd/wscript/mshta
无签名可执行文件
短时间内伴随外联、提权、文件落地
```

## 5. 关联启动方式

- [[Run Key]]
