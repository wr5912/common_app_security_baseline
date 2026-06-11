---
type: process
os: windows
process_name: "svchost.exe"
app: "[[Windows Per-user Services]]"
vendor: "Windows Per-user Services"
role:
  - service_process
risk_level: medium
confidence: medium
status: active
source_row_ids:
  - win-per-user-001
  - win-per-user-002
  - win-per-user-003
  - win-per-user-004
  - win-per-user-005
  - win-per-user-006
  - win-per-user-007
  - win-per-user-008
  - win-per-user-009
  - win-per-user-010
  - win-per-user-011
  - win-per-user-012
  - win-per-user-013
  - win-per-user-014
  - win-per-user-015
  - win-per-user-016
  - win-per-user-017
  - win-per-user-018
  - win-per-user-019
  - win-per-user-020
  - win-per-user-021
  - win-per-user-022
  - win-per-user-023
  - win-per-user-024
tags:
  - process/windows-source-full-coverage
---

# svchost.exe

<!-- generated: windows-source-full-coverage -->

## 1. 进程说明

本进程用于承载 [[Windows Per-user Services]] 在 Windows 服务或用户交互场景中的业务逻辑。若来源仅提供服务名而未给出精确 ImagePath，实际二进制路径必须以后续终端观测为准。

## 2. 所属应用

- [[Windows Per-user Services]]

## 3. 常见父进程

- [[services.exe]]
- [[explorer.exe]]

## 4. 异常行为

```text
从用户可写路径、临时目录、下载目录或网络共享启动
签名、厂商、版本或哈希与应用画像不一致
启动后立即连接未知外部地址、拉起脚本解释器或访问敏感配置
```

## 5. 关联安全基线

- [[第三方服务异常常驻]]
- [[应用异常网络外联行为]]
