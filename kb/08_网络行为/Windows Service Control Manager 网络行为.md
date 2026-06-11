---
type: network_behavior
os: windows
app: "[[Windows Service Control Manager]]"
process: "[[services.exe]]"
protocol: [tcp, udp, rpc, dns]
purpose: "系统管理、用户交互、服务承载或组件网络访问"
risk_level: medium
confidence: medium
status: active
tags:
  - network/windows-app-profile
---

# Windows Service Control Manager 网络行为

<!-- generated: windows-complete-profile-backfill -->

## 1. 行为说明

本页描述 [[Windows Service Control Manager]] 的常见网络行为模式。精确域名和网关必须来自官方文档、企业资产台账、代理日志、EDR/Sysmon 或流量观测，不在无来源情况下硬编码。

## 2. 相关进程

- [[services.exe]]

## 3. 常见端口

```text
tcp/135
dynamic-rpc
```

## 4. 常见目标

```text
厂商云服务、企业管理端、授权服务器、更新源、业务数据库或内网网关。
不要无来源填充精确域名、IP、账号或租户标识。
```

## 5. 正常用途

目的地址与企业授权、厂商服务或业务系统一致，路径、签名和启动账户可信。

## 6. 异常关注点

```text
系统组件从异常路径启动、由异常父进程拉起或产生与职责不符的外联。
进程路径、签名、父进程、启动账户或服务 ImagePath 与应用画像不一致
网络连接出现在未授权资产、异常时间窗口或异常登录之后
```

## 7. 关联对象

- [[Windows Service Control Manager]]
- [[应用异常网络外联行为]]
- [[Windows常见应用完整画像验收清单]]
