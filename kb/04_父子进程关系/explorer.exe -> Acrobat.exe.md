---
type: process_relation
os: windows
parent_process: "[[explorer.exe]]"
child_process: "[[Acrobat.exe]]"
relation: interactive_launch
normality: normal
risk_level: low
confidence: medium
status: active
tags:
  - relation/windows-app-profile
---

# explorer.exe -> Acrobat.exe

<!-- generated: windows-complete-profile-backfill -->

## 1. 关系说明

`explorer.exe` 启动 `Acrobat.exe` 是 [[Adobe Acrobat]] 画像中的常见进程链路之一。判断时必须结合路径、签名、命令行、启动账户、用户交互、服务注册表和网络行为。

## 2. 正常条件

```text
应用已授权安装
父进程、子进程路径和签名符合画像
命令行参数符合服务、更新、用户交互或管理场景
启动时间与用户操作、系统启动或企业变更记录一致
```

## 3. 异常条件

```text
子进程从用户目录、临时目录、下载目录或网络共享启动
命令行包含隐藏执行、下载执行、远程控制、凭据访问或异常代理参数
关系首次出现且伴随异常登录、服务创建、外联、文件落地或权限提升
签名、哈希、公司名或版本信息与应用不一致
```

## 4. 推荐处置

核验资产授权、服务 ImagePath、文件签名、父子进程时间线、网络目的地址和同主机相邻事件；不要只凭进程名定性。

## 5. 关联画像

- [[Adobe Acrobat]]
- [[explorer.exe]]
- [[Acrobat.exe]]
- [[AGMService]]
- [[AGSService]]
- [[AdobeARMservice]]
- [[AdobeUpdateService]]

## 6. 关联安全基线

- [[更新器外联行为]]
