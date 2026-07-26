# Interactive Project Onboarding

## Goal

Generate concise project guidance from verifiable repository facts, and create code-review standards only when they are warranted. Do not read every file mechanically, and do not turn common knowledge, **habits already internalized by the model/harness**, or unconfirmed personal preferences into project rules.

The project block in `AGENTS.md` should answer: **what is different in this repository from default behavior?**

## Read-only scan

Prioritize:

1. The repository root, existing `AGENTS.md`, `CLAUDE.md`, README, contribution guide, and architecture docs.
2. Package manifests, lockfiles, build configuration, and primary entry points.
3. CI workflows, PR templates, CODEOWNERS, and release configuration.
4. Test directories and test, lint, format, type-check, coverage, and security-tool configuration.
5. Database migrations, public APIs, protocols, persisted formats, and deployment entry points.
6. A few representative business modules and tests to check whether actual conventions match configuration.

Skip dependency directories, build output, caches, binaries, large generated files, credentials, and secrets. Unless the user asks, do not run formatters, migrations, code generation, installation, or other commands that rewrite files.

## Build a candidate project profile

Use evidence to identify:

- Key directories, module boundaries, and runtime entry points.
- Start, build, test, and static-analysis commands confirmed by configuration.
- CI gates that actually block merge.
- High-risk areas involving public interfaces, migrations, security, or performance.
- Existing engineering conventions and definitions of done (keep deltas only).
- Conflicting evidence, stale commands, and remaining unknowns.

Every conclusion should point to a concrete repository file. Do not invent project rules from language or framework convention. Do not encode generic habits such as “verify before claiming done” or “debug root causes first” as project policy.

## Confirm with the user

Show concise findings first, then ask only about choices that the user must make. Ask no more than three short questions per round, prioritizing:

1. Which commands or checks must block merge (if there is almost no CI/test tooling, confirm whether to skip `code_review.md`).
2. Review risk priorities such as correctness, security, compatibility, performance, or UI.
3. Team preferences that the repository cannot prove, such as collaboration cadence (for example small reviewable diffs), supported versions, migrations, and severity policy.

If the user does not answer, leave those items unconfirmed rather than silently making them mandatory. Do not ask questions answerable from repository configuration, CI, or documentation.

## Draft and confirm

1. Use the project block in `assets/AGENTS.<locale>.template.md` to draft an `agent-guidance:project` block. Remove missing commands and empty headings; keep content **short, executable, and delta-oriented**.
2. Use `assets/CODE_REVIEW.<locale>.template.md` to draft repository-root `code_review.md` **only when** concrete CI/review gates exist or the user explicitly wants a review doc. Skip by default for empty repos, learning labs, and repos with no gates. Remove every placeholder and generation note.
3. Test commands must state their working directory and purpose.
4. Show the proposed content or diff and wait for explicit user approval.
5. Write only after approval. If the user approves only part, apply only that part.

## Updating existing rules

- `agent-guidance:core` may be updated automatically from the template (including upgrades from an older verbose “workflow gearbox” Core to the slim Core).
- `agent-guidance:project` and `code_review.md` are user-owned project rules. After rescanning, propose diffs rather than overwriting silently.
- If existing guidance conflicts with repository evidence, show the conflict and evidence, then let the user keep, change, or remove it.
- Do not delete content outside managed blocks.
