#!/usr/bin/env python3
"""Validate localized resources and SKILL.md paths."""

import re
import sys
from pathlib import Path


LOCALES = ("en", "zh-CN")
SINGLE_LOCALE_RESOURCES: set[str] = set()
REFERENCE_RE = re.compile(
    r"(?<![\w/])((?:references|assets)/[A-Za-z0-9_.<>\-/]+)"
)


def validate(root: Path) -> list[str]:
    errors = []
    skills = sorted(root.glob("plugins/*/skills/*/SKILL.md"))
    if not skills:
        return ["no SKILL.md found under plugins/*/skills/*/"]

    for skill_md in skills:
        skill = skill_md.parent
        for match in REFERENCE_RE.finditer(skill_md.read_text()):
            reference = match.group(1).rstrip(".,;:)]/")
            localized = "<locale>" in reference
            paths = (
                [reference.replace("<locale>", locale) for locale in LOCALES]
                if localized
                else [reference]
            )
            for path in paths:
                if not (skill / path).exists():
                    reason = (
                        "missing localized counterpart"
                        if localized
                        else "referenced path does not exist"
                    )
                    errors.append(f"{skill_md}: {reason} '{path}'")

        for directory in (skill / "assets", skill / "references"):
            if not directory.is_dir():
                continue
            for path in directory.rglob("*"):
                if not path.is_file():
                    continue
                relative = path.relative_to(root).as_posix()
                if relative in SINGLE_LOCALE_RESOURCES:
                    continue
                for locale, counterpart in (("en", "zh-CN"), ("zh-CN", "en")):
                    marker = f".{locale}."
                    if marker not in path.name:
                        continue
                    expected = path.with_name(path.name.replace(marker, f".{counterpart}.", 1))
                    if not expected.is_file():
                        errors.append(
                            f"{path}: missing localized counterpart '{expected.name}'"
                        )
    return errors


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate(root)
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)
    print("Repository paths and localized resources are valid")


if __name__ == "__main__":
    main()
