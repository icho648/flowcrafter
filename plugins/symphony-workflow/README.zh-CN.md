# symphony-workflow

一个用于审计仓库本地 Agent Harness、将模糊意图收敛为最小 Issue 结构，
并把 Pull Request 推进到可合并状态的 Claude Code 与 Codex 插件。

## 包含的 Skill

- harness-audit：审计、初始化、检查、编码和整理项目指南、证据、链接、
  新鲜度与反馈闭环。
- intent-to-issues：判断目标是否需要拆解，生成最小的 Parent/Sub-issue 草案，
  并在写入 GitHub Issues 前征得确认。
- autopilot：持续处理当前 Pull Request 的冲突、Review thread 和 CI 阻塞，
  直到达到可合并状态。

三个 Skill 都采用显式调用，避免普通实现或规划工作无意触发审计、Issue 写入或
PR 自动化。

## 安装

    codex plugin marketplace add icho648/flowcrafter
    codex plugin add symphony-workflow@flowcrafter

Claude Code：

    claude plugin marketplace add icho648/flowcrafter
    claude plugin install symphony-workflow@flowcrafter

Codex 使用 $harness-audit、$intent-to-issues 和 $autopilot 调用；Claude Code
使用 /symphony-workflow:harness-audit、/symphony-workflow:intent-to-issues 和
/symphony-workflow:autopilot。

## 许可

MIT。见 LICENSE。
