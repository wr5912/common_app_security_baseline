---
type: process_relation
parent_process: "[[services.exe]]"
child_process: "[[GoogleUpdate.exe]]"
relation: service_start
normality: normal
risk_level: low
confidence: medium
status: active
tags:
  - relation/service-start
  - service/update
  - vendor/google
---

# services.exe -> GoogleUpdate.exe

## 1. 关系说明

`services.exe` 启动 `GoogleUpdate.exe` 通常对应 Google 更新服务，例如 [[gupdate]] 或 [[gupdatem]]。

## 2. 父进程

- [[services.exe]]

## 3. 子进程

- [[GoogleUpdate.exe]]

## 4. 正常条件

```text
服务名为 gupdate 或 gupdatem
路径位于 Google Update 常见目录
签名为 Google LLC
参数为 /svc 或 /medsvc
启动账户为 LocalSystem
```

## 5. 异常条件

```text
路径异常
签名异常
参数异常
服务 ImagePath 被篡改
访问非预期域名
```

## 6. 关联画像

- [[Google Chrome]]
- [[gupdate]]
- [[gupdatem]]
- [[GoogleUpdate.exe]]
- [[更新器外联行为]]
