---
name: harness-audit
description: >-
  Audits and maintains repo-local Agent Harness: short AGENTS.md as a map,
  structured docs as system of record, mechanical structure/cross-link/freshness
  checks, and failure-to-rule feedback loops (OpenAI Harness Engineering). Use
  when auditing project harness, scaffolding docs layout, checking indexes and
  links, encoding review taste into docs or linters, diagnosing harness drift,
  doc-gardening, or when the user mentions repo-as-system-of-record. Does not
  build Harness eval products, composite scores, or Finding dashboards.
---

# Harness Audit

Use repo-local docs, checks, and feedback loops to make Agents reliable. This
is repository hygiene and workflow design—not an eval platform, scorecard, or
Harness management product.

Primary source: [Harness Engineering](https://openai.com/index/harness-engineering/)
(OpenAI). Practice the harness in-repo while building the product; extract more
automation only after the same loop repeats.

## Boundaries

- Do not build eval/management surfaces, Finding boards, or composite scores.
- Do not treat a generic Trace/Eval UI as the repository source of truth.
- Do not silently change permissions, CI, merge policy, or release controls.
- Do not cargo-cult blocking gates when human throughput is the bottleneck.

## Evidence discipline

Label material claims as one of:

- **Observed** — a file, command result, test, CI run, or human decision directly shows it.
- **Inferred** — source or structure supports it, but the behavior was not executed.
- **Declared** — documentation says it is intended or decided.
- **Not verified** — runtime, CI, deployment, credentials, external services, or human acceptance were not checked.

Keep these states separate. A mock, inventory, build, clean diff, or static
document does not prove runtime or business correctness.

## Modes

Pick one mode from the request (default: audit):

| Mode | When | Output |
|---|---|---|
| audit | "check / audit harness" | Evidence-backed gaps + priorities |
| scaffold | "init / align skeleton" | Minimum directory + entry edits |
| check | "structure / links / freshness" | Mechanical failures with fix hints |
| encode | Repeated failure or review feedback | One doc rule or one failing check |
| garden | "garden / stale docs" | PR-sized candidate fixes |

## Fast path

1. Resolve the repository root and existing conventions.
2. Read AGENTS.md, the root README.md, ARCHITECTURE.md if present, and each
   docs partition index.md in use. Inspect existing tests, scripts, and CI
   before proposing a new check.
3. Classify each finding as Have, Missing, Drift signal, or Not verified. Do
   not call an optional file missing merely because a template suggested it.
4. Choose the smallest useful change and one runnable check. Stop after the
   requested mode is satisfied.

## Core loop

Stuck or failed
  → Missing capability, guidance, or enforcement?
  → Write the smallest repo-local rule or check
  → Verify on the next real task
  → Keep if it works; shrink, change, or delete it if not

## Principles

1. **Repo is the system of record**: chat or memory does not count until the
   decision is versioned in Git.
2. **Map, not encyclopedia**: keep AGENTS.md short (about 100 lines or less)
   and put durable truth in partitioned docs plus indexes.
3. **Mechanical checks are evidence**: use scripts/CI for structure, links,
   required fields, and dependency boundaries; leave judgment to docs and
   human review.
4. **Invariants beat micro-management**: enforce boundaries and dependency
   direction, then allow implementation freedom inside them.
5. **Errors teach the next action**: every checker failure names the fix.
6. **Drift is signal-based, not scored**: act on doc/reality mismatch, repeated
   violations, deprecated pattern copying, or bypassed checks.
7. **Merge policy matches throughput**: keep human review and blocking gates
   until retries are cheap and mechanical checks catch the common copies.

## Workflow by mode

### audit

1. Read the map, documentation indexes, existing checks, and recent failure or
   review evidence.
2. Judge only what the evidence supports:
   - Is AGENTS.md navigation rather than an encyclopedia?
   - Are design, specs, research, plans, and generated output separated where
     the repo uses them?
   - Do existing checks cover structure, links, freshness, and key invariants?
   - Are repeated pain points encoded in docs or checks?
3. Report Have, Missing, Drift signals, Not verified, and the next 1–3 actions.
   Do not propose a Harness management product.

### scaffold

Create or align only the minimum skeleton, adapting to repository conventions:

    AGENTS.md                 # short map
    ARCHITECTURE.md           # physical/module map when code exists
    docs/
      <partition>/index.md    # only partitions the repo actually uses
      exec-plans/active/      # only when the repo uses ExecPlans
      exec-plans/completed/
      PLANS.md

- Do not create empty leaf docs for completeness.
- Give every new partition an index.md.
- Reuse the repo's evidence markers, such as Observed, Decision, Proposed,
  Not verified, and Out of scope.
- Prefer editing the existing layout over renaming it wholesale.

### check

Run existing scripts first. If no checker exists, return a pasteable checklist
or add one only when the rule is repeatable and the repo has a natural place
to run it. Check:

- required indexes and AGENTS.md links exist;
- links in maps and indexes resolve;
- status fields and freshness claims are internally consistent;
- generated files document their regeneration command;
- active plans are real, in-progress work.

Use actionable errors:

    Broken link: docs/design-docs/index.md → ./missing.md
    Fix: restore the file or remove the index row.

### encode

For a failure, review comment, or repeated Agent mistake:

1. Classify it as missing tool, missing doc, missing enforceable rule, or noise.
2. Choose one short doc rule or one mechanical check with a fix-oriented
   message.
3. Delete or shrink rules that no Agent follows and no check enforces.
4. Stop; do not open a CMS or eval feature.

### garden

Scan the signals in [reference.md](reference.md), then propose or implement
PR-sized fixes: repair links, mark stale proposals, archive dead plans, and
update ARCHITECTURE.md when reality changed. Keep merge and release decisions
under human control.

## Stage guidance

| Stage | Do | Don't |
|---|---|---|
| Docs-only | map, indexes, and stage-0 checks | dependency linters or GC bots |
| App exists | module invariants and project checks as hard evidence | lower standards by default |
| Stable loop | doc gardening and small GC | Harness eval dashboards |

## Additional resources

- Article map, evidence rules, drift signals, and stage-0 catalog:
  [reference.md](reference.md)

Trigger tip: default mode is audit; say scaffold, check, encode, or garden when
needed.
