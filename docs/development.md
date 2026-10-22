# Building, refreshing and auditing the registry

## Reproduce the registry offline

Python 3.10 or newer is required. After installing the development dependencies,
the normal build performs no network requests:

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python scripts/build_registry.py
python scripts/build_registry.py --check
python -m pytest -q
```

`generated/aipe.json` contains exactly `schema_version` and `capabilities` (complete
manifest objects, sorted by ID). `generated/aipe.md` is the human/agent-readable
index. Neither embeds build times, machine paths, or mutable network responses.
Website builds consume these artifacts; visitors need no GitHub connection.
Markdown documentation links use the observed source commit. Local staging refs
without published PRs are labelled publication pending instead of linking missing
default-branch documents.

All configured sources are required. Missing files, invalid manifests, duplicate
IDs, unknown dependencies, required dependency cycles, incompatible versions,
source identity drift and tampered snapshots fail before writing generated files.
There is no successful partial index mode. A failed build leaves existing output
untouched; consumers must check the exit code before publishing it.

## Refresh sources and provenance

[`sources/repositories.yaml`](../sources/repositories.yaml) declares every canonical
repository, expected ID, manifest path and ref. `pinned` refs must be full commit
SHAs; `pending_pr` refs explicitly label staging work. To publish after review,
update records to upstream merged commit SHAs and `state: pinned`, then refresh.

```sh
# Capture exact working-tree bytes for a coordinated, unmerged change:
python scripts/refresh.py --checkouts ../
# Or explicitly opt in to remote refresh:
python scripts/refresh.py --remote
python scripts/build_registry.py
python scripts/build_registry.py --check
```

Remote refresh first resolves each declared ref to a GitHub commit and downloads
the manifest from that immutable commit. It only reads public GitHub repositories;
it does not use credentials, open PRs or write upstream. Pending branches on forks
must first become accessible through a canonical PR ref (`refs/pull/N/head`) or
an upstream commit; an unavailable ref fails the complete refresh.

Local refresh records the observed Git HEAD and whether the manifest is dirty.
Dirty snapshots are labelled, never falsely attributed to that commit. Every
snapshot's exact bytes are SHA-256 pinned in `sources/snapshots.lock.json`, so the
offline build remains reproducible even during cross-repository PR staging. Review
the lock's `origin`, `commit`, `manifest_dirty`, `committed_at` and hash alongside
the snapshot diff. Refresh validates every input before changing snapshots.
The lock is written last; an interrupted refresh fails hash verification.

## Read-only maintenance

`validate.py` emits structured diagnostics: missing/invalid manifests, stale
repositories, unresolved licences, duplicate capabilities, dependency conflicts,
connector references/versions, documentation drift, deprecated replacements and
missing declared open alternatives. Overlap/staleness are review hints; old or
specialised tools are never deleted automatically.

```sh
python scripts/validate.py --checkouts ../ --stale-days 365 --today 2026-10-07
python scripts/validate.py --check-links
```

Network link checks are opt-in, bounded per request, and report HTTP/transport
failures as warnings; authentication, anti-bot rules and rate limits can cause
false positives. Offline CI does not depend on third-party uptime.
`--warnings-as-errors` enables stricter audit policy. Each CLI supports `--help`.
Future agents may propose changes through reviewed PRs; no discovery or audit
command rewrites source repositories.

## Relationship to the wider ecosystem

Registry discovers the capabilities of the canonical AIPE repositories: inputs,
outputs, dependencies, tool accessibility and integration maturity. Engineering
schemas and contracts belong to [AIPE-Core](https://github.com/FulongLi/AIPE-Core).
The [awesome catalogue](https://github.com/FulongLi/awesome-open-source-power-electronics)
curates the wider engineering-tool ecosystem; Registry indexes AIPE's declared
capabilities and supported/evaluated integrations and does not copy that catalogue.
