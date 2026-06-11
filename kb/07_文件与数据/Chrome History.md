---
type: file_artifact
os: windows
artifact_name: Chrome History
app: "[[Google Chrome]]"
artifact_type: sqlite_db
sensitivity: high
confidence: medium
tags:
  - artifact/browser-history
  - data/privacy
---

# Chrome History

## 1. 数据说明

Chrome History 通常保存浏览历史、访问时间、页面标题等信息，具有取证和隐私价值。

## 2. 常见路径

```text
%LOCALAPPDATA%\Google\Chrome\User Data\Default\History
```

## 3. 安全关注点

```text
非浏览器进程读取历史数据库
攻击链中读取浏览历史辅助钓鱼或侦察
```
