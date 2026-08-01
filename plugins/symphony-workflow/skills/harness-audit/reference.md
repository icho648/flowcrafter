# Harness Audit — Reference

## Article → practice map

From [Harness Engineering](https://openai.com/index/harness-engineering/):

| Article idea | Practice |
|---|---|
| Humans steer; agents execute | Human designs environment + feedback; agent writes code/docs/fixes |
| Repo as system of record | No SoR in chat/Docs/brain; version in Git |
| AGENTS.md as TOC | Short map; progressive disclosure into `docs/` |
| Linters/CI on knowledge | Structure, cross-links, freshness as failing checks |
| Doc-gardening agent | Periodic scan → fix PRs (after checks exist) |
| Agent-readable systems | Logs/UI/checks reachable without human copy-paste |
| Architecture invariants | Allowed dependency edges; structural tests |
| Taste in tools | Review preferences → docs or lint with fix hints |
| Throughput changes merge gates | Only when agent fix cost << wait cost |
| Entropy / GC | Encode golden rules; small continuous cleanup PRs |
| Autonomy is encoded | Tests, review, recovery in-repo unlock E2E agent loops |

## Evidence discipline

Use the strongest label supported by the evidence:

| Label | Use when |
|---|---|
| **Observed** | A file, command result, test, CI run, or human decision directly shows it. |
| **Inferred** | Source or structure supports it, but the behavior was not executed. |
| **Declared** | Documentation states an intent or decision. |
| **Not verified** | Runtime, CI, deployment, credentials, external services, or human acceptance were not checked. |

Do not promote a claim from static evidence to runtime or business correctness.
Mocks, builds, inventories, clean diffs, and agent-written assertions are not
independent proof of those outcomes.

## Drift signals

Treat as drift when **observable**, not when "feels messy":

1. **Doc ≠ reality** — Accepted design with no implementation path; ARCHITECTURE still docs-only after app code lands.
2. **Broken navigation** — Index/AGENTS links 404; routes to deleted leaves.
3. **Status lies** — Plan language claims verified; unverified treated as done.
4. **Repeated violation** — Same failure class under the same harness revision ≥2 times.
5. **Pattern copying** — New files imitate a deprecated layout or bypass checks.
6. **Check bypass** — Lint disabled to merge; rules written but never wired to CI.

### Drift response

```text
Signal
  → Is it execution noise or rule/structure stale?
  → Same pattern repeating? → prefer encode (doc or check)
  → One-off? → fix instance; don't add rules yet
  → Rule with no signal ever? → delete
```

## What "linter / CI for docs" means

| Check type | Question | Example failure |
|---|---|---|
| Structure | Required shape present? | Missing partition `index.md` |
| Cross-links | References resolve? | `AGENTS.md` → missing path |
| Freshness | Claims still true? | Active plan with no progress; generated file hand-edited as SoR |

These are smoke alarms for the knowledge base—not quality scores.

## What "invariants not micro-management" means

- **Invariant:** "UI must not import Repo; go through Service/Provider."
- **Not invariant:** "You must use library X for parsing."

Central platform enforces boundaries; local expression stays free. Lint messages should tell the agent **how to comply**.

## Merge philosophy (do not cargo-cult)

OpenAI context: agent throughput ≫ human attention → short PRs, fewer blocking gates, fix-forward.

Most personal / early repos: human attention is scarce → keep review/blocking checks until retries are cheap and mechanical rules catch copies of bad patterns.

Fast iteration means **small verifiable steps**, not lower standards.

## Stage-0 check catalog (suggested)

Minimal set before application code:

1. Every path linked from `AGENTS.md` exists.
2. Every docs index that lists leaves: paths exist.
3. Design/spec leaves include the repo's required status fields (if any).
4. No file under `generated/` unless a regenerate command is documented.
5. Active plans (if used) are real in-progress work.
6. Research / notes do not silently override confirmed design decisions.

Wire as a script when the repo has CI; until then, run as agent checklist in `check` mode.

## Stage-1+ (after code)

1. Document allowed module dependency edges in `ARCHITECTURE.md` (or equivalent).
2. Enforce edges with import linter or structural test; errors include fix guidance.
3. Project checks (test/lint) become hard evidence (command + exit code), not agent self-report.
4. Optional observability deep links must not block task progress when the tool is down.

## Anti-patterns

- Giant single `AGENTS.md` encyclopedia
- Empty leaf docs "for the index to look complete"
- Harness eval dashboard / composite agent score
- Encoding every preference as a rule (rule rot)
- Auto-modifying merge/sandbox policy from a running agent loop
