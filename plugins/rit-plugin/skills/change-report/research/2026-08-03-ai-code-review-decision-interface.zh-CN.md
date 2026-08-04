# AI 代码 Review 人类决策界面研究快照

> 核验日期：2026-08-03
>
> 研究问题：AI 产码速度超过人类逐行审查能力后，什么信息架构最能帮助人快速、可靠地作出 Review 决策？
>
> 状态：设计研究，不自动成为产品决定；实际效率与准确性仍未验证。
>
> 使用边界：只供 Skill 与模板设计时查阅，不得把本文的方法论、研究结论或示例文案渲染进实际 Review 报告。

## 结论

最高效的首屏不是更漂亮的 Diff Viewer，也不是更短的 AI 总结，而是一个**人类注意力路由器**：

```text
Task / PR + exact revision + freshness
  → Intent / source
  → Actual behavior / drift
  → Blast radius
  → Evidence / unknowns
  → Top-K human spotlights
  → Change map / anchored diff
  → Human decision
```

模型读取改动和上下文只完成了 Review 的观察阶段。Review 还需要把实际行为与意图、约束和不变量比较，并为风险判断提供可复核证据；批准、拒绝或升级则是人类决定。界面应分别展示“看过什么”“判断了什么”“凭什么判断”和“谁有权决定”，不能把它们折叠成一个绿色 AI 结论。

## 证据综合

- **Observed—实证研究：**一项对 10 名开发者、34 次 Review 的观察与 think-aloud 研究把 Review 描述为先理解理由和上下文、再分析代码、最后投票的决策过程；研究也指出 Diff 中心工具迫使人跨工具补上下文。[Code review as decision-making](https://link.springer.com/article/10.1007/s10664-025-10791-2) Microsoft 的实证研究同样发现，理解代码与变更是 Reviewer 的核心诉求，而既有工具对此支持不足。[Expectations, outcomes, and challenges of modern code review](https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/)
- **Observed—工程实践：**Google 建议先读变更说明并形成整体视图，再从主要部分进入细节；GitHub 则把动机、Checks、文件树、已查看进度和最终 `Comment / Approve / Request changes` 分开呈现。[Google review navigation](https://google.github.io/eng-practices/review/reviewer/navigate.html) · [GitHub reviewing proposed changes](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request?tool=webui)
- **Observed—当前产品文档：**OpenAI Codex Review 会结合声明意图、仓库上下文、测试与引用，但明确把它定位为附加 Reviewer，而非人类替代。[Codex upgrades](https://openai.com/index/introducing-upgrades-to-codex/) OpenAI 的评测审计还采用独立调查者、工程师独立判断、具体证据分级和低信心升级，说明“另一个模型结论”仍需独立判断链。[Separating signal from noise](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)
- **Observed—当前产品文档：**Anthropic Code Review 采用多 Reviewer、行为验证、去重和严重度排序；在 GitHub 中提供摘要、行级定位、可折叠的验证理由，并把 `Important`、`Nit`、`Pre-existing` 分开。其规则建议限制 Nit 数量、跳过 CI 已覆盖事项、提高高风险路径的证据门槛，并保持最终检查结论中立。[Claude Code Review](https://code.claude.com/docs/en/code-review) Anthropic 也建议用新上下文执行 Writer/Reviewer 分工，但这仍是厂商实践建议，不是普适实验结论。[Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- **Preliminary—最直接的界面研究：**2026-07-31 的 ARCTIC 预印本从 18,000 条可行动人类 Review 中提炼主题，并提出 `Intent / Drift / Spotlight`：先展示意图和偏差，再把人导向 Top-K 高风险代码区，完整 Diff 下沉。其人类可行动评论主要落在正确性（44.4%）、可维护性（19.2%）和安全（19.1%），而样本中的 AI 输出明显偏向最佳实践和设计评论。[ARCTIC](https://arxiv.org/html/2607.29516) 该研究来自单一工程环境，使用 LLM-as-judge，线上 rollout 非随机且存在自选择；中间 Drift 档位 F1 仅 0.341 和 0.409，因此 Drift 分数只能导航注意力，不能充当真值或自动放行条件。

## 推荐信息架构

```text
┌ Task / PR · base→head SHA · Review freshness ────────────────┐
│ 意图及来源       │ 实际行为 / 偏离       │ Blast radius      │
├──────────────────── Evidence / Unknowns ─────────────────────┤
│ Tests ✓  CI ✓  Smoke ?  Self-review ✓  Independent review ? │
├────────────────── Top 3 Human Spotlights ────────────────────┤
│ 1. 后果 + 代码位置 + 证据       [查看 Hunk / 上下文]          │
│ 2. 后果 + 代码位置 + 证据       [查看 Hunk / 上下文]          │
│ 3. 必须由人回答的业务问题       [回答 / Escalate]             │
├────────────────────── Change Map ─────────────────────────────┤
│ 行为 → Module → Hunk；完整 Diff、日志、Nits 按需展开          │
└ Approve SHA | Request changes | Escalate | Not ready ────────┘
```

1. **Intent 在 Diff 前。** 首屏先回答为什么改、意图来自哪里、实际行为是否吻合。AI 推断的意图必须标明并允许人修正，否则 Drift 只是模型拿自己的猜测验证自己的总结。
2. **只把 Top-K 风险区域推给人。** Spotlight 按用户后果、跨 Module / 外部 Seam、权限与数据、回滚难度排序，不按文件顺序或增删行数排序。
3. **证据与未知并排。** 明示未读取文件、未运行检查、失败或超时、外部系统未验证、生成代码和排除路径。`No findings` 只能表示“在已检查范围内未产生 Finding”，不能显示为 `Verified`。
4. **Blocking finding 在上，Nits 折叠。** 样式、机械检查、重复项和 CI 已覆盖事项进入次级层；Pre-existing 单列。不得隐藏其他阻断问题。
5. **每条 Finding 都是证据卡。** 至少包含可证伪 Claim、后果、精确 `file:line` 或 Hunk、复现或测试证据、证据状态、Reviewer 来源与独立性，以及仍未覆盖的条件。
6. **不要显示全局安全分数。** 局部标出证据和不确定性；Drift、模型置信度或“92% 安全”都不能替代可复核证据。[Microsoft Research：LLM 搜索与过度依赖](https://www.microsoft.com/en-us/research/publication/effects-of-llm-based-search-on-decision-making-speed-accuracy-and-overreliance/)
7. **完整 Diff 仍保留，但不是首页。** 使用 `决策摘要 → 风险卡 → 概念变更 → Hunk → 全文件 / 原始日志` 的渐进披露，并让每层回到同一 Claim。
8. **Review 绑定精确 Revision。** 显示 base/head SHA；Push 后将旧 Finding、Viewed 进度和批准标记为 stale，再只突出新增风险。GitHub Copilot 文档也明确提示上下文收集可能降级、排除文件应列出且 AI 可能漏报。[GitHub Copilot code review](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/agents/code-review)
9. **决策动作保持中立且归人。** 固定提供 `Approve exact revision`、`Request changes`、`Escalate to owner`、`Not ready / missing evidence`。AI 可以建议下一步，但不是自动批准者。[Running Codex safely](https://openai.com/index/running-codex-safely/)
10. **多改动场景再加 Review Inbox。** Inbox 按“需要人类判断的风险”排序，而不是创建时间或改动行数。这是从风险分层研究和当前实践推导出的设计假设，并非已验证的通用定律。[Addy Osmani：Agentic Code Review](https://addyosmani.com/blog/agentic-code-review/)

## 自审与独立 Review 的边界

生成模型再次读取上下文并自查是有价值的 **self-review**，但不天然独立：它可能继承同一意图误解、遗漏和错误假设。界面应区分 `Author self-review`、`Independent AI review`、`Deterministic check`、`Human review`，而不是把它们合成一个通过状态。

独立 AI Review 最少应使用新的上下文重新建立意图和风险判断；测试、CI、Smoke 与领域 Owner 提供的是不同种类的证据。OpenAI 也要求 Codex 给出测试、日志和引用并沟通不确定性，而非只报告完成。[Introducing Codex](https://openai.com/index/introducing-codex/)

## 设计约束

- Task 及其人类确认意图是 Review 的坐标原点，不以 Agent 或文件列表为起点。
- AI 输出是建议与证据导航，最终决定归人。
- Finding、检查结果、未知和精确 Revision 共同构成可审计决策依据。
- 渐进披露不能隐藏覆盖缺口；“更少信息”必须意味着先展示更高信号的信息，而不是省略未知。
- Review 展示层不因此获得合并、部署、Issue 写回或业务系统写权限。
- 模板只渲染当前变更的数据；不得渲染本研究、设计原则、讨论过程或示例占位文案。

## Not verified

- 尚未用真实任务、Reviewer 和时间数据验证该布局是否比 GitHub 原生 Diff 更快或更准。
- Top-K 的最佳数量、严重度命名、移动端布局和团队差异尚未经过可用性测试。
- ARCTIC 是 2026 年预印本，其单组织 rollout、零归因缺陷和自审路径不能证明普遍安全，也不能支持自动合并。
- 厂商文档证明的是其公开设计与建议，不证明模型在任意仓库中的实际 Review 质量。
- 经验文章关于“人从逐行 Gatekeeper 转向 Why-loop”的观点可用于提出假设，但不是实证结论。[Martin Fowler：Humans and agents](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html) · [Google Cloud CTO viewpoint](https://cloud.google.com/transform/when-ai-writes-the-code-who-reviews-it-cto-google-cloud)
