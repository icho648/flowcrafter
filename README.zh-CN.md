# Flowcrafter

[![validate skills](https://github.com/icho648/flowcrafter/actions/workflows/validate.yml/badge.svg)](./.github/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-1.0-blue)](https://agentskills.io/specification)

[English](README.md)

一个托管精心打磨的 Agent 工作流的 Claude Code 与 Codex Marketplace。添加一次 `flowcrafter`，然后按需安装 Rit 的个人工作流插件、PRD 交付插件、Symphony Workflow 插件，或任意组合。

## 插件

| 插件 | 包含的 Skills | 边界 |
| --- | --- | --- |
| [rit-plugin](plugins/rit-plugin/) | `grounded-explainer`、`learn`、`change-report` | Rit 的解释、学习和确定性变更报告工作流共用一个个人插件包。 |
| [prd-workflow](plugins/prd-workflow/) | `write-prd`、`implement-prd`、`review-prd-implementation` | 实施对审阅闭环存在硬依赖，因此 PRD Skills 一起安装。 |
| [symphony-workflow](plugins/symphony-workflow/) | `harness-audit`、`intent-to-issues`、`autopilot` | 项目本地 Agent Harness 审计、最小 Issue 规划与推进 PR 可合并。 |

GitHub 仓库名与 Marketplace ID 都是 `flowcrafter`。

## 安装

### Codex

```bash
codex plugin marketplace add icho648/flowcrafter
codex plugin add rit-plugin@flowcrafter
codex plugin add prd-workflow@flowcrafter
codex plugin add symphony-workflow@flowcrafter
```

可以只安装一个插件，也可以按需组合安装。安装后新建 Codex 任务，使其发现所选 Skills。

### Claude Code

```bash
claude plugin marketplace add icho648/flowcrafter
claude plugin install rit-plugin@flowcrafter
claude plugin install prd-workflow@flowcrafter
claude plugin install symphony-workflow@flowcrafter
```

安装后重启 Claude Code。Claude Code 使用带命名空间的调用，例如 `/rit-plugin:learn` 和 `/prd-workflow:write-prd`；Codex 对同一 Skills 使用 `$learn` 和 `$write-prd`。

### 从 `icho648-skills` 迁移

旧 Marketplace ID 和一体化插件由 `flowcrafter` 与聚焦插件取代：

```bash
# Codex
codex plugin remove icho648-plugin@icho648-skills
codex plugin marketplace remove icho648-skills
codex plugin marketplace add icho648/flowcrafter
codex plugin add rit-plugin@flowcrafter
codex plugin add prd-workflow@flowcrafter
codex plugin add symphony-workflow@flowcrafter
```

```bash
# Claude Code
claude plugin uninstall icho648-plugin@icho648-skills
claude plugin marketplace remove icho648-skills
claude plugin marketplace add icho648/flowcrafter
claude plugin install rit-plugin@flowcrafter
claude plugin install prd-workflow@flowcrafter
claude plugin install symphony-workflow@flowcrafter
```

未安装的旧项目可以跳过对应的移除命令。

### 手动安装 Skill

每个 `plugins/<plugin>/skills/<skill>/` 目录都是便携 Agent Skills 包。克隆仓库后，把所需 Skill 复制或软链到 `$HOME/.claude/skills/` 或 `$HOME/.agents/skills/`。

手动安装 `implement-prd` 时还必须安装 `review-prd-implementation`，因为审阅闭环是硬依赖。

## 仓库结构

```text
.
├── .claude-plugin/marketplace.json       # Claude Code Marketplace
├── .agents/plugins/marketplace.json      # Codex Marketplace
├── plugins/
│   ├── rit-plugin/
│   │   └── skills/
│   │       ├── grounded-explainer/
│   │       ├── learn/
│   │       └── change-report/
│   ├── prd-workflow/
│   │   └── skills/
│   │       ├── write-prd/
│   │       ├── implement-prd/
│   │       └── review-prd-implementation/
│   └── symphony-workflow/
│       └── skills/
│           ├── harness-audit/
│           ├── intent-to-issues/
│           └── autopilot/
├── .github/                              # 校验与发布工作流
├── tests/                                # 校验器回归测试
└── AGENTS.md                             # Marketplace 维护策略
```

每个插件分别包含 `.claude-plugin/plugin.json` 与 `.codex-plugin/plugin.json`，规范 Agent Skills 位于其 `skills/` 目录。

## 兼容模型

- Claude Code Marketplace 与插件清单负责 Claude 分发和命令命名空间。
- Codex Marketplace 与插件清单负责 Codex 分发和呈现元数据。
- 每个 `skills/<name>/` 目录遵循跨客户端 Agent Skills 包结构，也可以绕过插件外壳单独安装。

## 维护原则

- 把 Plugin 作为安装、版本和依赖边界。
- 同步维护 Claude Code 与 Codex 的 Marketplace 条目和 manifests。
- 存在硬依赖的 Skills 放在同一个 Plugin。
- 英文与简体中文资源对保持语义同步。

## 校验

```bash
for skill in plugins/*/skills/*; do
  python -m skills_ref.cli validate "$skill"
done

for plugin in plugins/*; do
  python ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py "$plugin"
done

python .github/scripts/validate_repository.py
python -m unittest tests/test_validate_repository.py
```

GitHub Actions 会在 push 与 pull request 时执行同样的仓库、Skill、Marketplace 与 Plugin 校验。

## 参考

- [Claude Code 插件](https://code.claude.com/docs/zh-CN/plugins)
- [Claude Code 插件市场](https://code.claude.com/docs/zh-CN/plugin-marketplaces)
- [Agent Skills 规范](https://agentskills.io/specification)
- [Codex 定制与技能](https://developers.openai.com/codex/concepts/customization#skills)

## 许可

MIT。见 [LICENSE](LICENSE)。
