#!/usr/bin/env python3
"""Backfill canonical process creation/runtime baseline sections.

This script updates Markdown source pages only. SQLite, Cypher and JSONL files
remain derived artifacts and should be regenerated after the backfill.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

try:
    from .wabk_common import extract_frontmatter
except ImportError:  # allow running as: python tools/backfill_process_behavior_baselines.py
    from wabk_common import extract_frontmatter


MARKER = "<!-- baseline:process-creation-runtime -->"
BASELINE_LINK = "[[进程创建与运行时异常]]"


WINDOWS_PROCESS_CREATION = f"""{MARKER}
- 父进程基线：优先参考“常见父进程”和已建 `process_relation` 页面；服务型进程通常由 [[services.exe]] 启动，用户交互型进程通常由 [[explorer.exe]]、主程序或更新器启动。
- 启动账户基线：服务型进程需与服务画像中的启动账户、ImagePath、资产角色和授权范围一致；用户态进程需与登录用户、交互动作和启动来源一致。
- 路径基线：可执行文件应位于系统目录、厂商安装目录或企业授权部署目录；从用户可写目录、临时目录、下载目录、网络共享或异常挂载路径启动需要提高关注。
"""

LINUX_PROCESS_CREATION = f"""{MARKER}
- 父进程基线：守护进程通常由 [[systemd]]、服务管理器或 supervisor 类组件启动；用户交互进程通常由 shell、桌面会话或管理工具启动。
- 启动账户基线：服务进程需与 unit、配置文件、运行用户和资产角色一致；长期 root 运行、异常 setuid 或容器逃逸上下文需要提高关注。
- 路径基线：可执行文件应位于系统包、厂商安装目录或授权部署目录；从 `/tmp`、用户家目录、网络挂载或异常可写目录启动需要提高关注。
"""

WINDOWS_STARTUP = f"""{MARKER}
- 常见参数：记录服务模式、更新模式、用户交互模式、配置文件路径、插件/扩展路径等稳定参数类别；不要把单一版本样本写成全局白名单。
- 高风险参数：隐藏窗口、绕过策略、内联脚本、下载执行、异常代理、异常配置目录、调试/注入、凭据或令牌相关参数需要结合上下文研判。
- 动态情报边界：签名、哈希、信誉、首次出现时间和样本流行度由 EDR、资产台账或情报系统提供，本库只记录应核验的字段和异常条件。
"""

LINUX_STARTUP = f"""{MARKER}
- 常见参数：记录配置文件、前台/后台模式、监听地址、日志路径、插件目录和服务管理参数类别；不要把单一发行版样本写成全局白名单。
- 高风险参数：直接执行 shell、内联脚本、异常下载、LD_PRELOAD/库劫持、异常配置目录、暴露调试端口或凭据参数需要结合上下文研判。
- 动态情报边界：包签名、哈希、信誉、首次出现时间和样本流行度由资产台账、包管理器或情报系统提供，本库只记录应核验的字段和异常条件。
"""

PROCESS_RUNTIME = f"""{MARKER}
- 子进程：运行时拉起的子进程应符合“常见子进程”和父子关系画像；拉起脚本解释器、系统管理工具、下载器或未知二进制需要提高关注。
- 文件与注册表/配置：文件落点、配置读取、日志写入、注册表或 Linux 配置路径访问应与对应画像一致；新增持久化位置、敏感文件访问或异常写入需要补证据。
- 网络行为：监听端口、目的域名/IP、协议和代理设置应与网络行为画像一致；异常外联、非授权代理、数据上传或与命令执行相邻出现需要提高关注。
"""

PROCESS_SECURITY = f"""{MARKER}
- 进程创建链路与画像不一致：父进程、启动账户、路径、命令行或启动方式偏离常见画像。
- 运行时行为与画像不一致：子进程、文件、注册表/配置、网络目的地址或持久化行为无法由所属应用解释。
- 与高风险上下文相邻：新服务创建、权限提升、异常登录、下载落地、脚本解释器执行、数据打包或横向移动同时出现。
- 误报降级条件：资产已授权、路径和账户符合部署规范、命令行固定可解释、网络目的地址符合业务用途且无异常相邻事件。
"""

PROCESS_EVIDENCE = f"""{MARKER}
- 进程创建证据：时间、主机、用户、进程 GUID/PID、父进程 GUID/PID、完整命令行、当前目录、启动账户、完整镜像路径。
- 运行时证据：子进程链路、文件/注册表/配置访问、网络连接、监听端口、模块加载、服务/计划任务/Run Key 或 systemd/cron 变化。
- 外部核验：签名、哈希、证书链、信誉、首次出现时间、资产授权和变更单由 EDR、资产台账、软件分发或情报系统核验；不要把这些动态值沉淀为 Markdown 白名单。
"""

RELATION_CREATION = f"""{MARKER}
- 结构化关系：本页 `父进程 -> 子进程` 是可抽取的父子关系事实，判断时优先使用本页 frontmatter、标题和双链，不只依赖正文自然语言。
- 正常性判断：结合父进程来源、子进程路径、完整命令行、启动账户、服务/启动方式、所属应用和资产授权确认。
- 上下文边界：同一父子关系在服务启动、用户交互、更新器、插件、脚本执行或攻击链上下文中的风险等级可能不同。
"""

RELATION_ARGUMENTS = f"""{MARKER}
- 命令行与子进程角色不匹配，例如服务进程携带隐藏执行、下载执行、内联脚本、异常代理、异常配置目录或凭据相关参数。
- 子进程路径位于用户可写目录、临时目录、下载目录、网络共享或与所属应用不一致的位置。
- 父进程与业务上下文不匹配，例如 Office、浏览器、PDF 阅读器或远控进程拉起脚本解释器、系统管理工具或未知二进制。
"""

RELATION_EVIDENCE = f"""{MARKER}
- 进程创建事件：父子进程 GUID/PID、完整命令行、启动用户、当前目录、镜像路径、会话 ID 和完整时间线。
- 关联上下文：服务注册表或 systemd unit、启动方式、文件落地、网络连接、持久化写入、用户交互和资产授权记录。
- 外部核验：签名、哈希、信誉和流行度由情报/EDR/资产系统提供，本页只记录需要核验这些字段。
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Backfill process creation/runtime baseline sections.")
    parser.add_argument("--vault", default="kb", help="Knowledge-base vault root")
    parser.add_argument("--dry-run", action="store_true", help="Report files that would change without writing")
    return parser.parse_args(argv)


def normalize_heading(value: str) -> str:
    text = re.sub(r"^\s*\d+\.\s*", "", value or "").strip()
    return re.sub(r"\s+", "", text)


def level2_matches() -> re.Pattern[str]:
    return re.compile(r"^##\s+(.+?)\s*$", flags=re.M)


def get_os(raw: str) -> str:
    fm, _ = extract_frontmatter(raw)
    value = fm.get("os", "")
    return str(value).strip().lower() or "cross"


def find_section_span(body: str, aliases: list[str]) -> tuple[re.Match[str], int, int] | None:
    wanted = {normalize_heading(alias) for alias in aliases}
    matches = list(level2_matches().finditer(body))
    for idx, match in enumerate(matches):
        if normalize_heading(match.group(1)) in wanted:
            start = match.start()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(body)
            return match, start, end
    return None


def find_insert_pos(body: str, before_aliases: list[str] | None = None, after_aliases: list[str] | None = None) -> int:
    if before_aliases:
        found = find_section_span(body, before_aliases)
        if found:
            return found[1]
    if after_aliases:
        found = find_section_span(body, after_aliases)
        if found:
            return found[2]
    return len(body.rstrip()) + 1


def ensure_section(
    body: str,
    canonical_title: str,
    content: str,
    aliases: list[str] | None = None,
    before: list[str] | None = None,
    after: list[str] | None = None,
) -> str:
    aliases = [canonical_title, *(aliases or [])]
    existing = find_section_span(body, aliases)
    if existing:
        match, start, end = existing
        section = body[start:end]
        title_start, title_end = match.span(1)
        section = section[: title_start - start] + canonical_title + section[title_end - start :]
        if MARKER not in section:
            section = section.rstrip() + "\n\n" + content.strip() + "\n"
        return body[:start] + section + body[end:]

    insert_at = find_insert_pos(body, before_aliases=before, after_aliases=after)
    block = f"\n## {canonical_title}\n\n{content.strip()}\n"
    return body[:insert_at].rstrip() + "\n" + block + "\n" + body[insert_at:].lstrip()


def ensure_link_in_section(body: str, section_title: str, link: str, fallback_before: list[str] | None = None) -> str:
    existing = find_section_span(body, [section_title])
    if not existing:
        body = ensure_section(body, section_title, f"- {link}", before=fallback_before)
        existing = find_section_span(body, [section_title])
    if not existing:
        return body
    _, start, end = existing
    section = body[start:end]
    if link not in section:
        section = section.rstrip() + f"\n- {link}\n"
        body = body[:start] + section + body[end:]
    return body


def renumber_l2(body: str) -> str:
    count = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        title = re.sub(r"^\s*\d+\.\s*", "", match.group(1)).strip()
        return f"## {count}. {title}"

    return level2_matches().sub(repl, body)


def update_process(raw: str) -> str:
    os_name = get_os(raw)
    creation = LINUX_PROCESS_CREATION if os_name == "linux" else WINDOWS_PROCESS_CREATION
    startup = LINUX_STARTUP if os_name == "linux" else WINDOWS_STARTUP

    fm, body = extract_frontmatter(raw)
    prefix = raw[: raw.find(body)] if body and body in raw else ""
    body = ensure_section(
        body,
        "进程创建基线",
        creation,
        before=["常见启动参数", "高风险参数", "启动参数基线", "异常行为", "异常关注点", "关联安全基线"],
        after=["常见父子关系", "常见子进程", "常见父进程"],
    )
    body = ensure_section(
        body,
        "启动参数基线",
        startup,
        aliases=["常见启动参数", "高风险参数"],
        before=["运行时行为基线", "异常行为", "异常关注点", "关联安全基线"],
        after=["进程创建基线"],
    )
    body = ensure_section(
        body,
        "运行时行为基线",
        PROCESS_RUNTIME,
        before=["安全关注点", "参数安全关注", "异常行为", "异常关注点", "关联安全基线"],
        after=["启动参数基线"],
    )
    body = ensure_section(
        body,
        "安全关注点",
        PROCESS_SECURITY,
        aliases=["参数安全关注", "异常行为", "异常关注点"],
        before=["证据需求", "关联安全基线"],
        after=["运行时行为基线"],
    )
    body = ensure_section(
        body,
        "证据需求",
        PROCESS_EVIDENCE,
        before=["关联安全基线"],
        after=["安全关注点"],
    )
    body = ensure_link_in_section(body, "关联安全基线", BASELINE_LINK)
    body = renumber_l2(body)
    return prefix + body.lstrip()


def update_relation(raw: str) -> str:
    fm, body = extract_frontmatter(raw)
    prefix = raw[: raw.find(body)] if body and body in raw else ""
    body = ensure_section(
        body,
        "创建链路基线",
        RELATION_CREATION,
        before=["可能正常场景", "高风险场景", "高风险参数", "关联画像"],
        after=["子进程", "父进程", "关系说明"],
    )
    body = ensure_section(
        body,
        "高风险参数与命令行关注",
        RELATION_ARGUMENTS,
        aliases=["高风险参数"],
        before=["需要补充的证据", "证据需求", "检测建议", "误报条件", "关联画像"],
        after=["高风险场景", "创建链路基线"],
    )
    body = ensure_section(
        body,
        "证据需求",
        RELATION_EVIDENCE,
        aliases=["需要补充的证据"],
        before=["检测建议", "误报条件", "推荐处置", "关联画像"],
        after=["高风险参数与命令行关注"],
    )
    body = ensure_link_in_section(body, "关联画像", BASELINE_LINK)
    body = renumber_l2(body)
    return prefix + body.lstrip()


def update_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    if "/03_进程/" in path.as_posix():
        new_raw = update_process(raw)
    else:
        new_raw = update_relation(raw)
    if new_raw != raw:
        path.write_text(new_raw, encoding="utf-8")
        return True
    return False


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    vault = Path(args.vault)
    targets = sorted((vault / "03_进程").glob("*.md")) + sorted((vault / "04_父子进程关系").glob("*.md"))
    changed: list[Path] = []
    for path in targets:
        raw = path.read_text(encoding="utf-8")
        new_raw = update_process(raw) if "/03_进程/" in path.as_posix() else update_relation(raw)
        if new_raw != raw:
            changed.append(path)
            if not args.dry_run:
                path.write_text(new_raw, encoding="utf-8")

    for path in changed:
        print(path.as_posix())
    print(f"changed={len(changed)} dry_run={args.dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
