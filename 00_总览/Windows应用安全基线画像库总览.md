---
type: overview
title: Windows应用安全基线画像库总览
status: active
tags:
  - overview
  - windows/app-baseline
---

# Windows应用安全基线画像库总览

本库围绕一个核心链路组织知识：

```text
应用 -> 服务/启动方式 -> 进程 -> 父子关系 -> 文件/注册表/网络行为 -> 安全基线 -> 证据
```

## 核心入口

- [[应用分类索引]]
- [[服务分类索引]]
- [[进程分类索引]]
- [[高风险父子进程关系索引]]
- [[注册表关键位置索引]]
- [[安全基线索引]]
- [[维护工作流]]

## 样例链路

### Chrome 更新链路

```text
[[Google Chrome]]
  -> [[gupdate]] / [[gupdatem]]
  -> [[GoogleUpdate.exe]]
  -> [[services.exe -> GoogleUpdate.exe]]
  -> [[更新器外联行为]]
```

### Office 高风险链路

```text
[[Microsoft Office]]
  -> [[winword.exe]]
  -> [[winword.exe -> powershell.exe]]
  -> [[Office拉起脚本解释器]]
```

### 远控常驻链路

```text
[[AnyDesk]]
  -> [[AnyDesk Service]]
  -> [[AnyDesk.exe]]
  -> [[services.exe -> AnyDesk.exe]]
  -> [[远控软件服务常驻]]
```
