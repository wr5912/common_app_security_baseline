---
type: service
service_name: gupdatem
display_name: Google Update Service Machine
app: "[[Google Chrome]]"
vendor: Google LLC
service_type: Win32OwnProcess
start_type: manual
start_account: LocalSystem
image_name: GoogleUpdate.exe
risk_level: low
confidence: medium
status: active
tags:
  - service/update
  - vendor/google
  - windows/service
---

# gupdatem

## 1. 服务说明

`gupdatem` 通常是 Google Update 的 machine-level 服务，常用于按需更新。

## 2. 所属应用

- [[Google Chrome]]

## 3. 常见 ImagePath

```text
"C:\Program Files (x86)\Google\Update\GoogleUpdate.exe" /medsvc
```

## 4. 常见启动参数

```text
/medsvc
```

## 5. 常见父进程

- [[services.exe]]

## 6. 常见进程

- [[GoogleUpdate.exe]]

## 7. 异常关注点

```text
路径异常
签名异常
参数异常
更新器访问异常域名
```

## 8. 关联关系

- [[services.exe -> GoogleUpdate.exe]]
- [[更新器外联行为]]
