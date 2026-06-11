---
type: startup_method
name: Run Key
risk_level: high
confidence: medium
tags:
  - startup/run-key
  - registry
  - persistence
---

# Run Key

## 1. 启动方式说明

Run Key 是常见用户登录自启动位置，既用于正常软件开机启动，也常用于持久化。

## 2. 关联注册表

- [[Run Keys]]

## 3. 异常关注点

```text
指向 Temp/Downloads/Public/AppData 随机目录
启动脚本解释器
命令行混淆
名称伪装系统组件
```
