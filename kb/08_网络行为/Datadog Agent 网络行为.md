---
type: network_behavior
os: windows
confidence: medium
status: active
tags:
  - generated/windows-source-full-coverage
source_row_ids:
  - third-party-edr-025
---
# Datadog Agent 网络行为

<!-- generated: windows-source-full-coverage -->

## 1. 行为说明

[[Datadog Agent]] 的更新、授权、管理面、遥测、同步或业务连接模式。精确域名和 IP 必须来自官方文档或企业观测。

## 2. 相关进程

- [[DatadogAgent.exe]]

## 3. 常见端口

```text
tcp/443
tcp/80
udp/53
按应用类别补充业务端口
```

## 4. 异常关注点

```text
未授权资产外联未知目的地址
服务进程路径、签名、启动账户或父进程不符合画像
连接发生在异常登录、服务创建或文件落地之后
```
