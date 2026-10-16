#!/usr/bin/env python3

import argparse
import json
import unicodedata
import re
import sys
from datetime import date
from pathlib import Path


PROJECT_TYPES = (
    "website",
    "web-app",
    "ios-app",
    "android-app",
    "cross-platform-app",
    "desktop-app",
    "internal-tool",
    "api",
    "cli",
    "library",
    "other",
)


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value.replace("đ", "d").replace("Đ", "D"))
    ascii_name = normalized.encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    if not slug:
        raise ValueError("Project name must contain at least one letter or digit.")
    return slug


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a safe product-to-code workspace without scaffolding application code."
    )
    parser.add_argument("--name", required=True, help="Human-readable project name.")
    parser.add_argument("--type", required=True, choices=PROJECT_TYPES, dest="project_type")
    parser.add_argument(
        "--path",
        type=Path,
        help="Exact target directory. Defaults to the current directory plus the project slug.",
    )
    parser.add_argument(
        "--integrate",
        action="store_true",
        help="Add missing scaffold files to an existing non-empty directory; never overwrite.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Print actions without writing.")
    return parser.parse_args()


def template_destination(relative: Path) -> Path:
    if relative.suffix == ".tmpl":
        return relative.with_suffix("")
    return relative


def render(content: str, values: dict[str, str]) -> str:
    for token, value in values.items():
        content = content.replace(f"{{{{{token}}}}}", value)
    return content


def main() -> int:
    args = parse_args()
    if not args.name.strip() or any(ord(c) < 32 for c in args.name):
        print("Project name must be non-empty and single-line.", file=sys.stderr)
        return 2
    try:
        slug = slugify(args.name)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2
    target = (args.path or (Path.cwd() / slug)).expanduser().resolve()
    template_root = Path(__file__).resolve().parents[1] / "assets" / "project-kit"

    if not template_root.is_dir():
        print(f"Template directory is missing: {template_root}", file=sys.stderr)
        return 1

    if target.exists() and not target.is_dir():
        print(f"Target is not a directory: {target}", file=sys.stderr)
        return 1

    non_empty = target.exists() and any(target.iterdir())
    if non_empty and not args.integrate:
        print(
            f"Target is not empty: {target}. Inspect it and rerun with --integrate to add only missing files.",
            file=sys.stderr,
        )
        return 2

    values = {
        "PROJECT_NAME": args.name,
        "PROJECT_NAME_YAML": json.dumps(args.name, ensure_ascii=False),
        "PROJECT_SLUG": slug,
        "PROJECT_TYPE": args.project_type,
        "DATE": date.today().isoformat(),
    }

    created: list[Path] = []
    skipped: list[Path] = []
    local_directories = (
        Path("workbench/active"),
        Path("workbench/evidence"),
        Path("workbench/exports"),
        Path("workbench/scratch"),
    )

    # Preflight the entire plan before any writes, including dry runs.
    planned = []
    try:
        for source in sorted(path for path in template_root.rglob("*.tmpl") if path.is_file()):
            relative = template_destination(source.relative_to(template_root))
            destination = target / relative
            for part in [destination, *destination.parents]:
                if part == target:
                    break
                if part.is_symlink():
                    raise ValueError(f"Refusing symlink in scaffold path: {part}")
                if part != destination and part.exists() and not part.is_dir():
                    raise ValueError(f"Expected directory: {part}")
            if destination.exists():
                if not destination.is_file():
                    raise ValueError(f"Expected file: {destination}")
                skipped.append(relative)
                continue
            content = render(source.read_text(encoding="utf-8"), values)
            if re.search(r"\{\{[A-Z0-9_]+\}\}", content):
                raise ValueError(f"Unresolved template token: {relative}")
            planned.append((relative, content))
        for relative in local_directories:
            destination = target / relative
            if destination.is_symlink() or (destination.exists() and not destination.is_dir()):
                raise ValueError(f"Expected ordinary directory: {destination}")
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2

    for relative, content in planned:
        if not args.dry_run:
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            with destination.open("x", encoding="utf-8") as output:
                output.write(content)
        created.append(relative)

    if not args.dry_run:
        for relative in local_directories:
            (target / relative).mkdir(parents=True, exist_ok=True)

    unresolved = []
    if not args.dry_run:
        for relative in created:
            content = (target / relative).read_text(encoding="utf-8")
            if re.search(r"\{\{[A-Z0-9_]+\}\}", content):
                unresolved.append(relative)

    if unresolved:
        print("Unresolved template tokens:", file=sys.stderr)
        for relative in unresolved:
            print(f"  {relative}", file=sys.stderr)
        return 1

    action = "Would create" if args.dry_run else "Created"
    print(f"{action} project workspace: {target}")
    print(f"Project type: {args.project_type}")
    print(f"Files created: {len(created)}")
    print(f"Files skipped: {len(skipped)}")

    for relative in created:
        print(f"  CREATE {relative}")
    for relative in skipped:
        print(f"  SKIP   {relative}")

    if not args.dry_run:
        print("Status: discovery (scaffold only). Next: complete the brief; assess readiness before implementation.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
