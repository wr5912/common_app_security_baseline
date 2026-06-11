---
description: 维护 终端应用安全基线画像库 Markdown Wiki。用于新增/更新应用、服务、进程、父子关系、注册表、文件、网络或安全基线画像，补证据、双链、索引和变更日志，并保证结构化抽取可用。
---

# Wiki 维护技能

当任务涉及在 `终端应用安全基线画像库` 中新增或更新画像（应用 / 服务 / 进程 / 父子关系 / 注册表 / 文件 / 网络 / 安全基线），或补充来源证据、安全基线、索引与变更日志时，使用本技能。

通用工程行为见 `.claude/skills/project-skill/SKILL.md`，项目事实见 `CLAUDE.project.md`。本技能只承载知识库维护的高频流程。

## 1. 必读顺序

每次维护前按顺序读取：

1. `README.md`
2. `kb/00_总览/终端应用安全基线画像库 AI 维护规范.md`
3. `kb/00_总览/终端应用安全基线画像库总览.md` 与 `kb/00_总览/维护工作流.md`
4. 对应类型模板，例如 `kb/99_模板/应用画像模板.md`
5. 已存在的相关实体页面（避免重复建页或破坏已有双链）
6. `kb/logs/变更日志.md`

## 2. 主数据源不变量

- Markdown / Obsidian 是唯一正式知识源；`out/` 中的 SQLite、JSONL、Cypher 是派生产物。
- 任何知识修订都先回写 Markdown，再由 `tools/` 重新构建结构化数据；不得把 SQLite / Cypher / JSONL 当主数据源直接编辑。
- 在任务计划中明确写出本次写入的 Markdown 页面，再考虑是否需要重建派生数据。

## 3. 选择模板与目录

| type | os 典型值 | 目录 | 模板 |
|---|---|---|---|
| `app` | windows / linux | `kb/01_应用/` | `kb/99_模板/应用画像模板.md` |
| `service` | windows / linux | `kb/02_服务/` | `kb/99_模板/服务画像模板.md` |
| `process` | windows / linux | `kb/03_进程/` | `kb/99_模板/进程画像模板.md` |
| `process_relation` | windows / linux | `kb/04_父子进程关系/` | `kb/99_模板/父子进程关系模板.md` |
| `startup_method` | windows / linux | `kb/05_启动方式/` | `kb/99_模板/启动方式模板.md` |
| `registry_pattern` | windows | `kb/06_注册表画像/` | `kb/99_模板/注册表行为模板.md` |
| `file_artifact` | windows / linux | `kb/07_文件与数据/` | `kb/99_模板/文件数据行为模板.md` |
| `network_behavior` | windows / linux | `kb/08_网络行为/` | `kb/99_模板/网络行为模板.md` |
| `security_baseline` | windows / linux / cross | `kb/09_安全基线/` | `kb/99_模板/安全基线模板.md` |
| `source_evidence` | windows / linux | `kb/10_来源与证据/` | `kb/99_模板/证据记录模板.md` |
| `config_persistence` | linux | `kb/12_Linux持久化与配置/` | `kb/99_模板/Linux持久化与配置模板.md` |
| `extract_spec` | cross | `kb/11_抽取与图谱/` | （规范文档，无画像模板） |

文件命名遵循 README 第 9 节：应用 `Google Chrome.md`、服务 `gupdate.md`、进程 `chrome.exe.md`、关系 `winword.exe -> powershell.exe.md`。

## 4. 实体拆分与平台维度

- 一个页面只表达一个主要实体或关系，`type` 必须准确。
- 每个画像页面必须标注 `os: windows | linux | cross`；缺省时抽取会按 `windows/*`/`linux/*` 标签和目录回退，但应显式写明。
- 跨平台共享目录（应用 / 服务 / 进程 / 父子关系 / 启动方式 / 文件 / 网络 / 安全基线 / 来源证据）按 `os` 字段区分 Windows 与 Linux 实体；平台专属持久化分目录：Windows 用 `kb/06_注册表画像/`（`registry_pattern`），Linux 用 `kb/12_Linux持久化与配置/`（`config_persistence`），二者互为对应。
- 跨平台对照 / 方法论页用 `os: cross`，例如 [[服务持久化机制对比]]。
- 不把多个服务 / 进程合并进一个页面。
- 父子进程关系等“关系类”安全判断必须单独建 `process_relation` 文档，不能只写在进程页内。

## 5. 双链与索引

- 使用 Obsidian 双链表达关系，不用裸文本代替已有页面链接：
  `所属应用：[[Google Chrome]]`、`相关服务：[[gupdate]]`、`父子关系：[[services.exe -> GoogleUpdate.exe]]`、`安全基线：[[更新器外联行为]]`。
- 新增实体后，在对应 `kb/00_总览/*索引.md` 增加入口（应用分类、服务分类、进程分类、高风险父子进程关系、安全基线、注册表关键位置）。
- 不破坏已有链接；重命名页面时同步引用方。

## 6. 安全判断与证据

- 分层使用：`normality: normal | rare | suspicious | malicious_like`、`risk_level: low | medium | high | critical`、`confidence: low | medium | high`、`status: draft | needs_review | active | deprecated`。
- 不在无来源情况下把“可疑”升级为“恶意”；保留误报条件、业务上下文和证据需求。
- 来源写入 `kb/10_来源与证据/`，或在页面“证据与来源”区记录来源类型、采集时间、可信度、说明。
- 不确定时标记 `confidence: low` / `status: needs_review`，不用虚假确定性填满页面。

## 7. 变更日志

每次重要更新后在 `kb/logs/变更日志.md` 追加：

```markdown
## YYYY-MM-DD | 类型 | 标题

- 变更内容：
- 影响页面：
- 依据来源：
- 待验证问题：
```

## 8. 结构化抽取影响

改动以下内容会影响 `tools/` 抽取与下游 SQLite / Neo4j / API，必须谨慎并同步：

- frontmatter 字段或 `type` 枚举：同步 `README.md`、AI 维护规范、`kb/11_抽取与图谱/` 抽取规范和样例数据。
- 目录结构或标题结构：确认 `tools/kb_to_sqlite.py` / `kb_to_neo4j.py` 的 section / link 抽取仍成立。
- 双链写法：保持机器可解析，关系用 `[[...]]`，不用自然语言暗示。

## 9. 完成后验证

- 结构自检：YAML 可解析、`type` 正确、双链目标存在、索引入口已加、变更日志已追加。
- 如改动可能影响抽取，运行（先 `uv venv .venv` + `uv pip install -r tools/requirements.txt`）：
  - `.venv/bin/python tools/kb_to_sqlite.py --vault kb --out out/windows_app_baseline.db --rebuild --debug --log-file kb/logs/kb_to_sqlite.debug.log`
  - `.venv/bin/python tools/kb_to_neo4j.py --vault kb --out out/windows_app_baseline.cypher --debug --log-file kb/logs/kb_to_neo4j.debug.log`
  - 关注日志中的 `unresolved target`，确认新增双链已解析。
- 说明未验证项、原因和残余风险。

## 推荐回答模式

当用户要求“补充某应用画像”时：先判断该创建/更新哪些页面 → 输出新增/修改页面清单 → 按模板生成内容 → 补索引和双链 → 记录变更日志 → 标出待验证项。
