# GitHub Collaboration Lab

A practical, dependency-free Python command-line tool for finding duplicate files without deleting or modifying them. Files are grouped by size before SHA-256 hashing to reduce disk reads.

## Installation and usage

Requires Python 3.10+.

```bash
python -m pip install -e .
dupscan /path/to/folder
dupscan /path/to/folder --json
dupscan /path/to/folder --min-size 1048576
```

Without installation: `PYTHONPATH=src python -m collab_lab.cli .`

### Minimum file size filter

Use `--min-size BYTES` to skip files smaller than the specified byte count before hashing. For example, `--min-size 1048576` considers files of at least 1 MiB. A file exactly equal to the threshold is included. Negative sizes are rejected. This option works with `--json` as well.

## Tests

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

PowerShell: `$env:PYTHONPATH='src'; python -m unittest discover -s tests -v`

## Collaboration

See [CONTRIBUTING.md](CONTRIBUTING.md). Changes should be meaningful, reviewed, and tested. Only add co-author attribution to changes actually made together using the contributor's verified commit email.

## Limitations

Symlinks are ignored, unreadable files are skipped, and scans of large folders may take time. SHA-256 hash collisions are extraordinarily unlikely but theoretically possible.
