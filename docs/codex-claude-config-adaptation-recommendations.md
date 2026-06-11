# Codex / Claude 配置适配建议

生成日期：2026-06-11

## 结论摘要

当前仓库已经复制了团队通用的 Codex 与 Claude Code 配置骨架，但还没有完成对 `Windows应用安全基线画像库` 的项目化适配。最明显的问题不是配置缺失，而是项目覆盖层仍保留模板占位，导致 Agent 无法稳定知道本项目的主数据源、维护约束、验证入口和安全边界。

建议先补齐 `AGENTS.override.md` 与 `CLAUDE.project.md` 的项目事实，再把可重复的 Wiki 维护流程沉淀为按需 skill。暂时不要启用 hooks，也不要新增 MCP；等有确定性校验脚本和稳定命令后再接入自动化。

## 当前证据

- `AGENTS.override.md` 和 `CLAUDE.project.md` 仍包含项目名称、目标、关键模块、验证入口、CI、环境边界、专项 skill 等占位内容。
- `README.md` 已明确项目定位：Markdown / Obsidian 是源头，SQLite、Neo4j、API 服务是派生产物。
- `Windows应用安全基线画像库 AI 维护规范.md` 已定义 AI 维护规则、必读顺序、模板使用、Obsidian 链接、证据记录和变更日志要求，但尚未被项目覆盖层明确收口为 Codex / Claude 的共同约束。
- `.codex/hooks.json` 当前为空，符合“没有稳定治理命令前不启用 hook”的边界。
- `.claude/settings.json` 已包含基本密钥读取 deny 规则，但本地私有文件边界还未完全落到 `.gitignore`。
- 标准 Codex 配置审计命令 `.venv/bin/python .codex/skills/codex-config-optimizer/scripts/audit_codex_config.py` 当前因 `.venv` 不存在无法运行；使用系统 `python3` 替代执行时，审计报告显示 `surfaces: 10`，未发现 P0/P1/P2 静态问题，但提示多个治理词存在重复收口空间。
- `tools/README.md` 当前使用 `venv/pip` 示例；团队通用 Codex 规则要求 `.venv/uv`，两者需要统一。

## 官方配置面依据

- Codex 项目级配置应放在仓库内 `.codex/config.toml`，用户级配置放在 `~/.codex/config.toml`：<https://developers.openai.com/codex/config-basic>
- Codex 通过 `AGENTS.md` / `AGENTS.override.md` 加载项目说明，并按目录层级组合：<https://developers.openai.com/codex/guides/agents-md>
- Codex skills 适合承载可复用工作流，正文按需加载：<https://developers.openai.com/codex/skills>
- Codex hooks 适合确定性生命周期检查，不适合承载主观判断：<https://developers.openai.com/codex/hooks>
- Claude Code 项目根 `CLAUDE.md` 用于会话启动时读取编码标准、架构决策、库偏好和检查清单：<https://code.claude.com/docs/en/overview>
- Claude Code skills 适合反复粘贴的流程和检查清单，避免常驻说明膨胀：<https://code.claude.com/docs/en/skills>
- Claude Code subagents 适合大范围搜索、独立审查和隔离上下文任务：<https://code.claude.com/docs/en/sub-agents>
- Claude Code `.mcp.json` 支持环境变量展开，可共享配置但不提交密钥：<https://code.claude.com/docs/en/mcp>
- Claude Code hooks 用于自动执行确定性命令；需要判断的问题仍应交给 skill 或人工审查：<https://code.claude.com/docs/en/hooks-guide>

## 配置治理建议

| 证据 | 当前配置面 | 问题 | 动作 | 目标配置面 | 验证 | 风险 |
| --- | --- | --- | --- | --- | --- | --- |
| 项目覆盖层仍是模板占位 | `AGENTS.override.md`、`CLAUDE.project.md` | Agent 不能稳定知道本项目名称、目标、模块和必读文档 | `merge` | 两个覆盖层分别填入同一组项目事实 | 搜索无占位内容；新会话能复述项目定位 | 不适配会导致通用规则压过项目事实 |
| README 已声明 Markdown / Obsidian 是主数据源 | 覆盖层未声明 | Agent 可能直接改派生 SQLite、Cypher 或 API 结果 | `keep` | 覆盖层产品不变量 | 修改任务计划中必须写明 Markdown 是唯一正式写入源 | 派生产物被手工修改后会与 Wiki 漂移 |
| AI 维护规范已存在 | 独立根目录文档 | Codex / Claude 不一定优先读取该规范 | `merge` | 覆盖层“必读文档” | 新任务计划先读 README、总览、模板、相关页面、变更日志 | 复制整篇规范到常驻配置会增加上下文噪声 |
| 新增或更新画像是高频流程 | 目前散落在 README、维护规范、模板中 | 维护步骤长，不适合每次常驻加载 | `move-to-skill` | `.codex/skills/wiki-maintenance/SKILL.md` 与 `.claude/skills/wiki-maintenance/SKILL.md` | 触发“新增应用画像/更新服务画像/补安全基线”时自动读取 skill | 不沉淀 skill 会反复靠 prompt 约束，漏变更日志和索引 |
| Frontmatter、type、双链、索引、变更日志可机械检查 | 当前无统一检查命令 | Verify 阶段只能靠人工肉眼确认 | `move-to-script` | `tools/validate_wiki.py` 或等价校验脚本 | 可检查 YAML、type、链接目标、索引入口、变更日志追加 | 直接接 hook 前若脚本不稳定，会阻断正常维护 |
| `.codex/hooks.json` 为空 | `.codex/hooks.json` | 当前没有稳定项目治理命令 | `keep` | 暂不启用 Codex hooks | 保持 `hooks: []`，直到校验脚本可重复运行 | 过早启用 hook 可能出现命令不存在或误阻断 |
| Claude hooks 未配置 | `.claude/settings.json` | 当前只有权限 deny，未配置自动治理 | `keep` | 暂不配置 Claude hooks | 本地 Claude 运行不因缺命令失败 | 过早接入 hook 会让 Claude 配置变成环境绑定 |
| 工具文档使用 `pip`，团队规则使用 `uv` | `tools/README.md`、`AGENTS.md`、`.codex/skills/project-skill` | 环境入口不一致，审计脚本标准命令也因 `.venv` 缺失失败 | `merge` | 覆盖层与工具文档统一为 `.venv/bin/python`；依赖安装建议使用 `uv pip install -r tools/requirements.txt` | `.venv/bin/python` 可运行 SQLite / Neo4j / API 工具与配置审计脚本 | 如果团队仍希望保留纯 Python venv/pip，需要明确写成项目例外 |
| `.claude/settings.local.json.example` 包含个人模型示例 | Claude 本地示例 | 示例文件可保留，但真实本地配置不能入库 | `keep` | `.gitignore` 补充私有 Claude 本地文件 | `git status` 不显示真实 `CLAUDE.local.md` 或 `.claude/settings.local.json` | 忽略规则缺失时个人模型、路径或账号偏好可能被提交 |
| 当前没有项目 MCP | 根目录无 `.mcp.json` | SQLite / API / Neo4j 是否需要 MCP 尚未成型 | `no-op` | 暂不新增 MCP | 只有真实需要外部工具接入时再设计 `.mcp.json` | 为了配置完整而新增 MCP 会引入密钥和环境变量边界 |
| `.codex/rules` 中有偏 Agent runtime 的重型输出契约规则 | `.codex/rules/*.rules` | 本项目主要是知识库维护，typed output / backend-owned 字段只在工具或未来 Agent 流程中适用 | `merge` | 常驻 rules 保留触发入口；知识库维护细节放 skill | 配置审计重复词下降；Wiki 任务触发专用 skill | 不收口会让普通 Markdown 维护任务背负过多工程后端约束 |

## 建议落地顺序

1. 先填项目覆盖层。`AGENTS.override.md` 与 `CLAUDE.project.md` 至少写入：项目名、目标、关键模块、必读文档、Markdown 主数据源不变量、派生产物边界、验证命令、环境边界、私有配置边界。
2. 统一 Python 工具入口。建议把项目实际验证命令统一为 `.venv/bin/python ...`，依赖安装统一为 `uv pip install -r tools/requirements.txt`；如果保留 `pip`，应在覆盖层声明这是项目例外。
3. 新增 Wiki 维护 skill。Codex 与 Claude 各自保留同名语义的 skill，内容聚焦：读取顺序、模板选择、实体拆分、双链、证据、变更日志、结构化抽取影响。
4. 再补确定性校验脚本。优先检查 Markdown 结构，而不是一开始写 hook。脚本稳定后再决定是否接 Codex / Claude hooks 或 CI。
5. 最后评估 MCP。如果 API 服务、SQLite 或 Neo4j 图查询需要被 Agent 直接调用，再设计 `.mcp.json`，并用环境变量承载 URL、账号和密钥。

## 覆盖层建议内容要点

`AGENTS.override.md` 与 `CLAUDE.project.md` 建议保持语义一致，但按各自平台写法组织：

- 项目名称：`Windows应用安全基线画像库`。
- 主要目标：维护面向人和 AI 的 Windows 应用、服务、进程、父子关系、注册表、文件、网络和安全基线 Markdown Wiki，并可抽取为 SQLite、Neo4j、API 检索数据。
- 关键模块：`00_总览/`、`01_应用/`、`02_服务/`、`03_进程/`、`04_父子进程关系/`、`09_安全基线/`、`10_来源与证据/`、`11_抽取与图谱/`、`99_模板/`、`tools/`。
- 必读文档：`README.md`、`Windows应用安全基线画像库 AI 维护规范.md`、`00_总览/维护工作流.md`、相关类型模板、相关实体页面、`logs/变更日志.md`。
- 产品不变量：Markdown / Obsidian 是正式知识源；`out/` 中 SQLite、JSONL、Cypher 是派生产物；安全判断不得无来源升级为恶意结论；重要判断需要证据与可信度。
- 兼容边界：允许调整 Markdown 模板和抽取脚本，但改变 frontmatter 字段、`type` 枚举、目录结构或 API 输出时必须同步 README、抽取规范和示例数据。
- 验证入口：配置 `.venv` 后运行 SQLite 构建、Neo4j Cypher 生成、关键 API smoke；新增校验脚本后作为完整硬门。
- 环境边界：真实密钥、Neo4j 密码、私有 MCP header、本机路径和本地 Claude 设置不得提交。

## 建议验证命令

短期可用的验证命令：

```bash
uv venv .venv
uv pip install -r tools/requirements.txt

.venv/bin/python tools/kb_to_sqlite.py \
  --vault . \
  --out out/windows_app_baseline.db \
  --rebuild \
  --export-jsonl out/documents.jsonl \
  --debug \
  --log-file logs/kb_to_sqlite.debug.log

.venv/bin/python tools/kb_to_neo4j.py \
  --vault . \
  --out out/windows_app_baseline.cypher \
  --debug \
  --log-file logs/kb_to_neo4j.debug.log

.venv/bin/python .codex/skills/codex-config-optimizer/scripts/audit_codex_config.py
```

API 服务 smoke 在需要启动服务时再运行：

```bash
.venv/bin/python tools/api_service.py \
  --db out/windows_app_baseline.db \
  --host 127.0.0.1 \
  --port 8000 \
  --debug \
  --log-file logs/api_service.debug.log
```

服务启动后检查：

```bash
curl "http://127.0.0.1:8000/health"
curl "http://127.0.0.1:8000/stats"
curl "http://127.0.0.1:8000/search?q=chrome&mode=fuzzy&limit=5"
```

## 不建议现在做的事

- 不建议把 `Windows应用安全基线画像库 AI 维护规范.md` 全量复制进 `AGENTS.md` 或 `CLAUDE.md`。保留引用即可。
- 不建议现在启用 Codex / Claude hooks。先有稳定校验脚本，再接生命周期阻断。
- 不建议为了“配置完整”新增 `.mcp.json`。MCP 应服务真实工具调用需求。
- 不建议把个人模型、账号、私有路径、本地服务 URL 或真实 Neo4j 密码写入项目配置。
- 不建议把 SQLite、Cypher 或 JSONL 当作正式源直接编辑。

## 下一步实施清单

- 填写 `AGENTS.override.md` 与 `CLAUDE.project.md`，清除模板占位。
- 新增 Codex 与 Claude 的 Wiki 维护 skill。
- 统一 Python 环境入口和工具文档。
- 补充 `.gitignore` 的 Claude 本地私有配置规则。
- 设计并实现 Markdown 知识库校验脚本。
- 脚本稳定后，再评估是否接入 hooks 或 CI。
