#!/usr/bin/env python3
"""Render change-report/v1 JSON into the bundled standalone HTML template."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

SCHEMA_VERSION = 1
MAX_INPUT_BYTES = 2_000_000
DATA_SENTINEL = "__CHANGE_REPORT_DATA__"
ALLOWED_LOCALES = {"en", "zh-CN"}
ALLOWED_REVISION_STATES = {"observed", "not_verified"}
ALLOWED_FILE_STATUSES = {"added", "modified", "deleted", "renamed", "copied", "untracked", "unknown"}
ALLOWED_CHECK_STATUSES = {"passed", "failed", "not_run", "not_verified"}
ALLOWED_GROUP_CATEGORIES = {"behavior", "adapter", "runtime", "contract", "verification", "test", "docs", "tooling", "other"}
ALLOWED_HREF_SCHEMES = {"file", "http", "https"}


class ContractError(ValueError):
    pass


def require_object(value: Any, path: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError(f"{path} must be an object")
    return value


def require_list(value: Any, path: str, *, maximum: int | None = None) -> list[Any]:
    if not isinstance(value, list):
        raise ContractError(f"{path} must be an array")
    if maximum is not None and len(value) > maximum:
        raise ContractError(f"{path} must contain at most {maximum} items")
    return value


def require_string(value: Any, path: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        qualifier = "a string" if allow_empty else "a non-empty string"
        raise ContractError(f"{path} must be {qualifier}")
    return value


def require_string_list(value: Any, path: str, *, maximum: int = 100) -> list[str]:
    rows = require_list(value, path, maximum=maximum)
    for index, row in enumerate(rows):
        require_string(row, f"{path}[{index}]")
    return rows


def validate_href(value: Any, path: str) -> None:
    href = require_string(value, path, allow_empty=True)
    if not href or href.startswith("#"):
        return
    parsed = urlsplit(href)
    scheme = parsed.scheme.lower()
    if scheme not in ALLOWED_HREF_SCHEMES:
        raise ContractError(f"{path} must use http(s), file, or a fragment href")
    if scheme in {"http", "https"} and not parsed.netloc:
        raise ContractError(f"{path} must include a host for {scheme}")
    if scheme == "file" and not parsed.path and not parsed.netloc:
        raise ContractError(f"{path} must include a file path")


def require_choice(value: Any, path: str, choices: set[str]) -> str:
    text = require_string(value, path)
    if text not in choices:
        raise ContractError(f"{path} must be one of: {', '.join(sorted(choices))}")
    return text


def require_nonnegative_int(value: Any, path: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ContractError(f"{path} must be a non-negative integer")
    return value


def validate_link(value: Any, path: str) -> None:
    link = require_object(value, path)
    require_string(link.get("label"), f"{path}.label")
    validate_href(link.get("href", ""), f"{path}.href")


def validate_file(value: Any, path: str) -> None:
    item = require_object(value, path)
    require_choice(item.get("status"), f"{path}.status", ALLOWED_FILE_STATUSES)
    require_string(item.get("path"), f"{path}.path")
    require_string(item.get("oldPath", ""), f"{path}.oldPath", allow_empty=True)
    require_string(item.get("area", ""), f"{path}.area", allow_empty=True)
    require_nonnegative_int(item.get("additions"), f"{path}.additions")
    require_nonnegative_int(item.get("deletions"), f"{path}.deletions")
    require_string(item.get("summary"), f"{path}.summary")
    validate_href(item.get("href", ""), f"{path}.href")
    for index, hunk in enumerate(require_list(item.get("hunks", []), f"{path}.hunks", maximum=50)):
        validate_link(hunk, f"{path}.hunks[{index}]")


def validate_group(value: Any, path: str) -> None:
    group = require_object(value, path)
    require_choice(group.get("category"), f"{path}.category", ALLOWED_GROUP_CATEGORIES)
    require_string(group.get("title"), f"{path}.title")
    require_string(group.get("summary", ""), f"{path}.summary", allow_empty=True)
    require_string(group.get("basis", ""), f"{path}.basis", allow_empty=True)
    for index, link in enumerate(require_list(group.get("files", []), f"{path}.files", maximum=500)):
        validate_link(link, f"{path}.files[{index}]")


def validate_highlight(value: Any, path: str) -> None:
    highlight = require_object(value, path)
    require_choice(highlight.get("category"), f"{path}.category", ALLOWED_GROUP_CATEGORIES)
    require_string(highlight.get("title"), f"{path}.title")
    require_string(highlight.get("summary"), f"{path}.summary")
    require_string(highlight.get("basis", ""), f"{path}.basis", allow_empty=True)
    for index, link in enumerate(require_list(highlight.get("files", []), f"{path}.files", maximum=100)):
        validate_link(link, f"{path}.files[{index}]")
    for index, link in enumerate(require_list(highlight.get("hunks", []), f"{path}.hunks", maximum=50)):
        validate_link(link, f"{path}.hunks[{index}]")


def validate_check(value: Any, path: str) -> None:
    check = require_object(value, path)
    require_string(check.get("name"), f"{path}.name")
    require_choice(check.get("status"), f"{path}.status", ALLOWED_CHECK_STATUSES)
    require_string(check.get("summary"), f"{path}.summary")
    require_string(check.get("command", ""), f"{path}.command", allow_empty=True)
    validate_href(check.get("href", ""), f"{path}.href")


def validate_change_data(data: Any) -> dict[str, Any]:
    root = require_object(data, "report")
    if root.get("schemaVersion") != SCHEMA_VERSION:
        raise ContractError(f"schemaVersion must equal {SCHEMA_VERSION}")
    require_choice(root.get("locale"), "locale", ALLOWED_LOCALES)

    report = require_object(root.get("report"), "report.report")
    for key in ("title", "scope", "source", "generatedAt"):
        require_string(report.get(key), f"report.report.{key}")
    require_string(report.get("repository", ""), "report.report.repository", allow_empty=True)
    validate_href(report.get("url", ""), "report.report.url")
    validate_href(report.get("diffUrl", ""), "report.report.diffUrl")
    require_string_list(report.get("excluded", []), "report.report.excluded", maximum=100)

    revision = require_object(root.get("revision"), "report.revision")
    revision_status = require_choice(revision.get("status"), "report.revision.status", ALLOWED_REVISION_STATES)
    allow_empty_revision = revision_status == "not_verified"
    require_string(revision.get("base"), "report.revision.base", allow_empty=allow_empty_revision)
    require_string(revision.get("head"), "report.revision.head", allow_empty=allow_empty_revision)

    summary = require_object(root.get("summary"), "report.summary")
    require_string(summary.get("purpose", ""), "report.summary.purpose", allow_empty=True)
    require_string(summary.get("purposeSource", ""), "report.summary.purposeSource", allow_empty=True)
    require_string(summary.get("before", ""), "report.summary.before", allow_empty=True)
    require_string(summary.get("after", ""), "report.summary.after", allow_empty=True)
    require_string_list(summary.get("flow", []), "report.summary.flow", maximum=20)
    require_string(summary.get("headline"), "report.summary.headline")
    require_string(summary.get("details", ""), "report.summary.details", allow_empty=True)

    stats = require_object(root.get("stats"), "report.stats")
    for key in ("files", "additions", "deletions"):
        require_nonnegative_int(stats.get(key), f"report.stats.{key}")

    for index, highlight in enumerate(require_list(root.get("highlights", []), "report.highlights", maximum=5)):
        validate_highlight(highlight, f"report.highlights[{index}]")

    for index, item in enumerate(require_list(root.get("files"), "report.files", maximum=2000)):
        validate_file(item, f"report.files[{index}]")

    for index, group in enumerate(require_list(root.get("groups", []), "report.groups", maximum=100)):
        validate_group(group, f"report.groups[{index}]")

    for index, check in enumerate(require_list(root.get("checks", []), "report.checks", maximum=100)):
        validate_check(check, f"report.checks[{index}]")

    return root


def read_data(path: Path) -> dict[str, Any]:
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ContractError(f"input exceeds {MAX_INPUT_BYTES} bytes")
    try:
        return validate_change_data(json.loads(path.read_text(encoding="utf-8")))
    except json.JSONDecodeError as error:
        raise ContractError(f"invalid JSON: {error}") from error


def serialize_for_html(data: dict[str, Any]) -> str:
    return (
        json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def render(data: dict[str, Any], output_path: Path) -> None:
    template_path = Path(__file__).resolve().parent.parent / "assets" / "change-report-template.html"
    template = template_path.read_text(encoding="utf-8")
    if template.count(DATA_SENTINEL) != 1:
        raise ContractError("bundled template must contain exactly one data sentinel")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template.replace(DATA_SENTINEL, serialize_for_html(data)), encoding="utf-8")


def sample_data() -> dict[str, Any]:
    return {
        "schemaVersion": 1,
        "locale": "zh-CN",
        "report": {
            "title": "示例变更报告",
            "repository": "example/repo",
            "url": "https://example.invalid/pull/42",
            "diffUrl": "https://example.invalid/pull/42/files",
            "scope": "base 1111111 → head 2222222",
            "excluded": ["部署环境"],
            "source": "local diff",
            "generatedAt": "2026-08-03T00:00:00Z",
        },
        "revision": {"base": "1111111", "head": "2222222", "status": "observed"},
        "summary": {
            "purpose": "把缓存读取改为可复用的进程内路径，并补充对应测试。",
            "purposeSource": "PR description",
            "before": "读取路径直接执行底层查询，相关测试分散在调用方。",
            "after": "读取路径经过进程内缓存，测试集中覆盖命中和失效场景。",
            "flow": ["调用方 → 缓存读取", "缓存未命中 → 底层查询", "测试 → 命中与失效场景"],
            "headline": "缓存读取路径与相关测试发生变化。",
            "details": "报告列出文件级状态、增删统计和按模块归类的变更摘要。 </script><script>alert(1)</script>",
        },
        "stats": {"files": 2, "additions": 18, "deletions": 5},
        "highlights": [
            {
                "category": "behavior",
                "title": "缓存读取路径",
                "summary": "把缓存分支接入读取路径，并同步增加命中与失效场景。",
                "basis": "PR description 与 local diff",
                "files": [{"label": "src/cache.ts", "href": "file:///tmp/cache.ts#L42"}],
                "hunks": [{"label": "src/cache.ts:42", "href": "file:///tmp/cache.ts#L42"}]
            }
        ],
        "files": [
            {
                "status": "modified",
                "path": "src/cache.ts",
                "oldPath": "",
                "area": "缓存",
                "additions": 14,
                "deletions": 4,
                "summary": "加入进程内缓存读取分支。",
                "href": "file:///tmp/cache.ts#L42",
            },
            {
                "status": "added",
                "path": "tests/cache.test.ts",
                "oldPath": "",
                "area": "测试",
                "additions": 4,
                "deletions": 1,
                "summary": "增加缓存命中和失效场景。",
                "href": "",
            },
        ],
        "groups": [
            {
                "category": "behavior",
                "title": "缓存读取",
                "summary": "实现缓存分支并补充对应测试。",
                "basis": "local diff",
                "files": [
                    {"label": "src/cache.ts", "href": "file:///tmp/cache.ts#L42"},
                    {"label": "tests/cache.test.ts", "href": ""},
                ],
            }
        ],
        "checks": [
            {"name": "Tests", "status": "passed", "summary": "测试命令退出状态为 0。", "command": "pnpm test", "href": ""}
        ],
    }


def run_self_test() -> None:
    data = validate_change_data(sample_data())
    unverified = json.loads(json.dumps(data))
    unverified["revision"] = {"base": "", "head": "", "status": "not_verified"}
    validate_change_data(unverified)
    for href in ("javascript:alert(1)", "data:text/html,unsafe"):
        try:
            validate_href(href, "selfTest.href")
        except ContractError:
            pass
        else:
            raise ContractError(f"unsafe href was accepted: {href}")
    for href in ("https://example.invalid/report", "file:///tmp/report.html", "#files-section"):
        validate_href(href, "selfTest.href")
    with tempfile.TemporaryDirectory(prefix="change-report-") as directory:
        output = Path(directory) / "report.html"
        render(data, output)
        without_hunks = json.loads(json.dumps(data))
        del without_hunks["highlights"][0]["hunks"]
        render(validate_change_data(without_hunks), Path(directory) / "report-without-hunks.html")
        html = output.read_text(encoding="utf-8")
        if "</script><script>alert(1)</script>" in html:
            raise ContractError("unsafe script terminator was not escaped")
        if "\\u003c/script\\u003e" not in html:
            raise ContractError("escaped script terminator missing")
        if DATA_SENTINEL in html:
            raise ContractError("data sentinel was not replaced")
        if "@media (prefers-color-scheme: dark)" not in html or "color-scheme: dark" not in html:
            raise ContractError("automatic dark color scheme is missing")
        if "Review Decision" in html or "review decision" in html or "decisionBoundary" in html:
            raise ContractError("review decision language leaked into the change report")
        if "file-list" not in html or "change-groups" not in html or "summary-purpose" not in html or "group-category" not in html or "highlight-list" not in html or "summary-flow" not in html:
            raise ContractError("change report sections are missing")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, help="change-report/v1 JSON input")
    parser.add_argument("--out", type=Path, help="standalone HTML output")
    parser.add_argument("--validate-only", action="store_true", help="validate JSON without rendering")
    parser.add_argument("--self-test", action="store_true", help="run the bundled renderer safety check")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.self_test:
            run_self_test()
            print(json.dumps({"status": "ok", "selfTest": True}))
            return 0
        if args.data is None:
            raise ContractError("--data is required")
        data = read_data(args.data)
        if not args.validate_only:
            if args.out is None:
                raise ContractError("--out is required unless --validate-only is used")
            render(data, args.out)
        print(
            json.dumps(
                {
                    "status": "ok",
                    "schemaVersion": data["schemaVersion"],
                    "files": len(data["files"]),
                    "output": str(args.out.resolve()) if args.out and not args.validate_only else None,
                },
                ensure_ascii=False,
            )
        )
        return 0
    except (ContractError, OSError) as error:
        print(json.dumps({"status": "error", "message": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
