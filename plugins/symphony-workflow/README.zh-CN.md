# symphony-workflow

一个用于审计仓库本地 Agent Harness，并编码最小有效工作流护栏的
Claude Code 与 Codex 插件。

## 包含的 Skill

- harness-audit：审计、初始化、检查、编码和整理项目指南、证据、链接、
  新鲜度与反馈闭环。

该 Skill 采用显式调用，避免在普通实现工作中无意触发 Harness 审计。

## 安装

    codex plugin marketplace add icho648/flowcrafter
    codex plugin add symphony-workflow@flowcrafter

Claude Code：

    claude plugin marketplace add icho648/flowcrafter
    claude plugin install symphony-workflow@flowcrafter

Codex 使用 $harness-audit 调用该 Skill；Claude Code 使用
/symphony-workflow:harness-audit。

## 许可

MIT。见 LICENSE。
