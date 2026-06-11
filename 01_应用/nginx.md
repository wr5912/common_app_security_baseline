---
type: app
os: linux
app_id: app_nginx
app_name_cn: nginx
app_name_en: nginx
vendor: nginx / F5
category: Web 服务器
subcategory: 反向代理 / HTTP 服务
is_system_builtin: false
confidence: medium
status: active
tags:
  - app/web-server
  - vendor/nginx
  - linux/app
---

# nginx

## 1. 基本说明

nginx 是 Linux 上常见的高性能 Web 服务器与反向代理，通常由发行版包管理器安装，并以 systemd 服务常驻。

## 2. 常见服务

- [[nginx.service]]

## 3. 常见进程

- [[nginx (进程)]]（master / worker）

## 4. 启动方式

- [[systemd Service]]

## 5. 持久化与配置

- [[systemd unit 持久化]]
- 配置目录：`/etc/nginx/`

## 6. 关联安全基线

- [[服务持久化机制对比]]

## 7. 异常关注点

```text
worker 进程拉起 shell / 解释器（如 nginx -> sh -> curl）
配置中新增可疑 proxy_pass 外联
unit 的 ExecStart 指向非标准路径
监听非预期端口或对外暴露管理接口
```
