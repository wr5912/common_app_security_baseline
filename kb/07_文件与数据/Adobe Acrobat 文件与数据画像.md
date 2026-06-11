---
type: file_artifact
os: windows
artifact_name: "Adobe Acrobat 文件与数据画像"
app: "[[Adobe Acrobat]]"
artifact_type: install_config_log
sensitivity: medium
confidence: medium
status: active
tags:
  - artifact/windows-app-profile
source_row_ids:
  - third-party-office-006
  - third-party-office-007
  - third-party-office-008
  - third-party-service-011
  - third-party-service-012
  - third-party-service-013
  - third-party-service-014
---
# Adobe Acrobat 文件与数据画像

<!-- generated: windows-complete-profile-backfill -->

## 1. 数据说明

本页记录 [[Adobe Acrobat]] 的安装目录、配置、日志、缓存或用户态数据位置模式，用于判断路径、签名、落地时间线和数据访问是否符合应用画像。

## 2. 常见路径

```text
%APPDATA%\AdobeAcrobat\\
%LOCALAPPDATA%\AdobeAcrobat\\
%ProgramData%\AdobeAcrobat\\
C:\Program Files (x86)\Common Files\Adobe\ARM\1.0\armsvc.exe
C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe
C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe
```

## 3. 相关进程

- [[AcroRd32.exe]]
- [[Acrobat.exe]]
- [[armsvc.exe]]

## 4. 数据内容

- 安装目录和主程序文件。
- 服务配置、日志、缓存、更新器落地目录或用户配置。
- 具体文件名、版本目录和日志位置可能随安装方式、语言、企业定制包变化。

## 5. 安全关注点

```text
主程序或服务二进制落在用户可写目录、临时目录或下载目录
同名文件签名、哈希或厂商信息与应用不一致
日志、配置或缓存中出现凭据、令牌、远控会话信息或数据库连接串
文件落地时间与异常服务创建、外联、登录或权限提升接近
```

## 6. 关联对象

- [[Adobe Acrobat]]
- [[应用敏感文件与配置访问异常]]
- [[Windows常见应用完整画像验收清单]]
