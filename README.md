# Flowcrafter

[![validate skills](https://github.com/icho648/flowcrafter/actions/workflows/validate.yml/badge.svg)](./.github/workflows/validate.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-1.0-blue)](https://agentskills.io/specification)

[简体中文](README.zh-CN.md)

A Claude Code, Codex, and Cursor marketplace for crafted Agent workflows. Add `flowcrafter` once, then install Rit’s personal workflow bundle, the PRD delivery workflow, the Symphony Workflow plugin, or any combination.

## Plugins

| Plugin | Included skills | Boundary |
| --- | --- | --- |
| [rit-plugin](plugins/rit-plugin/) | `grounded-explainer`, `learn`, `change-report` | Rit’s explanation, learning, and deterministic change-report workflows share one personal bundle. |
| [prd-workflow](plugins/prd-workflow/) | `write-prd`, `implement-prd`, `review-prd-implementation` | Implementation has a hard dependency on the review loop, so the PRD skills install together. |
| [symphony-workflow](plugins/symphony-workflow/) | `harness-audit`, `intent-to-issues`, `autopilot` | Repo-local Agent Harness auditing, minimal linked Issue planning, and merge-ready PR automation. |

The GitHub repository name and Marketplace ID are both `flowcrafter`.

## Install

### Codex

```bash
codex plugin marketplace add icho648/flowcrafter
codex plugin add rit-plugin@flowcrafter
codex plugin add prd-workflow@flowcrafter
codex plugin add symphony-workflow@flowcrafter
```

Install any plugin or combination. Start a new Codex task afterward so the selected skills are discovered.

### Claude Code

```bash
claude plugin marketplace add icho648/flowcrafter
claude plugin install rit-plugin@flowcrafter
claude plugin install prd-workflow@flowcrafter
claude plugin install symphony-workflow@flowcrafter
```

Restart Claude Code after installation. Claude Code invocations are namespaced, for example `/rit-plugin:learn` and `/prd-workflow:write-prd`; Codex invokes the same skills as `$learn` and `$write-prd`.

### Cursor

Cursor discovers this marketplace through `.cursor-plugin/marketplace.json`. Import the GitHub repository as a Team Marketplace, then install plugins from **Customize**:

1. Open **Cursor Dashboard → Settings → Plugins**.
2. Under **Team Marketplaces**, choose **Import Marketplace** / **Add Marketplace**.
3. Paste `https://github.com/icho648/flowcrafter` and save.
4. Open **Customize** in Cursor and install `rit-plugin`, `prd-workflow`, and/or `symphony-workflow`.

If the marketplace was imported earlier, refresh or update it so Cursor picks up the latest commit (including `symphony-workflow`).

### Migrate from `icho648-skills`

The former Marketplace ID and all-in-one plugin are replaced by `flowcrafter` and focused plugins:

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

Skip any removal command for an item that was not installed.

### Manual skill installation

Each `plugins/<plugin>/skills/<skill>/` directory is a portable Agent Skills package. Clone the repository, then copy or symlink the desired skill into `$HOME/.claude/skills/` or `$HOME/.agents/skills/`.

When installing `implement-prd` manually, also install `review-prd-implementation`; the review loop is a hard dependency.

## Repository layout

```text
.
├── .claude-plugin/marketplace.json       # Claude Code Marketplace
├── .agents/plugins/marketplace.json      # Codex Marketplace
├── .cursor-plugin/marketplace.json       # Cursor Marketplace
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
├── .github/                              # validation and release workflows
├── tests/                                # validator regression tests
└── AGENTS.md                             # Marketplace maintenance policy
```

Each plugin has client-specific manifests in `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and `.cursor-plugin/plugin.json`. Its canonical Agent Skills live under `skills/`.

## Compatibility model

- The Claude Code Marketplace and plugin manifests provide Claude distribution and command namespacing.
- The Codex Marketplace and plugin manifests provide Codex distribution and presentation metadata.
- The Cursor Marketplace and plugin manifests provide Cursor Customize / Team Marketplace distribution.
- Every `skills/<name>/` directory follows the cross-client Agent Skills package structure and can also be installed without the plugin wrapper.

## Maintenance

- Treat a plugin as an install, version, and dependency boundary.
- Keep the Claude Code, Codex, and Cursor marketplace entries and manifests synchronized.
- Keep hard-dependent skills in the same plugin.
- Keep English and Simplified Chinese resource pairs in semantic lockstep.

## Validate

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

GitHub Actions runs the same repository, Skill, Marketplace, and Plugin checks on pushes and pull requests.

## Sources

- [Claude Code plugins](https://code.claude.com/docs/en/plugins)
- [Claude Code plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Agent Skills specification](https://agentskills.io/specification)
- [Codex customization and skills](https://developers.openai.com/codex/concepts/customization#skills)

## License

MIT. See [LICENSE](LICENSE).
