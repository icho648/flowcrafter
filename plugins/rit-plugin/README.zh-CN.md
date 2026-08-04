# rit-plugin

Rit 的个人 Claude Code 与 Codex 工作流插件包。

## 包含的 Skills

- `grounded-explainer`：仅显式调用，以真实场景和必要证据为基础、按问题深度展开的技术解释。
- `learn`：通过真实练习维护有证据的学习状态。
- `change-report`：把选定 Diff 渲染为确定性的独立 HTML 变更报告。

作为一组个人工作流打包，统一安装与版本；每个 skill 仍可独立使用。PRD 交付工作流仍通过 `prd-workflow` 单独安装。

## 安装

```bash
codex plugin marketplace add icho648/flowcrafter
codex plugin add rit-plugin@flowcrafter
```

Claude Code：

```bash
claude plugin marketplace add icho648/flowcrafter
claude plugin install rit-plugin@flowcrafter
```

Codex 中分别使用 `$grounded-explainer`、`$learn` 和 `$change-report`；Claude Code 使用 `/rit-plugin:<skill-name>`。

## 许可

MIT。见 [LICENSE](LICENSE)。
