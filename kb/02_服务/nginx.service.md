---
type: service
os: linux
service_name: nginx.service
display_name: A high performance web server and a reverse proxy server
app: "[[nginx]]"
vendor: nginx / F5
service_type: systemd-unit
start_type: enabled
start_account: root
image_name: /usr/sbin/nginx
risk_level: medium
confidence: medium
status: active
tags:
  - service/web-server
  - linux/service
  - persistence
---

# nginx.service

## 1. 服务说明

nginx 的 systemd 服务单元，开机自启并常驻，负责拉起 nginx master 进程。对应 Windows 的 [[Windows Service]] 角色。

## 2. 关键 unit 字段

```ini
[Service]
Type=forking
ExecStartPre=/usr/sbin/nginx -t -q -g 'daemon on; master_process on;'
ExecStart=/usr/sbin/nginx -g 'daemon on; master_process on;'
ExecReload=/usr/sbin/nginx -g 'daemon on; master_process on;' -s reload
User=root
```

## 3. 常见父进程

- [[systemd]]（PID 1）

## 4. 常见进程

- [[nginx (进程)]]

## 5. 持久化位置

- [[systemd unit 持久化]]

## 6. 异常关注点

```text
ExecStart 指向用户目录 / 临时目录
unit 文件在可写目录（如 /etc/systemd/system 被异常写入）
启动后立即外联或落地文件
被伪装成系统 unit 名
```
