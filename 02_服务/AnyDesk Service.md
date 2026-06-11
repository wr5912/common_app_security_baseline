---
type: service
os: windows
service_name: AnyDesk Service
display_name: AnyDesk Service
app: "[[AnyDesk]]"
vendor: AnyDesk Software GmbH
service_type: Win32OwnProcess
start_type: auto
start_account: LocalSystem
image_name: AnyDesk.exe
risk_level: medium
confidence: medium
status: active
tags:
  - service/remote-control
  - app/remote-control
  - risk/medium
---

# AnyDesk Service

## 1. 服务说明

AnyDesk 安装为服务后，可支持无人值守远程访问和开机自启动。

## 2. 所属应用

- [[AnyDesk]]

## 3. 常见进程

- [[AnyDesk.exe]]

## 4. 常见父进程

- [[services.exe]]

## 5. 常见父子关系

- [[services.exe -> AnyDesk.exe]]

## 6. 正常行为

- 后台常驻。
- 连接远控基础设施。
- 支持远程桌面控制。

## 7. 异常关注点

```text
非授权终端存在 AnyDesk 服务
短时间内安装并外联
从临时目录或用户下载目录运行
被脚本静默安装
与横向移动、数据打包、凭据访问同时出现
```

## 8. 关联安全基线

- [[远控软件服务常驻]]
