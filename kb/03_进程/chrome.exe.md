---
type: process
os: windows
process_name: chrome.exe
app: "[[Google Chrome]]"
vendor: Google LLC
role:
  - 主进程
  - 渲染进程
  - GPU进程
  - 网络进程
risk_level: medium
confidence: medium
status: active
tags:
  - process/browser
  - process/multiprocess
  - vendor/google
---

# chrome.exe

## 1. 进程说明

`chrome.exe` 是 Google Chrome 的主进程和子进程名称。不同角色通常通过命令行参数区分。

## 2. 所属应用

- [[Google Chrome]]

## 3. 常见路径

```text
C:\Program Files\Google\Chrome\Application\chrome.exe
C:\Program Files (x86)\Google\Chrome\Application\chrome.exe
%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe
```

## 4. 常见父进程

- [[explorer.exe]]
- [[chrome.exe]]

## 5. 常见子进程

- [[chrome.exe]]
- `crashpad_handler.exe`，待建页面

## 6. 常见启动参数

```text
--type=renderer
--type=gpu-process
--type=utility
--type=crashpad-handler
--profile-directory=
--user-data-dir=
--disable-features=
--load-extension=
--proxy-server=
```

## 7. 参数安全关注

| 参数 | 常见含义 | 关注点 |
|---|---|---|
| `--type=renderer` | 渲染进程 | 正常 |
| `--type=gpu-process` | GPU 进程 | 正常 |
| `--user-data-dir=` | 指定用户数据目录 | 指向异常目录需关注 |
| `--load-extension=` | 加载扩展 | 可能加载恶意扩展 |
| `--proxy-server=` | 指定代理 | 异常代理需关注 |

## 8. 异常行为

```text
chrome.exe -> powershell.exe
chrome.exe -> cmd.exe
chrome.exe 从 Temp / Downloads / Public 目录启动
chrome.exe 使用异常代理或异常扩展目录
```

## 9. 关联安全基线

- [[浏览器拉起脚本解释器]]
