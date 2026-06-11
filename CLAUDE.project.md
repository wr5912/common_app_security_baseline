# 项目覆盖说明

本文件只放当前项目的专属约束。团队通用行为以 `CLAUDE.md` 和 `.claude/rules/` 为准。

## 项目上下文

- 项目名称：`Windows应用安全基线画像库`
- 主要目标：维护一套面向人和 AI 共同维护的 Windows 应用 / 服务 / 进程 / 父子关系 / 注册表 / 文件 / 网络 / 安全基线 Markdown Wiki，并可抽取为 SQLite、Neo4j、API 检索等结构化派生数据。
- 关键模块：`00_总览/`、`01_应用/`、`02_服务/`、`03_进程/`、`04_父子进程关系/`、`05_启动方式/`、`06_注册表画像/`、`07_文件与数据/`、`08_网络行为/`、`09_安全基线/`、`10_来源与证据/`、`11_抽取与图谱/`、`99_模板/`、`raw_sources/`、`logs/`、`tools/`。
- 必读文档：`README.md`、`00_总览/Windows应用安全基线画像库 AI 维护规范.md`、`00_总览/Windows应用安全基线画像库总览.md`、`00_总览/维护工作流.md`、对应类型模板（`99_模板/*`）、相关实体页面、`logs/变更日志.md`。

## 项目专属质量策略

- 产品不变量：
  - Markdown / Obsidian 是唯一正式知识源；`out/` 中的 SQLite、JSONL、Cypher 是派生产物，不得当作主数据源手工编辑；知识修订先回写 Markdown，再重建结构化数据。
  - 安全判断不得在无来源的情况下从“可疑”升级为“恶意”；尽量保留误报条件、业务上下文和证据需求。
  - 不确定字段标记 `confidence: low` 或 `status: needs_review`。
  - 一个页面只表达一个主要实体或关系；父子进程关系等“关系类”判断单独建文档。
  - 维护双链、索引入口和 `logs/变更日志.md`，不删除旧判断而不记录原因。
- 兼容边界：可调整 Markdown 模板与 `tools/` 抽取脚本；改动 frontmatter 字段、`type` 枚举、目录结构或 API 输出契约时，必须同步 `README.md`、`00_总览/Windows应用安全基线画像库 AI 维护规范.md`、`11_抽取与图谱/` 抽取规范和样例数据。
- 旧设计清理策略：本项目以知识库维护为主，通用 rules 中偏 Agent runtime 的输出契约约束只在 `tools/` 或未来 Agent 流程中适用，普通 Markdown 维护任务不强制套用。

## 项目验证入口

- 局部开发验证：`.venv/bin/python tools/kb_to_sqlite.py --vault . --out out/windows_app_baseline.db --rebuild --debug --log-file logs/kb_to_sqlite.debug.log`
- 主流程验证：在上一步基础上运行 `.venv/bin/python tools/kb_to_neo4j.py --vault . --out out/windows_app_baseline.cypher --debug --log-file logs/kb_to_neo4j.debug.log`；需要服务时再 smoke `tools/api_service.py`。
- 完整验证硬门：未配置（计划由 `tools/validate_wiki.py` 等 Markdown 结构校验脚本承担；脚本稳定前以人工审核 frontmatter / `type` / 双链 / 索引 / 变更日志为准）。
- 覆盖清单或测试 manifest：未配置。

`warn`、dry-run 或只读审计类命令只能用于 Analyze 阶段观察。当前项目尚未配置阻断硬门，Verify 阶段以构建脚本可重复运行 + 人工结构审核为准。

## CI 与差异治理

- PR 对比基线：未配置。
- 主分支 push 对比基线：未配置。
- 旧债处理策略：通过 `logs/变更日志.md` 和 `logs/` 待办记录跟踪。
- CI workflow：未配置。

## 配置与环境边界

- 环境变量文件：未配置（暂无 `.env`）；如未来接入 Neo4j / MCP，真实 URL、账户、密码、header 只放本地私有文件。
- 应用配置文件：`tools/` 脚本参数由命令行传入，无常驻 config。
- Docker/Compose 入口：未配置。
- 持久化数据路径：`out/` 与 `logs/*.debug.log` 均为生成物，已在 `.gitignore` 中忽略，不提交。
- Python 环境：使用仓库本地 `.venv` 并以 `uv` 管理依赖（`uv venv .venv`、`uv pip install -r tools/requirements.txt`、`.venv/bin/python ...`），禁止直接使用 `pip`。
- 密钥边界：真实 API key、Neo4j 密码、MCP header、本机私有路径和运行态数据不得提交。

## Claude Code 专项

- 必须按需使用的项目 skill：`.claude/skills/wiki-maintenance/SKILL.md`（新增 / 更新画像、补安全基线、变更日志、结构化抽取影响）；通用工程行为见 `.claude/skills/project-skill/SKILL.md`。
- 推荐子代理：`.claude/agents/project-worker.md`（大范围搜索、独立审查、隔离上下文任务）。
- 项目 MCP：未配置。SQLite / Neo4j / API 是否需要 MCP 接入尚未成型，只有出现真实工具调用需求时再设计 `.mcp.json`。
- 本地私有说明：个人偏好放在 `CLAUDE.local.md`，个人模型示例见 `.claude/settings.local.json.example`；真实 `CLAUDE.local.md` 与 `.claude/settings.local.json` 已被 `.gitignore` 忽略，不入库。

## 专属边界

- 不要把本项目的脚本名、私有路径、端口、产品不变量或临时迁移策略写回通用 `CLAUDE.md`、`.claude/rules/` 或通用 skill。
- 如果其他项目复用本模板，必须重新填写自己的覆盖层、治理命令、base-ref 策略和环境边界。
