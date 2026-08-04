---
name: change-report
description: Generate a deterministic standalone HTML report that explains what changed in a local diff, commit, branch, or pull request. Use when the user wants a change summary or file-by-file change report, not code review, audit, risk findings, merge recommendations, or approval decisions.
---

# Change Report

Describe the selected change set and render only structured data into the bundled standalone template. This skill is a change report, not a code review.

## Boundaries

- Work read-only on the source project by default. Write report artifacts outside the project unless the user explicitly chooses a project path.
- Do not diagnose bugs, rank risks, audit behavior, recommend merge actions, approve, request changes, post comments, or modify external state.
- Bind the report to the exact observed base and head when the change set has revisions. Use `not_verified` when either identifier cannot be resolved.
- Report observed facts separately from concise change summaries. Do not turn a file list, build, test result, or author claim into a quality conclusion.
- Keep the report useful for understanding: explain the change purpose when a commit, PR, or Issue states it; show the main change path; classify related changes; and list every changed file with a concrete summary. Optional checks are factual context only.

## Workflow

1. Resolve the change set: working tree, commit range, branch comparison, or pull request. Record its scope and exclusions.
2. Read the diff metadata and changed files. Record each file's status, path, line additions/deletions, and a concrete summary grounded in the diff; avoid generic text such as "modified file".
3. Extract the stated change purpose from the commit, PR, or Issue when available. Describe `summary.before`, `summary.after`, and `summary.flow` as a factual before/after and path explanation; distinguish sourced purpose from a description inferred from the diff.
4. Select up to five key changes for `highlights`. Order them by explanatory value, not risk or severity; each highlight should name the change, its basis, and its main files or hunks.
5. Group related files into human-readable categories such as behavior, adapter, runtime, contract, verification, test, docs, or tooling. Keep the groups descriptive; do not turn them into findings or review conclusions.
6. Add optional factual checks only when their command/output is available. Use `not_run` or `not_verified` when appropriate; omit checks that were not requested or observed.
7. Create the data artifact and render the fixed standalone HTML template.

The bundled renderer is an intentional runtime-free exception: it uses only Python's standard library to validate the nested contract, enforce safe link schemes, escape data for HTML/JavaScript, and replace the template sentinel deterministically. Replacing these checks with manual agent-native edits would remove those guarantees; it adds no third-party, network, or source-project runtime dependency.

## Build the report

Resolve this skill's directory from the loaded `SKILL.md` path.

1. Choose a user-supplied output directory, or create an OS temporary directory when none is supplied. Do not default to the reviewed repository.
2. Copy `assets/change-report-data.v1.json` to `<output>/change-report.json`.
3. Fill the change-report data contract. Preserve `schemaVersion`; do not add review findings, decisions, risk levels, or audit sections.
4. Validate and render:

```bash
python3 <skill-dir>/scripts/render_change_report.py --data <output>/change-report.json --out <output>/report.html
```

5. Open or visually inspect `report.html` when a browser or screenshot surface is available. Return clickable links to the report and data artifact, with a short scope summary.

Run the bundled renderer check after changing this skill:

```bash
python3 <skill-dir>/scripts/render_change_report.py --self-test
```

The generated `report.html` is self-contained: embedded data, inline style and script, no fetch, no CDN, and no runtime dependency on `change-report.json`.

## Data contract

Use only plain text and optional links. Never put model-generated HTML in JSON. Links may be empty, `#fragment`, `http(s)`, or `file:` URLs. The complete item shapes are in `references/change-report-data-v1.md`.

- `report`: title, repository/URL, optional full-Diff URL, scope, exclusions, source, and generation time.
- `revision`: exact base/head identifiers and whether they were observed.
- `summary`: optional purpose and its source, before/after description, ordered change flow, one-line change headline, and detail explaining the main change path.
- `stats`: total changed files, additions, and deletions.
- `highlights`: up to five explanatory key changes with category, basis, file links, and optional Hunk links; never add severity or consequence fields.
- `files`: every changed file with status, path, optional old path/area/link, additions/deletions, and a concise diff summary.
- `groups`: descriptive change areas with a category, explanation, basis, and linked file labels.
- `checks`: optional factual command results; these do not imply quality or acceptance.

Allowed file statuses are `added`, `modified`, `deleted`, `renamed`, `copied`, `untracked`, and `unknown`. Allowed group categories are `behavior`, `adapter`, `runtime`, `contract`, `verification`, `test`, `docs`, `tooling`, and `other`. Allowed revision states are `observed` and `not_verified`. Allowed check statuses are `passed`, `failed`, `not_run`, and `not_verified`.

Do not add fields for drift judgments, blast radius risk, findings, evidence gaps, decision boundaries, approval state, severity, consequence, or human attention routing. If the user asks for those, use a separate review skill or ask them to change the requested mode.
