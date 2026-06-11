---
type: network_behavior
app: "[[Google Chrome]]"
process: "[[chrome.exe]]"
protocol:
  - HTTP
  - HTTPS
  - QUIC
purpose: web_browsing
risk_level: medium
confidence: medium
tags:
  - network/browser
---

# Chrome Web Browsing Network

## 1. 行为说明

Chrome 浏览器会根据用户访问行为连接大量域名和 IP，网络行为高度动态。

## 2. 常见端口

```text
80/tcp
443/tcp
443/udp
```

## 3. 安全关注点

```text
浏览器访问恶意域名
下载可执行文件或脚本
通过异常代理访问网络
浏览器拉起脚本解释器后外联
```

## 4. 关联安全基线

- [[浏览器拉起脚本解释器]]
