---
type: readme
project: Windows应用安全基线画像库
version: 0.1.0
status: draft
created: 2026-06-11
maintainer: security-baseline-team
tags:
  - windows/app-baseline
  - llm-wiki
  - obsidian
  - security-knowledge-base
---

# Windows应用安全基线画像库

> 一套面向人和 AI 共同维护的 Windows 应用 / 服务 / 进程 / 行为 / 安全基线画像库。
>
> 它不是一次性的 Excel 表，也不是最终数据库；它是一个可持续演化的 Markdown Wiki 中间层，最终可以被抽取为结构化数据、规则库、知识图谱、威胁分析系统的长期知识资产。

---

## 1. 需求背景

在 Windows 终端安全分析中，我们经常会遇到这些问题：

- 某个服务名是否常见？
- 某个进程属于哪个应用？
- 某个应用正常会启动哪些服务？
- 某个服务的启动参数是否正常？
- 某个进程拉起某个子进程，是正常插件行为，还是攻击链迹象？
- 某个进程访问注册表、文件、网络目标，是否符合应用基线？
- 一个看似可疑的行为，在具体业务环境里是否可能是正常误报？

传统做法通常是维护一张或多张表：

```text
应用清单
服务清单
进程清单
父子进程关系清单
注册表行为清单
文件行为清单
网络行为清单
```

但一旦进入真实终端环境，表格很快会遇到限制：

- 字段不断膨胀；
- 一个单元格里塞入多个路径、多个参数、多个上下文；
- 证据、解释、误报条件、版本差异很难表达；
- 人能看懂的分析过程和机器能抽取的结构化字段很难兼顾；
- AI 很难知道哪些文件该读、如何更新、如何保持一致。

因此，本项目采用 **Markdown + Obsidian 双链 + YAML Frontmatter + AI 维护规范** 的方式，先构建一个可读、可查、可演化、可抽取的中间知识层。

---

## 2. 核心理念

本库充分吸收 “LLM Wiki” 的思想：

> 不只是把原始资料丢给检索系统，而是让 LLM 持续构建和维护一个持久化、结构化、互相链接的 Markdown Wiki。

本库采用三层结构：

```text
raw_sources/              原始资料层：只追加，不轻易改写
wiki markdown pages       画像知识层：AI 和人共同维护的结构化 Wiki
AGENTS.md / 模板 / 规范    维护约束层：告诉 AI 如何读、写、更新、抽取
```

这个思路对应到 Windows 安全基线场景就是：

```text
原始来源：终端扫描、EDR、Sysmon、服务注册表、官方文档、人工分析
    ↓
AI 归纳：应用画像、服务画像、进程画像、行为画像、安全基线
    ↓
人类审核：补充误报条件、业务上下文、可信路径、版本差异
    ↓
结构化抽取：JSON / CSV / SQLite / Neo4j / STIX 扩展知识库
```

---

## 3. 为什么对人和 AI 都友好

### 3.1 对人友好

- 每个应用、服务、进程、关系都是独立 Markdown 页面；
- 可以在 Obsidian 中使用 `[[双链]]` 浏览关系；
- 可以按目录、标签、索引、反向链接理解知识网络；
- 可以在正文中保留解释、判断、误报条件、样例和证据；
- 不要求一开始就把字段设计到完美。

### 3.2 对 AI 友好

- 所有文档都有稳定的 `type`；
- 关键字段进入 YAML Frontmatter，便于抽取；
- 标题结构固定，便于增量更新；
- 实体关系用 Obsidian 链接表达，便于转图谱；
- `AGENTS.md` 明确了 AI 的维护规则、更新流程、禁止事项；
- `99_模板/` 提供统一写作骨架；
- `11_抽取与图谱/` 提供结构化抽取路径。

---

## 4. 目标

本项目的第一阶段目标不是追求“列全所有应用”，而是建立可持续扩展的画像体系。

### 4.1 短期目标

- 建立 Windows 应用安全画像的 Obsidian Vault；
- 建立应用、服务、进程、父子进程关系、安全基线五类核心文档；
- 提供可复用模板；
- 提供 Google Chrome、Office、AnyDesk、Docker Desktop、Microsoft Defender 等样例；
- 提供 AI 维护规则；
- 提供后续转结构化数据的抽取约定。

### 4.2 中期目标

- 扩展常见应用画像：浏览器、办公、远控、VPN、云盘、安全软件、数据库、开发工具、驱动软件；
- 沉淀常见服务名、服务参数、进程参数、子进程关系；
- 沉淀注册表、文件、网络、数据资产画像；
- 建立“正常 / 少见 / 可疑 / 高危”的安全基线分层；
- 将企业真实观测事件映射到画像库。

### 4.3 长期目标

- 从 Markdown Wiki 自动抽取结构化数据；
- 导入 Neo4j 形成 Windows 应用安全知识图谱；
- 作为威胁分析平台的静态知识基线；
- 支撑误报核验、异常行为解释、持续监测池、回归测试用例生成；
- 形成长期优化迭代的数据资产。

---

## 5. 愿景

本库的愿景是：

> 把 Windows 终端上“看起来杂乱无章”的应用、服务、进程和行为，整理成一套可被人理解、可被 AI 维护、可被系统消费的安全基线知识网络。

最终它应该成为威胁分析系统中的“常识层”：

```text
这是什么应用？
这个服务正常吗？
这个启动参数常见吗？
这个父子进程关系危险吗？
这个注册表写入属于安装、更新，还是持久化？
这个网络连接是更新、同步、遥测，还是异常外联？
```

它不是替代检测规则，而是帮助检测规则和智能体更准确地理解上下文。

---

## 6. 目录说明

```text
00_总览/                 全局地图、分类索引、维护说明
01_应用/                 应用画像，例如 Google Chrome、Microsoft Office
02_服务/                 Windows Service 画像，例如 gupdate、WinDefend
03_进程/                 进程画像，例如 chrome.exe、winword.exe
04_父子进程关系/          父子进程关系画像，例如 winword.exe -> powershell.exe
05_启动方式/              服务、计划任务、Run Key、驱动等启动方式
06_注册表画像/            高价值注册表路径画像
07_文件与数据/            文件路径、数据资产、缓存、配置、日志
08_网络行为/              域名、端口、协议、用途、异常条件
09_安全基线/              可疑行为、误报条件、检测建议
10_来源与证据/            来源记录、证据样例、观测事件
11_抽取与图谱/            转 JSON、CSV、Neo4j、STIX 的说明
99_模板/                 应用、服务、进程、关系等模板
raw_sources/             原始来源材料，只追加，不轻易改写
logs/                    维护日志、变更日志、待办事项
```

---

## 7. 文档类型设计

核心文档类型如下：

| type | 目录 | 说明 |
|---|---|---|
| `app` | `01_应用/` | 应用实体画像 |
| `service` | `02_服务/` | Windows 服务画像 |
| `process` | `03_进程/` | 进程实体画像 |
| `process_relation` | `04_父子进程关系/` | 父子进程关系画像 |
| `startup_method` | `05_启动方式/` | 启动方式画像 |
| `registry_pattern` | `06_注册表画像/` | 注册表位置画像 |
| `file_artifact` | `07_文件与数据/` | 文件 / 数据资产画像 |
| `network_behavior` | `08_网络行为/` | 网络行为画像 |
| `security_baseline` | `09_安全基线/` | 安全判断基线 |
| `source_evidence` | `10_来源与证据/` | 来源和证据 |
| `extract_spec` | `11_抽取与图谱/` | 抽取和图谱规范 |

---

## 8. 实践指南

### 8.1 新增一个应用画像

1. 从 `99_模板/应用画像模板.md` 复制；
2. 放到 `01_应用/应用名.md`；
3. 填写 YAML 字段；
4. 补充常见服务、进程、启动方式；
5. 建立 `[[服务]]`、`[[进程]]`、`[[父子进程关系]]` 链接；
6. 在 `00_总览/应用分类索引.md` 中增加入口；
7. 在 `logs/变更日志.md` 中记录变更。

### 8.2 新增一个服务画像

1. 从 `99_模板/服务画像模板.md` 复制；
2. 放到 `02_服务/ServiceName.md`；
3. 重点填写 `service_name`、`display_name`、`image_path_pattern`、`start_account`；
4. 链接所属应用和服务启动的进程；
5. 记录正常启动参数和异常关注点。

### 8.3 新增一个父子进程关系

父子进程关系必须单独建文档，因为很多安全判断属于“关系”，而不是单个进程。

例如：

```text
winword.exe 正常
powershell.exe 正常
但 winword.exe -> powershell.exe 这个关系需要高关注
```

新增步骤：

1. 从 `99_模板/父子进程关系模板.md` 复制；
2. 放到 `04_父子进程关系/父进程 -> 子进程.md`；
3. 标记 `normality`、`risk_level`、`attack_techniques`；
4. 补充正常条件、异常条件、误报条件、需要补充的证据；
5. 链接到对应安全基线。

### 8.4 从终端观测数据更新画像

建议流程：

```text
采集原始事件
  ↓
放入 raw_sources/ 或 10_来源与证据/
  ↓
AI 摘要和归类
  ↓
更新对应画像页面
  ↓
新增或修正安全基线
  ↓
人工审核
  ↓
记录 logs/变更日志.md
```

---

## 9. 命名规范

### 9.1 文件命名

```text
应用：Google Chrome.md
服务：gupdate.md
进程：chrome.exe.md
关系：winword.exe -> powershell.exe.md
注册表：HKLM_SYSTEM_CurrentControlSet_Services.md
安全基线：Office拉起脚本解释器.md
```

### 9.2 链接规范

统一使用 Obsidian 双链：

```markdown
所属应用：[[Google Chrome]]
相关服务：[[gupdate]]、[[gupdatem]]
相关进程：[[chrome.exe]]、[[GoogleUpdate.exe]]
父子关系：[[services.exe -> GoogleUpdate.exe]]
安全基线：[[更新器外联行为]]
```

### 9.3 标签规范

建议标签形态：

```text
app/browser
app/office
app/remote-control
service/update
service/security
process/browser
relation/process-spawn
risk/high
vendor/google
windows/service
```

---

## 10. 安全判断分层

建议使用四级：

| normality | 含义 | 说明 |
|---|---|---|
| `normal` | 正常 | 符合常见应用行为 |
| `rare` | 少见 | 不是默认恶意，但需要上下文 |
| `suspicious` | 可疑 | 需要关联证据判断 |
| `malicious_like` | 类恶意 | 行为形态高度接近攻击链 |

风险等级使用：

```text
low / medium / high / critical
```

注意：

> 本库不建议仅凭单点行为直接定恶意。安全判断必须尽量表达上下文、误报条件和证据需求。

---

## 11. 推荐的最小闭环

第一阶段先跑通这一条链：

```text
应用 -> 服务 -> 进程 -> 父子关系 -> 安全基线 -> 证据样例
```

示例：

```text
[[Google Chrome]]
  -> [[gupdate]]
  -> [[GoogleUpdate.exe]]
  -> [[services.exe -> GoogleUpdate.exe]]
  -> [[更新器外联行为]]

[[Microsoft Office]]
  -> [[winword.exe]]
  -> [[winword.exe -> powershell.exe]]
  -> [[Office拉起脚本解释器]]
```

等这条链稳定后，再扩展注册表、文件、网络、驱动、计划任务。

---

## 12. 结构化抽取方向

本库的 Markdown 页面可以后续抽取为：

```text
YAML Frontmatter -> 实体属性
Obsidian Links -> 图谱边
固定标题正文 -> 长文本字段
代码块样例 -> evidence / example
标签 -> 分类和筛选字段
```

可转换为：

```text
CSV
JSON
SQLite
Neo4j
STIX 扩展知识库
威胁分析系统内置基线
```

详见：

- [[Markdown到结构化数据抽取规范]]
- [[Obsidian链接到知识图谱映射]]
- [[Windows应用画像到威胁分析系统映射]]

---

## 13. AI 协作方式

请让 AI 优先读取：

1. `README.md`
2. `AGENTS.md`
3. `00_总览/Windows应用安全基线画像库总览.md`
4. 相关模板
5. 相关实体页面

AI 的任务不是“自由发挥写文章”，而是作为一个受约束的 Wiki 维护者：

- 不随意删除旧判断；
- 新增知识必须注明来源或标记为待验证；
- 不确定时使用 `confidence: low`；
- 不把攻击行为误写成必然恶意；
- 优先保留误报条件和证据需求；
- 维护双链关系和索引。

---

## 14. 推荐工作流

### 14.1 人工新增知识

```text
发现一个常见应用/服务
  ↓
创建画像页面
  ↓
补充基础字段和说明
  ↓
链接服务、进程、关系、安全基线
  ↓
标记置信度
  ↓
进入待审核
```

### 14.2 AI 增量维护

```text
读取新增来源
  ↓
总结可沉淀知识
  ↓
更新相关页面
  ↓
新增必要链接
  ↓
标记证据来源
  ↓
输出变更摘要
  ↓
等待人工审核
```

### 14.3 转结构化数据

```text
扫描 Markdown 文件
  ↓
解析 YAML Frontmatter
  ↓
抽取 Obsidian 链接
  ↓
生成 JSON / CSV
  ↓
导入 Neo4j 或安全平台
```

---

## 15. 维护原则

### 15.1 原始资料不可轻易改写

`raw_sources/` 中的原始材料应尽量保持原貌。

### 15.2 Wiki 页面可以演化

画像页面是知识沉淀层，可以更新、合并、拆分，但必须在变更日志中记录。

### 15.3 证据优先

任何重要判断都应尽量记录来源：

```text
官方文档
终端观测
EDR 事件
Sysmon 事件
注册表导出
人工分析
```

### 15.4 关系优先

安全判断往往不在单个实体上，而在关系上：

```text
谁启动了谁
谁访问了什么
谁连接了哪里
谁修改了哪个持久化位置
```

### 15.5 允许不完整，但不允许假装完整

不确定的字段可以留空或标记：

```yaml
confidence: low
status: needs_review
```

---

## 16. 下一步建议

建议优先补全以下类别：

```text
浏览器：Chrome / Edge / Firefox / Brave
办公：Office / WPS / Adobe Reader / Foxit
远控：AnyDesk / TeamViewer / ToDesk / RustDesk / 向日葵
VPN：OpenVPN / WireGuard / GlobalProtect / Cisco AnyConnect / Tailscale / ZeroTier
安全：Microsoft Defender / CrowdStrike / SentinelOne / 火绒 / 360 / Wazuh / Splunk Forwarder
开发：Docker Desktop / WSL / VMware / VirtualBox / JetBrains / VS Code
数据库：SQL Server / MySQL / PostgreSQL / MongoDB / Redis / Elasticsearch
硬件驱动：NVIDIA / AMD / Intel / Realtek / Dell / Lenovo / HP
```

---

## 17. 本包内容说明

本 starter kit 已包含：

- README.md：需求、背景、理念、目标、愿景、实践指南；
- AGENTS.md：AI 维护规范；
- 总览和索引；
- 核心模板；
- 多个样例应用、服务、进程、父子关系、安全基线；
- 抽取和图谱映射说明；
- 变更日志和待办事项。

你可以直接把整个目录作为 Obsidian Vault 打开。

---

# CLI / API 工具集

本画像库已内置 `tools/` 工具集，用于把 Markdown Wiki 中间产物进一步转成结构化数据、图数据和检索服务。

## 一、Markdown 转 SQLite

用途：把 Obsidian/Markdown 画像库转为结构化 SQLite 数据，适合统计、检索、API 服务、后续落库。

```bash
pip install -r tools/requirements.txt
python tools/kb_to_sqlite.py \
  --vault . \
  --out out/windows_app_baseline.db \
  --rebuild \
  --debug \
  --log-file logs/kb_to_sqlite.debug.log
```

输出核心表：

```text
documents          Markdown 文档主表
entities           应用/服务/进程/安全基线等实体视图
sections           标题章节抽取结果
links              Obsidian [[双链]] 关系
frontmatter_kv     YAML frontmatter 展开表
tags               标签表
documents_fts      SQLite FTS5 全文索引
metadata           构建元数据
```

## 二、Markdown 转 Neo4j

用途：把 Obsidian 双链转为 Neo4j 图数据，适合关系查询、路径分析、知识图谱可视化。

默认生成 Cypher 文件：

```bash
python tools/kb_to_neo4j.py \
  --vault . \
  --out out/windows_app_baseline.cypher \
  --debug \
  --log-file logs/kb_to_neo4j.debug.log
```

也可以直连 Neo4j 执行：

```bash
python tools/kb_to_neo4j.py \
  --vault . \
  --out out/windows_app_baseline.cypher \
  --execute \
  --uri bolt://localhost:7687 \
  --user neo4j \
  --password password \
  --database neo4j \
  --debug
```

图模型默认采用：

```text
(:KbDocument:App)
(:KbDocument:Service)
(:KbDocument:Process)
(:KbDocument:ProcessRelation)
(:KbDocument:SecurityBaseline)
(:KbDocument)-[:LINKS_TO]->(:KbDocument)
```

## 三、API 检索服务

用途：基于 SQLite 提供 HTTP API，支持全匹配、模糊匹配、FTS 全文检索和 LIKE 检索。

```bash
python tools/api_service.py \
  --db out/windows_app_baseline.db \
  --host 0.0.0.0 \
  --port 8000 \
  --debug \
  --log-file logs/api_service.debug.log
```

常用接口：

```text
GET /health
GET /stats
GET /search?q=chrome&mode=fuzzy&limit=20
GET /search?q=Google%20Chrome&mode=exact&type=app
GET /search?q=chrome&mode=fts
GET /documents/{doc_id}
```

检索模式：

```text
exact   全匹配：title/name/path/service_name/process_name/vendor/type
fuzzy   模糊匹配：title/name/path/body_text
fts     SQLite FTS5 全文检索
like    SQL LIKE 包含匹配
```

## 四、调试日志

所有工具都支持：

```bash
--debug
--log-file logs/xxx.debug.log
```

推荐在每次批量构建时保留日志，便于排查：

```text
解析了哪些 Markdown 文件
frontmatter 是否解析成功
抽取了多少章节
抽取了多少 Obsidian 双链
哪些链接被解析成功
哪些链接成为 unresolved target
SQLite FTS 是否创建成功
Neo4j Cypher 是否生成成功
API 每次检索的 SQL、参数和结果数量
```

## 五、主数据原则

正式维护时仍应遵循：

```text
Markdown / Obsidian 是主数据源
SQLite 是检索和统计派生产物
Neo4j 是关系分析派生产物
API 服务读取 SQLite，不直接修改 Markdown
```

也就是说，知识修订应先回到 Markdown，再重新构建 SQLite / Neo4j。
