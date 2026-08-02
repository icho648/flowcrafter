# rit-plugin

Rit's personal Claude Code and Codex workflow bundle.

## Included skills

- `grounded-explainer` — explicitly invoked, evidence-grounded technical explanation with concrete scenarios and proportional depth.
- `learn` — maintain evidence-based learning state through real practice.

Grouped as one personal workflow set so they install and version together; each skill remains independently usable. The PRD delivery workflow is separately installable as `prd-workflow`.

## Install

```bash
codex plugin marketplace add icho648/flowcrafter
codex plugin add rit-plugin@flowcrafter
```

For Claude Code:

```bash
claude plugin marketplace add icho648/flowcrafter
claude plugin install rit-plugin@flowcrafter
```

Codex invokes the skills as `$grounded-explainer` and `$learn`. Claude Code uses `/rit-plugin:<skill-name>`.

## License

MIT. See [LICENSE](LICENSE).
