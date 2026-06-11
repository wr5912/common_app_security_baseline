---
type: app
app_id: app_anydesk
app_name_cn: AnyDesk
app_name_en: AnyDesk
vendor: AnyDesk Software GmbH
category: 远控
subcategory: 远程控制
is_system_builtin: false
confidence: medium
status: active
tags:
  - app/remote-control
  - vendor/anydesk
  - windows/app
---

# AnyDesk

## 1. 基本说明

AnyDesk 是常见远程控制软件，可用于远程桌面、无人值守访问、远程运维。安全分析中，远控软件既可能是合法运维工具，也可能被攻击者滥用。

## 2. 相关服务

- [[AnyDesk Service]]

## 3. 相关进程

- [[AnyDesk.exe]]

## 4. 常见启动方式

- 用户手动启动
- Windows 服务常驻
- 安装后开机自启

## 5. 常见父子进程关系

- [[services.exe -> AnyDesk.exe]]

## 6. 正常行为画像

- 监听或主动连接远程控制基础设施。
- 访问屏幕、键盘、鼠标、剪贴板。
- 写入配置文件和连接日志。
- 作为服务运行以支持无人值守连接。

## 7. 异常关注点

```text
非 IT 管理终端出现 AnyDesk 服务常驻
AnyDesk 从临时目录运行
短时间内新安装并外联
伴随账户创建、权限提升、文件打包、数据外传
被脚本或攻击工具静默安装
```

## 8. 关联安全基线

- [[远控软件服务常驻]]
