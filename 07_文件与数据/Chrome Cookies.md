---
type: file_artifact
os: windows
artifact_name: Chrome Cookies
app: "[[Google Chrome]]"
artifact_type: sqlite_db
sensitivity: high
confidence: medium
tags:
  - artifact/browser-cookies
  - data/credential-like
---

# Chrome Cookies

## 1. 数据说明

Chrome Cookies 保存网站 Cookie，可能包含会话相关数据，敏感性高。

## 2. 常见路径

```text
%LOCALAPPDATA%\Google\Chrome\User Data\Default\Network\Cookies
```

## 3. 安全关注点

```text
非浏览器进程读取 Cookies
Cookie 数据被打包或外传
与凭据窃取行为同时出现
```
