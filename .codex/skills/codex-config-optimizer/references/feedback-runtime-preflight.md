# 反馈闭环与 Runtime 短预检

用于用户可见反馈闭环、runtime/env、后台任务、结构化 AI 输出、回归资产和产品主流程问题。目标是在改代码前用 5 行固定证据链和验证点，避免把常驻规则继续写长。

## 五行预检

```text
1. 用户动作/对象：批次、反馈、页面动作、后台任务或运行模式是什么；用户期望的可见结果是什么。
2. 证据链：UI state -> API response -> task/job state -> data projection -> structured output -> persisted payload 中当前卡在哪一层。
3. 所有权：backend-owned、agent-owned、boundary-owned 字段分别是什么；LLM 不应输出哪些后端权威字段。
4. 契约词表：涉及的 status、task_type、profile、target_type、problem_type、actionability 是否来自现有 typed schema 或集中注册表。
5. 验证绑定：目标 pytest、UI verification 或主流程测试是什么；是否需要同步项目覆盖清单或 manifest。
```

## 使用规则

- 如果只是当前线程的一次性问答，不需要写文件，预检可以口头完成。
- 如果要改反馈闭环、后台任务、formatter、数据投影、runtime/env 或用户可见 UI 状态，必须先填完五行预检再改代码。
- 如果第 4 行发现需要新增枚举或状态，先回到 schema/状态机设计，不能在测试桩或局部实现里自造字符串。
- 如果第 5 行找不到现有覆盖，先补目标测试或覆盖清单场景，再确认实现。
