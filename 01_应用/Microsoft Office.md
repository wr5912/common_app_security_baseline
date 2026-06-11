---
type: app
app_id: app_microsoft_office
app_name_cn: Microsoft Office
app_name_en: Microsoft Office
vendor: Microsoft Corporation
category: 办公
subcategory: 文档处理
is_system_builtin: false
confidence: medium
status: active
tags:
  - app/office
  - vendor/microsoft
  - windows/app
---

# Microsoft Office

## 1. 基本说明

Microsoft Office 是常见办公套件，包括 Word、Excel、PowerPoint、Outlook 等。安全分析中，Office 进程拉起脚本解释器、下载器、压缩工具、系统工具时需要重点关注。

## 2. 常见相关服务

- [[ClickToRunSvc]]

## 3. 相关进程

- [[winword.exe]]
- `excel.exe`，待建页面
- `powerpnt.exe`，待建页面
- `outlook.exe`，待建页面

## 4. 常见启动方式

- 用户双击文档
- Office Click-to-Run 服务维护和更新
- 邮件附件打开
- 浏览器下载后打开

## 5. 高关注父子进程关系

- [[winword.exe -> powershell.exe]]

## 6. 正常行为画像

- 用户打开文档。
- Office 加载模板、插件、字体、最近文档。
- Office 访问用户文档目录、临时目录、注册表配置。

## 7. 异常关注点

```text
Office 进程拉起 powershell.exe / cmd.exe / wscript.exe / mshta.exe
Office 进程下载远程内容后执行
Office 进程写入 Run Key / 计划任务 / 服务
Office 进程落地可执行文件或脚本
宏启用后出现外联和子进程执行
```

## 8. 关联安全基线

- [[Office拉起脚本解释器]]
