---
type: app
os: windows
app_id: app_postgresql
app_name_cn: "PostgreSQL"
app_name_en: "PostgreSQL"
vendor: "PostgreSQL Global Development Group"
category: "数据库 / 中间件 / 开发服务"
subcategory: "数据库"
is_system_builtin: false
confidence: low
status: needs_review
tags:
  - windows/app
  - app/数据库
---

# PostgreSQL

## 1. 基本说明

PostgreSQL 属于 `数据库 / 中间件 / 开发服务` 场景应用。当前画像依据 `/tmp/windows系统上常见应用.md` 中的常见服务基线清单建立，用于终端服务、进程和资产角色识别；具体路径、签名和版本差异需要结合企业终端观测确认。

## 2. 常见安装路径

```text
C:\Program Files\PostgreSQL\*\bin\postgres.exe
```

## 3. 相关服务

- [[postgresql-x64 服务模式]]

## 4. 相关进程

- [[postgres.exe]]

## 5. 常见启动方式

- [[Windows Service]]
- 用户交互启动或软件自启动，具体取决于安装方式和企业策略。

## 6. 常见父子进程关系

- 服务常驻组件通常由 [[services.exe]] 启动。
- 用户交互组件通常由 [[explorer.exe]]、软件更新器或主程序拉起。

## 7. 常见文件与数据

- 安装目录、服务配置、日志、缓存和用户配置文件。
- 具体路径随版本、安装范围和企业定制包变化。

## 8. 常见注册表信息

- [[HKLM_SYSTEM_CurrentControlSet_Services]]
- [[Uninstall Registry]]

## 9. 常见网络行为

- 更新、授权、管理端通信或业务连接，需按资产角色和目的地址白名单判断。

## 10. 正常行为画像

数据库服务器或开发环境运行 PostgreSQL 服务。

## 11. 异常关注点

```text
非授权主机出现 PostgreSQL 服务
服务账户或数据目录异常
监听范围超过业务需要
```

## 12. 关联安全基线

- [[数据库中间件服务常驻]]

## 13. 证据与来源

- 来源类型：场景清单 / 待企业终端观测补强
- 来源页面：[[Windows常见应用服务基线清单]]
- 可信度：low
- 待验证：服务名、ImagePath、签名厂商、启动账户、网络目的地址和企业授权状态。
