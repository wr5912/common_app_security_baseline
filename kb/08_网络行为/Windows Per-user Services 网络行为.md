---
type: network_behavior
os: windows
confidence: medium
status: active
tags:
  - generated/windows-source-full-coverage
source_row_ids:
  - win-per-user-001
  - win-per-user-002
  - win-per-user-003
  - win-per-user-004
  - win-per-user-005
  - win-per-user-006
  - win-per-user-007
  - win-per-user-008
  - win-per-user-009
  - win-per-user-010
  - win-per-user-011
  - win-per-user-012
  - win-per-user-013
  - win-per-user-014
  - win-per-user-015
  - win-per-user-016
  - win-per-user-017
  - win-per-user-018
  - win-per-user-019
  - win-per-user-020
  - win-per-user-021
  - win-per-user-022
  - win-per-user-023
  - win-per-user-024
---
# Windows Per-user Services 网络行为

<!-- generated: windows-source-full-coverage -->

## 1. 行为说明

[[Windows Per-user Services]] 的更新、授权、管理面、遥测、同步或业务连接模式。精确域名和 IP 必须来自官方文档或企业观测。

## 2. 相关进程

- [[svchost.exe]]

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
