---
type: app
os: windows
app_id: app_mozilla_firefox
app_name_cn: "Firefox 浏览器"
app_name_en: "Mozilla Firefox"
vendor: "Mozilla"
category: "浏览器"
subcategory: "Firefox"
is_system_builtin: false
confidence: low
status: needs_review
tags:
  - windows/app
  - app/浏览器
---

# Mozilla Firefox

## 1. 基本说明

Mozilla Firefox 属于 `浏览器` 场景应用。当前画像依据 `/tmp/windows系统上常见应用.md` 中的常见服务基线清单建立，用于终端服务、进程和资产角色识别；具体路径、签名和版本差异需要结合企业终端观测确认。

## 2. 常见安装路径

```text
C:\Program Files\Mozilla Firefox\firefox.exe
C:\Program Files\Mozilla Maintenance Service\maintenanceservice.exe
```

## 3. 相关服务

- [[MozillaMaintenance]]

## 4. 相关进程

- [[firefox.exe]]
- [[maintenanceservice.exe]]

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

用户启动浏览器访问 Web；维护服务用于浏览器更新和组件维护。

## 11. 异常关注点

```text
firefox.exe 从临时目录或下载目录运行
maintenanceservice.exe 路径或签名异常
浏览器拉起脚本解释器或异常代理参数
```

## 12. 关联安全基线

- [[更新器外联行为]]

## 13. 证据与来源

- 来源类型：场景清单 / 待企业终端观测补强
- 来源页面：[[Windows常见应用服务基线清单]]
- 可信度：low
- 待验证：服务名、ImagePath、签名厂商、启动账户、网络目的地址和企业授权状态。
