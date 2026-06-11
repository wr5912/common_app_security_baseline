---
type: file_artifact
os: windows
artifact_name: "VBoxNetLwf.sys"
app: "[[VirtualBox]]"
artifact_type: driver
sensitivity: low
confidence: medium
status: active
tags:
  - windows/file-artifact
  - file/driver
source_row_ids:
  - third-party-service-039
---

# VBoxNetLwf.sys

## 1. 数据说明

`VBoxNetLwf.sys` 是 [[VirtualBox]] NDIS6 Bridged Networking Driver 的驱动镜像，常见于 VirtualBox 桥接网络能力。

## 2. 常见路径

```text
C:\Windows\System32\drivers\VBoxNetLwf.sys
```

## 3. 相关进程

- [[VBoxNetLwf]]
- [[VirtualBox]]

## 4. 数据内容

```text
VirtualBox 网络桥接驱动文件。
```

## 5. 安全关注点

```text
驱动文件路径不在 Windows drivers 目录
驱动签名与 Oracle / VirtualBox 发行方不一致
未授权资产出现 VirtualBox 桥接网络驱动
服务注册表 ImagePath 指向用户可写目录或异常文件名
```
