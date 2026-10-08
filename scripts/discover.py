#!/usr/bin/env python3
"""Discover a complete set of canonical manifests without modifying repositories."""
import argparse
from pathlib import Path
import sys

from registry import ROOT, RegistryError, discover, document, json_text, require_valid


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, default=ROOT / "sources/repositories.yaml")
    parser.add_argument("--checkouts", type=Path, help="directory containing all canonical sibling checkouts; otherwise use offline snapshots")
    parser.add_argument("--output", type=Path, help="write JSON to this path instead of stdout")
    args = parser.parse_args(argv)
    try:
        entries = discover(args.sources, args.checkouts)
        require_valid(entries)
        output = json_text(document(entries))
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8", newline="\n")
        else:
            print(output, end="")
    except (RegistryError, OSError, UnicodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
