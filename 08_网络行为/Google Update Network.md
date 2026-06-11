---
type: network_behavior
os: windows
app: "[[Google Chrome]]"
process: "[[GoogleUpdate.exe]]"
protocol:
  - HTTPS
  - HTTP
purpose: update
risk_level: low
confidence: low
status: needs_review
tags:
  - network/update
  - vendor/google
---

# Google Update Network

## 1. 行为说明

Google 更新器通常会访问 Google 更新相关服务，用于检查版本和下载更新包。

## 2. 相关进程

- [[GoogleUpdate.exe]]

## 3. 相关服务

- [[gupdate]]
- [[gupdatem]]

## 4. 常见用途

```text
检查更新
下载更新包
上报更新状态
```

## 5. 异常关注点

```text
GoogleUpdate.exe 访问非预期域名
明文下载可执行文件
更新器路径或签名异常
更新后落地未知可执行文件
```

## 6. 待验证项

具体域名和 URL 模式应从企业代理、EDR、DNS 日志中补充，不建议无来源填充精确域名。
