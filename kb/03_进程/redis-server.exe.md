---
type: process
os: windows
process_name: "redis-server.exe"
app: "[[Redis for Windows]]"
vendor: "Redis / Microsoft Open Tech legacy"
role:
  - "Redis 服务进程"
risk_level: medium
confidence: low
status: needs_review
tags:
  - windows/process
  - process/scenario-baseline
---

# redis-server.exe

## 1. 进程说明

`redis-server.exe` 是 [[Redis for Windows]] 相关进程，常见角色为：Redis 服务进程。当前画像用于终端基线识别，具体路径、签名和命令行参数需要结合真实观测校验。

## 2. 所属应用

- [[Redis for Windows]]

## 3. 常见路径

```text
C:\Program Files\Redis\redis-server.exe
```

## 4. 常见父进程

- [[services.exe]]
- [[explorer.exe]]

## 5. 常见子进程

- 同应用组件、更新器、浏览器子进程或网络隧道组件，取决于应用类型。

## 6. 常见启动参数

```text
未统一；以终端命令行观测为准。
```

## 7. 参数安全关注

- 异常代理、脚本执行、隐藏窗口、临时目录执行、非预期配置文件路径。

## 8. 常见文件行为

- 读取安装目录、配置目录、日志目录和用户数据目录。

## 9. 常见注册表行为

- 读取卸载信息、服务注册项、自动启动项或应用配置项。

## 10. 常见网络行为

- 与更新、管理端、远控、VPN、日志转发或业务服务目的地址通信。

## 11. 异常行为

```text
从非标准路径运行
签名厂商异常
由 Office、浏览器、脚本解释器等异常父进程启动
连接未知公网管理端或代理节点
短时间内伴随服务创建、凭据访问或数据打包
```

## 12. 关联安全基线

- [[数据库中间件服务常驻]]

## 13. 相关服务

- [[Redis 服务模式]]
