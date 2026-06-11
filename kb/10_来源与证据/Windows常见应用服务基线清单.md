---
type: source_evidence
os: windows
title: Windows常见应用服务基线清单
source_type: scenario_list
confidence: medium
status: active
tags:
  - evidence/scenario-list
  - windows/service
---

# Windows常见应用服务基线清单

## 1. 来源说明

本页记录 `/tmp/windows系统上常见应用.md` 中的 Windows 常见应用 / 系统服务基线清单，作为本次补充 KB 的来源证据。原文件覆盖 Windows 内置系统服务、Per-user services、常见第三方应用服务、采集命令和落库归一化建议。

## 2. 关键建模要点

```text
ServiceName 比 DisplayName 更适合检测、关联和归一化。
Per-user services 常带 _LUID 后缀，应归一化为模板 ServiceName。
第三方服务应结合精确名、前缀/包含规则、签名厂商和路径共同识别。
Markdown / Obsidian 页面是主数据源，SQLite / Cypher / JSONL 是派生产物。
```

## 3. 本次落库范围

- 新增高频第三方场景应用、服务和进程画像。
- 新增 [[Windows第三方应用服务识别索引]] 覆盖第三方服务模式。
- 新增 VPN / 安全代理 / 数据库中间件 / 虚拟化开发服务安全基线。
- 暂不为数百个 Windows 内置服务逐一生成页面；后续按检测命中、风险等级或企业资产角色逐步拆分。

## 4. 待验证

- 服务 ImagePath、签名厂商、启动账户和命令行参数需用企业真实终端观测补强。
- 第三方服务名可能随版本、安装方式和企业定制包变化，需要保留低置信度状态直到样本验证。
