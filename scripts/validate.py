#!/usr/bin/env python3
"""Validate manifests and report read-only maintenance diagnostics as JSON."""
import argparse
import datetime as dt
from pathlib import Path
import sys

from registry import ROOT, RegistryError, discover, json_text, read_yaml, validate


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifests", type=Path, nargs="*", help="explicit complete manifest set, including dependencies")
    parser.add_argument("--sources", type=Path, default=ROOT / "sources/repositories.yaml")
    parser.add_argument("--checkouts", type=Path, help="discover all canonical siblings instead of offline snapshots")
    parser.add_argument("--today", type=dt.date.fromisoformat, help="YYYY-MM-DD for repeatable stale checks")
    parser.add_argument("--stale-days", type=int, default=365)
    parser.add_argument("--check-links", action="store_true", help="opt in to HTTPS requests (10-second timeout each)")
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args(argv)
    if args.manifests and args.checkouts:
        parser.error("choose explicit manifests or --checkouts")
    if args.stale_days < 0:
        parser.error("--stale-days must be nonnegative")
    try:
        entries = ([{"manifest": read_yaml(path), "root": path.resolve().parent, "provenance": {}} for path in args.manifests]
                   if args.manifests else discover(args.sources, args.checkouts))
        diagnostics = validate(entries, args.today, args.stale_days, args.check_links)
        print(json_text({"manifest_count": len(entries), "diagnostics": diagnostics}), end="")
        return int(any(d["severity"] == "error" or args.warnings_as_errors for d in diagnostics))
    except (RegistryError, OSError, UnicodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
