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
source_row_ids:
  - third-party-service-066
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

## 全量来源覆盖

<!-- generated: windows-source-full-coverage -->

- 来源行：`third-party-service-066`
- 相关服务：
- [[nginx Service]]
- 相关进程：
- [[nginx.exe]]
- 父子关系：
- [[services.exe -> nginx.exe]]
- 文件：[[nginx 文件与数据画像]]
- 注册表：[[nginx 注册表画像]]
- 网络：[[nginx 网络行为]]
- 证据：[[nginx 画像证据记录]]
