---
type: security_baseline
os: windows
baseline_id: base_vpn_proxy_service
object_type: service
normality: rare
risk_level: medium
confidence: low
status: needs_review
tags:
  - baseline/vpn-proxy
  - risk/medium
---

# VPN与代理服务常驻

## 1. 基线说明

VPN、Mesh VPN 或代理类服务常驻可能是合法远程接入，也可能形成绕过边界控制的隐蔽通道。

## 2. 关联对象

- [[OpenVPN]]
- [[WireGuard]]
- [[Tailscale]]
- [[ZeroTier]]
- [[GlobalProtect]]
- [[Cisco AnyConnect]]

## 3. 合法条件

```text
资产台账登记
网关或网络 ID 属于企业授权范围
服务路径和签名可信
变更记录可追溯
```

## 4. 异常条件

```text
未授权终端出现 VPN / 代理服务
连接未知公网网关或个人网络
服务由 NSSM 等包装器从临时目录注册
伴随异常远程登录或横向移动
```

## 5. 推荐处置

优先核验资产角色、授权状态、服务 ImagePath、签名、启动账户、监听端口、网络目的地址和变更时间线。不要只凭服务名判断恶意。

## 6. 证据与来源

- 来源页面：[[Windows常见应用服务基线清单]]
- 待验证：企业资产角色、授权清单、真实命令行和网络观测。
