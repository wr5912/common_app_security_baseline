# .codex 分层说明

本目录保存团队通用 Codex 模板。复制到其他项目时，通用层只承载团队统一工作方式、环境硬约束和可迁移治理规则；项目专属路径、脚本、CI、base-ref 策略、端口、运行态数据路径和产品不变量必须放在目标项目自己的 `AGENTS.override.md`。

## 默认模板内容

- `config.toml`：安全、通用的 Codex 项目配置模板。
- `hooks.json`：默认不启用任何 hook；各项目自行接入真实存在的治理命令。
- `rules/project.rules`：规则入口和执行顺序。
- `rules/architecture.rules`：通用架构卫生阈值。
- `rules/verify.rules`：通用验证要求。
- `skills/project-skill/SKILL.md`：团队开发通用技能。
- `skills/codex-config-optimizer/SKILL.md`：Codex 配置治理和删重流程。
- `agents/worker.toml`：通用项目 worker 画像。

## 可选 Overlay

`../overlays/agent-runtime/` 是后台 Agent / AI workflow runtime 类项目的可选配置增量包，不属于默认启用内容。只有目标项目确实存在后台 Agent、worker、结构化 AI 输出、多运行模式或模型凭据边界时，才按需复制其中的 skill、hook wrapper 和覆盖层片段。

可选 overlay 不得使用任何具体项目名称、私有路径或原项目治理脚本。合并后必须改成目标项目真实存在的命令、路径和环境变量。

## 通用质量优先策略

通用层包含“替换旧设计模式”：当用户要求重构、去除旧设计、优化架构、提高代码质量，或 Analyze 阶段发现旧 facade、兼容 shim、历史路径、重复实现、schema 双轨、状态分散、过期 API、不可达分支等旧债信号时，默认优先级为代码质量 > 新设计/框架/架构 > 旧模式兼容或保留。

涉及 AI / 自动化输出契约、结构化输出、用户可见工作流、API/schema 生成物或后台任务时，通用层只保留字段所有权和边界验证入口；项目具体框架、job 类型、测试命令和生成物路径必须放入项目覆盖层或按需 skill。

`.codex` 不存放项目债务账本。旧债如需人工跟踪，应放在普通 docs 或 issue；可机械判定的检查应进入项目治理脚本、hook 或 CI。

## 复用要求

- 新项目应重新填写自己的 `AGENTS.override.md`，声明治理命令、CI base-ref 策略、产品不变量、环境边界和持久化路径。
- 新项目必须保留团队统一环境硬约束：`.venv`、`uv`、`pnpm`、Python 3.10+、Node.js 20+、国内下载源和 Docker 目录规范。
- 默认模板不得硬编码项目私有脚本名、CI workflow、端口、volume 路径、API key 名称或产品不变量。
- Hook 默认关闭；只有目标项目已经提供稳定、无交互、可重复运行的治理命令时，才在目标项目中启用。
