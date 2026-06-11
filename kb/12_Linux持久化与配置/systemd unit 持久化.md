---
type: config_persistence
os: linux
mechanism: systemd-unit
path_pattern: /etc/systemd/system/*.service
purpose:
  - 服务常驻
  - 开机自启
risk_level: high
confidence: high
tags:
  - linux/persistence
  - persistence
---

# systemd unit 持久化

> Linux 侧最主要的服务持久化位置，对应 Windows 的 [[HKLM_SYSTEM_CurrentControlSet_Services]]。

## 1. 位置说明

systemd 通过 unit 文件描述常驻服务。正常由软件包、运维部署或容器编排写入；攻击者也常借此实现持久化。

## 2. 关键路径

```text
/etc/systemd/system/*.service        # 管理员 / 部署写入，优先级高
/usr/lib/systemd/system/*.service    # 发行版包写入
~/.config/systemd/user/*.service     # 用户级，无需 root
/run/systemd/system/*.service        # 运行态临时单元
```

## 3. 正常写入场景

```text
apt / yum / dnf 安装服务（如 [[nginx.service]]）
运维通过 systemctl enable 部署
容器 / 编排工具注册守护
```

## 4. 异常关注点

```text
ExecStart 指向用户目录、/tmp、/dev/shm 或解释器
用户级 unit 实现免 root 持久化
Restart=always 维持恶意常驻
unit 名伪装系统服务
启用后立即外联或落地文件
最近修改时间与变更窗口不符
```

## 5. 关联

- 启动方式：[[systemd Service]]
- 安全基线：[[服务持久化机制对比]]
