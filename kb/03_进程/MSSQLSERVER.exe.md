---
type: process
os: windows
process_name: "MSSQLSERVER.exe"
app: "[[Microsoft SQL Server]]"
vendor: "Microsoft SQL Server"
role:
  - service_process
risk_level: medium
confidence: medium
status: active
source_row_ids:
  - third-party-service-043
  - third-party-service-044
  - third-party-service-045
  - third-party-service-046
  - third-party-service-047
  - third-party-service-048
tags:
  - process/windows-source-full-coverage
---

# MSSQLSERVER.exe

<!-- generated: windows-source-full-coverage -->

## 1. 进程说明

本进程用于承载 [[Microsoft SQL Server]] 在 Windows 服务或用户交互场景中的业务逻辑。若来源仅提供服务名而未给出精确 ImagePath，实际二进制路径必须以后续终端观测为准。

## 2. 所属应用

- [[Microsoft SQL Server]]

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
