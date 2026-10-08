#!/usr/bin/env python3
"""Explicitly refresh hash-pinned snapshots; no automatic source-repository writes."""
import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen

from registry import ROOT, VERSION, RegistryError, confined, git_info, json_text, parse_yaml, require_valid, sha256, source_records


def fetch(url):
    request = Request(url, headers={"User-Agent": "AIPE-Registry/0.1", "Accept": "application/vnd.github+json"})
    with urlopen(request, timeout=30) as response:
        # Manifests are metadata, not arbitrary large downloads.
        data = response.read(2_000_001)
        if len(data) > 2_000_000:
            raise RegistryError(f"manifest/API response exceeds 2 MB: {url}")
        return data


def refresh(sources, checkouts=None, remote=False):
    records = source_records(sources)
    entries, snapshots, locked = [], {}, []
    for source in records:
        if remote:
            slug = source["repository"].removeprefix("https://github.com/")
            revision = json.loads(fetch(f"https://api.github.com/repos/{slug}/commits/{quote(source['ref'], safe='')}"))
            commit = revision["sha"]
            if not re.fullmatch(r"[a-f0-9]{40}", commit):
                raise RegistryError(f"unexpected remote revision: {commit}")
            if source["state"] == "pinned" and commit != source["ref"]:
                raise RegistryError("remote did not resolve the pinned commit")
            data = fetch(f"https://raw.githubusercontent.com/{slug}/{commit}/{quote(source['path'], safe='/')}")
            provenance = {"commit": commit, "committed_at": revision["commit"]["committer"]["date"], "manifest_dirty": False, "origin": "remote"}
            root = None
        else:
            root = Path(checkouts).resolve() / source["repository"].rsplit("/", 1)[1]
            data = confined(root, source["path"]).read_bytes()
            provenance = {**git_info(root, source["path"]), "origin": "local_checkout"}
        manifest = parse_yaml(data.decode("utf-8-sig"), source["id"])
        if not isinstance(manifest, dict) or manifest.get("id") != source["id"] or manifest.get("repository") != source["repository"]:
            raise RegistryError(f"manifest/source identity mismatch: {source['id']}")
        snapshot = f"snapshots/{source['id']}.yaml"
        snapshots[snapshot] = data
        locked.append({**source, **provenance, "snapshot": snapshot, "sha256": sha256(data)})
        entries.append({"manifest": manifest, "root": root, "provenance": provenance})
    # Complete validation happens before any snapshot or lock is touched.
    require_valid(entries)
    for relative, data in snapshots.items():
        target = confined(Path(sources).parent, relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    (Path(sources).parent / "snapshots.lock.json").write_text(json_text({"schema_version": VERSION, "sources": locked}), encoding="utf-8", newline="\n")
    return len(entries)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", type=Path, default=ROOT / "sources/repositories.yaml")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--checkouts", type=Path, help="capture sibling manifests with local Git provenance")
    mode.add_argument("--remote", action="store_true", help="opt in to fetching source refs, resolved once to immutable GitHub commits")
    args = parser.parse_args(argv)
    try:
        count = refresh(args.sources, args.checkouts, args.remote)
        print(f"Refreshed {count} snapshots; review provenance and generated diff before committing")
    except (RegistryError, OSError, UnicodeError, ValueError, KeyError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
