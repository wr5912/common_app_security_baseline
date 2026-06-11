---
type: process
os: windows
process_name: elevation_service.exe
app: "[[Brave Browser]]"
vendor: Brave Software
role:
  - 安装提权辅助
  - 更新辅助
risk_level: medium
confidence: low
status: needs_review
tags:
  - process/browser
  - windows/service-process
---

# elevation_service.exe

## 1. 进程说明

`elevation_service.exe` 在本库中用于承载 [[Brave Browser]] 的提权或更新辅助进程识别。该文件名也可能被其他 Chromium 系应用使用，不能仅凭进程名判断归属。

## 2. 所属应用

- [[Brave Browser]]

## 3. 常见路径

```text
C:\Program Files\BraveSoftware\Brave-Browser\Application\elevation_service.exe
```

## 4. 常见父进程

- [[services.exe]]

## 5. 异常行为

```text
路径不在 Brave 官方安装目录
签名厂商不一致
服务名、ImagePath 与资产授权软件不匹配
异常时间窗口内伴随未知下载或服务创建
```

## 6. 证据与来源

- 来源类型：[[Windows常见应用服务基线清单]]
- 可信度：low
- 待验证：需用真实终端样本确认 Brave 版本、路径和签名。
