---
type: file_artifact
os: windows
artifact_name: Chrome User Data
app: "[[Google Chrome]]"
artifact_type: profile_directory
sensitivity: high
confidence: medium
tags:
  - artifact/browser-profile
  - data/sensitive
---

# Chrome User Data

## 1. 数据说明

Chrome User Data 是 Chrome 用户配置、缓存、历史、Cookie、扩展等数据所在目录。

## 2. 常见路径

```text
%LOCALAPPDATA%\Google\Chrome\User Data\
```

## 3. 相关数据

- [[Chrome History]]
- [[Chrome Cookies]]

## 4. 安全关注点

```text
恶意进程读取浏览器 Profile
异常进程访问 Cookies / Login Data
浏览器以异常 --user-data-dir 指向其他目录
```
