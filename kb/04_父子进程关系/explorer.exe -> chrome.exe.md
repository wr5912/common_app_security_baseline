---
type: process_relation
os: windows
parent_process: "[[explorer.exe]]"
child_process: "[[chrome.exe]]"
relation: user_launch
normality: normal
risk_level: low
confidence: medium
status: active
tags:
  - relation/user-launch
  - browser
---

# explorer.exe -> chrome.exe

## 1. 关系说明

`explorer.exe` 拉起 `chrome.exe` 通常表示用户通过桌面、开始菜单、快捷方式或文件关联启动浏览器。

## 2. 正常条件

```text
chrome.exe 路径位于 Google 官方安装目录
签名正常
命令行参数符合浏览器启动场景
存在用户交互上下文
```

## 3. 异常条件

```text
chrome.exe 位于临时目录、下载目录或公共目录
签名异常
命令行包含异常代理、扩展或调试参数
启动后立即拉起脚本解释器
```

## 4. 关联画像

- [[Google Chrome]]
- [[chrome.exe]]
