# Change report data v1

Start from `assets/change-report-data.v1.json`. Preserve the top-level structure and use only plain text plus optional links. The report describes a change set; it does not make a review or merge decision.

## Enums

- `locale`: `zh-CN`, `en`
- `revision.status`: `observed`, `not_verified`
- File status: `added`, `modified`, `deleted`, `renamed`, `copied`, `untracked`, `unknown`
- Check status: `passed`, `failed`, `not_run`, `not_verified`

## Top-level sections

```json
{
  "schemaVersion": 1,
  "locale": "zh-CN",
  "report": {
    "title": "变更报告",
    "repository": "owner/repository",
    "url": "https://github.com/owner/repository/pull/42",
    "diffUrl": "https://github.com/owner/repository/pull/42/files",
    "scope": "base abc123 → head def456",
    "excluded": ["部署环境"],
    "source": "local Git diff",
    "generatedAt": "2026-08-03T00:00:00Z"
  },
  "revision": {"base": "abc123", "head": "def456", "status": "observed"},
  "summary": {
    "purpose": "来自 PR/Issue/commit 的改动目的。",
    "purposeSource": "PR description",
    "before": "改动前的相关路径或结构。",
    "after": "改动后的相关路径或结构。",
    "flow": ["入口 → 核心处理", "核心处理 → 结果"],
    "headline": "一句话描述这批改动。",
    "details": "解释主要变化如何连接起来。"
  },
  "stats": {"files": 2, "additions": 10, "deletions": 3},
  "highlights": [],
  "files": [],
  "groups": [],
  "checks": []
}
```

`report.excluded` can describe files or environments intentionally outside the report. `revision.status` is `observed` only when both identifiers resolve from VCS, a PR API, or the assigned Workspace.

## File item

Include every changed file. Use `oldPath` for renames; leave it empty otherwise. `summary` must describe the visible diff, not whether the change is correct.

```json
{
  "status": "modified",
  "path": "src/module/file.ts",
  "oldPath": "",
  "area": "Scheduler",
  "additions": 18,
  "deletions": 4,
  "summary": "增加重试状态转换和对应调用路径。",
  "href": "file:///absolute/path/src/module/file.ts#L42"
}
```

## Highlight item

Highlights are the few most useful explanations for orientation, not risk findings. Order them by how much they help a reader understand the change.

```json
{
  "category": "behavior",
  "title": "缓存读取路径",
  "summary": "把缓存分支接入读取路径，并同步增加命中与失效场景。",
  "basis": "PR description 与 local diff",
  "files": [{"label": "src/cache.ts", "href": "file:///absolute/path/src/cache.ts#L42"}],
  "hunks": [{"label": "src/cache.ts:42", "href": "file:///absolute/path/src/cache.ts#L42"}]
}
```

Up to five highlights are allowed. Do not add severity, consequence, claim, or decision fields.

## Group item

Groups are the report's main structure. Use a category to distinguish behavior, adapters, runtime, contracts, verification, tests, docs, and tooling. Keep each explanation descriptive and link the files that belong to the area.

```json
{
  "category": "adapter",
  "title": "Scheduler lifecycle",
  "summary": "集中展示调度状态和重试相关文件。",
  "basis": "local diff",
  "files": [
    {"label": "src/scheduler.ts", "href": "file:///absolute/path/src/scheduler.ts#L1"}
  ]
}
```

Allowed group categories are `behavior`, `adapter`, `runtime`, `contract`, `verification`, `test`, `docs`, `tooling`, and `other`.

## Check item

Checks are optional factual context. They do not establish quality, safety, or acceptance.

```json
{
  "name": "Tests",
  "status": "passed",
  "summary": "命令退出状态为 0。",
  "command": "pnpm test",
  "href": ""
}
```
