---
type: process
process_name: GoogleUpdate.exe
app: "[[Google Chrome]]"
vendor: Google LLC
role:
  - 更新器
risk_level: low
confidence: medium
status: active
tags:
  - process/updater
  - vendor/google
---

# GoogleUpdate.exe

## 1. 进程说明

`GoogleUpdate.exe` 是 Google 软件更新相关进程，常由 Google 更新服务或计划任务启动。

## 2. 所属应用

- [[Google Chrome]]

## 3. 常见父进程

- [[services.exe]]

## 4. 常见服务

- [[gupdate]]
- [[gupdatem]]

## 5. 常见启动参数

```text
/svc
/medsvc
/c
```

## 6. 常见父子关系

- [[services.exe -> GoogleUpdate.exe]]

## 7. 异常关注点

```text
路径不在 Google Update 目录
签名不是 Google LLC
由异常父进程启动
访问非预期域名
参数异常或带脚本执行参数
```
