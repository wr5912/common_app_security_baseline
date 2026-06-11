---
type: config_persistence
os: linux
mechanism:                # systemd-unit | cron | rc-local | profile | ld-preload | ...
path_pattern:
purpose: []
risk_level:
confidence: low
status: draft
tags:
  - linux/persistence
  - persistence
---

# <Linux 持久化 / 配置位置名称>

> Linux 侧持久化与配置位置，对应 Windows 的注册表持久化（见 [[注册表关键位置索引]]）。

## 1. 位置说明

<这是什么持久化 / 配置机制，正常由哪些应用或运维流程写入>

## 2. 关键路径

```text
<例如 /etc/systemd/system/*.service、/etc/cron.d/*、/etc/crontab、~/.bashrc>
```

## 3. 正常写入场景

```text
<软件包安装、运维部署、容器编排、定时任务>
```

## 4. 异常关注点

```text
可写目录中新增 unit / cron
ExecStart / 命令指向用户目录、临时目录或解释器
启用后立即外联或落地文件
伪装系统 unit 名
最近修改时间与变更窗口不符
```

## 5. 关联安全基线

- <[[相关安全基线]]>
