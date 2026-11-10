"""Scan folders for duplicate files by content without third-party dependencies."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def digest(path: Path, chunk_size: int = 1024 * 1024) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(chunk_size), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def find_duplicates(root: Path) -> list[list[str]]:
    """Return deterministically sorted groups of files with identical contents."""
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")
    sizes: dict[int, list[Path]] = defaultdict(list)
    for path in root.rglob("*"):
        if path.is_file() and not path.is_symlink():
            try:
                sizes[path.stat().st_size].append(path)
            except OSError:
                continue
    groups: list[list[str]] = []
    for candidates in sizes.values():
        if len(candidates) < 2:
            continue
        hashes: dict[str, list[str]] = defaultdict(list)
        for path in candidates:
            try:
                hashes[digest(path)].append(str(path.relative_to(root)))
            except OSError:
                continue
        groups.extend(sorted(paths) for paths in hashes.values() if len(paths) > 1)
    return sorted(groups)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Find duplicate files by SHA-256")
    parser.add_argument("directory", type=Path, help="Directory to scan recursively")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args(argv)
    try:
        duplicates = find_duplicates(args.directory)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps({"duplicate_groups": duplicates}, indent=2))
    elif not duplicates:
        print("No duplicate files found.")
    else:
        for index, files in enumerate(duplicates, 1):
            print(f"Group {index}:")
            for filename in files:
                print(f"  {filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
