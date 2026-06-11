---
type: process_relation
os: windows
parent_process: "[[services.exe]]"
child_process: "[[AnyDesk.exe]]"
relation: service_start
normality: rare
risk_level: medium
confidence: medium
status: active
tags:
  - relation/service-start
  - app/remote-control
  - risk/medium
---

# services.exe -> AnyDesk.exe

## 1. 关系说明

`services.exe` 启动 `AnyDesk.exe` 表示 AnyDesk 可能以服务方式常驻，支持无人值守远程访问。

## 2. 正常条件

```text
IT 运维授权安装
路径位于 AnyDesk 正常安装目录
签名正常
资产台账中登记为远控工具
```

## 3. 异常条件

```text
普通办公终端首次出现
从用户目录或临时目录运行
短时间内安装并外联
伴随异常登录、数据打包、凭据访问、横向移动
```

## 4. 推荐处置

结合资产授权、用户确认、安装时间线、网络连接、同主机其他行为综合判断。

## 5. 关联画像

- [[AnyDesk]]
- [[AnyDesk Service]]
- [[AnyDesk.exe]]
- [[远控软件服务常驻]]
