---
type: app
app_id: app_microsoft_edge
app_name_cn: Microsoft Edge
app_name_en: Microsoft Edge
vendor: Microsoft Corporation
category: 浏览器
subcategory: Chromium浏览器
is_system_builtin: true
confidence: medium
status: active
tags:
  - app/browser
  - vendor/microsoft
  - windows/app
---

# Microsoft Edge

## 1. 基本说明

Microsoft Edge 是 Windows 10/11 常见内置浏览器，基于 Chromium，包含浏览器主进程、更新服务、提权服务等组件。

## 2. 常见安装路径

```text
C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
C:\Program Files\Microsoft\Edge\Application\msedge.exe
```

## 3. 相关服务

- [[edgeupdate]]

## 4. 相关进程

- `msedge.exe`，待建页面

## 5. 常见父子进程关系

- `explorer.exe -> msedge.exe`
- `msedge.exe -> msedge.exe`

## 6. 正常行为画像

- 浏览网页。
- 多进程运行。
- 自动更新。
- 访问用户 Profile、缓存、Cookie、扩展目录。

## 7. 异常关注点

```text
msedge.exe 拉起脚本解释器
msedge.exe 从用户临时目录启动
更新服务路径或签名异常
浏览器扩展加载异常
```

## 8. 关联安全基线

- [[浏览器拉起脚本解释器]]
- [[更新器外联行为]]
