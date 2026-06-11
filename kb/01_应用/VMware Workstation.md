---
type: app
os: windows
app_id: app_vmware_workstation
app_name_cn: "VMware Workstation"
app_name_en: "VMware Workstation"
vendor: "VMware"
category: "虚拟化 / 容器 / 开发环境"
subcategory: "虚拟机"
is_system_builtin: false
confidence: low
status: needs_review
tags:
  - windows/app
  - app/虚拟化
---

# VMware Workstation

## 1. 基本说明

VMware Workstation 属于 `虚拟化 / 容器 / 开发环境` 场景应用。当前画像依据 `/tmp/windows系统上常见应用.md` 中的常见服务基线清单建立，用于终端服务、进程和资产角色识别；具体路径、签名和版本差异需要结合企业终端观测确认。

## 2. 常见安装路径

```text
C:\Program Files (x86)\VMware\VMware Workstation\vmware-authd.exe
C:\Windows\SysWOW64\vmnat.exe
```

## 3. 相关服务

- [[VMAuthdService]]
- [[VMnetDHCP]]
- [[VMware NAT Service]]
- [[VMUSBArbService]]

## 4. 相关进程

- [[vmware-authd.exe]]
- [[vmnat.exe]]

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

开发或测试主机运行虚拟机网络、NAT、USB 透传等服务。

## 11. 异常关注点

```text
普通办公终端出现未授权虚拟化服务
VMware 网络服务创建异常端口转发或未知虚拟网段
```

## 12. 关联安全基线

- [[虚拟化与开发服务常驻]]

## 13. 证据与来源

- 来源类型：场景清单 / 待企业终端观测补强
- 来源页面：[[Windows常见应用服务基线清单]]
- 可信度：low
- 待验证：服务名、ImagePath、签名厂商、启动账户、网络目的地址和企业授权状态。
