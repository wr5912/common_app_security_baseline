---
type: app
os: windows
app_id: app_google_chrome
app_name_cn: 谷歌浏览器
app_name_en: Google Chrome
vendor: Google LLC
category: 浏览器
subcategory: Chromium浏览器
is_system_builtin: false
confidence: medium
status: active
tags:
  - app/browser
  - vendor/google
  - windows/app
---

# Google Chrome

## 1. 基本说明

Google Chrome 是 Windows 上常见浏览器，主要用于网页访问、扩展运行、文件下载、账号同步、自动更新等。

## 2. 常见安装路径

```text
C:\Program Files\Google\Chrome\Application\chrome.exe
C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe
```

## 3. 相关服务

- [[gupdate]]
- [[gupdatem]]

## 4. 相关进程

- [[chrome.exe]]
- [[GoogleUpdate.exe]]

## 5. 常见启动方式

- [[Windows Service]]
- [[Scheduled Task]]
- 用户手动启动
- 浏览器协议唤起

## 6. 常见父子进程关系

- [[explorer.exe -> chrome.exe]]
- [[services.exe -> GoogleUpdate.exe]]
- [[chrome.exe -> powershell.exe]]，少见，高关注

## 7. 常见文件与数据

- [[Chrome User Data]]
- [[Chrome History]]
- [[Chrome Cookies]]

## 8. 常见注册表信息

- [[Run Keys]]
- [[Uninstall Registry]]

## 9. 常见网络行为

- [[Google Update Network]]
- [[Chrome Web Browsing Network]]

## 10. 正常行为画像

- 用户通过 `explorer.exe` 或快捷方式启动 `chrome.exe`。
- 浏览器使用多进程架构，一个 `chrome.exe` 会拉起多个 `chrome.exe` 子进程。
- 浏览器访问 HTTP/HTTPS/QUIC 网络。
- 浏览器写入用户 Profile、缓存、Cookie、历史记录。
- Google 更新器周期性检查和下载更新。

## 11. 异常关注点

```text
chrome.exe 从 Temp、Downloads、Public 等异常目录启动
chrome.exe 拉起 powershell.exe / cmd.exe / wscript.exe / mshta.exe
chrome.exe 使用异常 --proxy-server 或 --load-extension 参数
GoogleUpdate.exe 路径、签名、参数异常
更新器访问非预期域名
```

## 12. 关联安全基线

- [[浏览器拉起脚本解释器]]
- [[更新器外联行为]]

## 13. 证据与来源

- 来源类型：通用经验 / 待企业环境观测验证
- 可信度：medium
