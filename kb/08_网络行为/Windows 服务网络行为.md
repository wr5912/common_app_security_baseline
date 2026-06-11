---
type: network_behavior
os: windows
confidence: medium
status: active
tags:
  - generated/windows-source-full-coverage
---

# Windows 服务网络行为

<!-- generated: windows-source-full-coverage -->

## 1. 行为说明

Windows 服务的网络行为必须结合具体服务职责判断；精确目标需要企业观测补充。

## 2. 异常关注点

```text
系统服务或第三方服务连接未知目的地址
网络连接与异常服务创建、ImagePath 修改、登录或权限提升接近
```
