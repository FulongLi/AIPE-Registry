# AIPE Registry

AIPE means **AI for Power Engineering**. Registry discovers the capabilities of
the eleven canonical AIPE repositories. It describes inputs, outputs, dependencies,
tool accessibility and integration maturity. Engineering schemas and contracts
belong to [AIPE-Core](https://github.com/FulongLi/AIPE-Core).

The [awesome catalogue](https://github.com/FulongLi/awesome-open-source-power-electronics)
curates the wider engineering-tool ecosystem. Registry indexes AIPE's declared
capabilities and supported/evaluated integrations; it does not copy that catalogue.

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
without published PRs are labeled publication pending instead of linking missing
default-branch documents.

All configured sources are required. Missing files, invalid manifests, duplicate
IDs, unknown dependencies, required dependency cycles, incompatible versions,
source identity drift and tampered snapshots fail before writing generated files.
There is no successful partial index mode. A failed build leaves existing output
untouched; consumers must check the exit code before publishing it.

## Author and validate a manifest

Each repository owns `aipe.yaml`. The normative contract is
[`schema/capability-manifest.schema.json`](schema/capability-manifest.schema.json),
JSON Schema 2020-12, version `0.1.0`. Unknown fields are errors; domain additions
use a namespaced `extensions` key. YAML must use JSON-compatible scalar values,
unique string keys and quoted dates. Custom tags, recursive aliases and nonfinite
numbers are rejected.

`repository` always names the canonical upstream, even in a fork. `license` is an
SPDX identifier/expression or `NOASSERTION` where rights are unresolved. The
validator does not claim to audit SPDX expressions or legal ownership. New
Registry code proposes MIT; other repositories' rights are not changed.

`compatibility.core` and `compatibility.engineering_state` identify the understood
`0.1.x` contract family. `integration` is `native`, `mapped`, or `none`:
documentation mapping alone is `mapped`; `none` does not claim state IO. A matching
version is not proof of an executed adapter or physically validated result.
Dependencies reference Registry IDs with version `0.1.x`; external tools and
connectors belong in their dedicated arrays. Required dependencies must be acyclic;
optional dependencies still need known IDs.

Tool `licence_class` distinguishes `open_source`, `free_proprietary`, `commercial`.
Proprietary integrations are optional at repository level. Skill-specific required
licences must be stated in the skill's own metadata. Capability overlap does not
establish physical fidelity or a one-to-one tool replacement. Connector `evaluated`
does not mean installed, trusted, or supported; record licence, versions, platforms
and security notes. Registry never executes connectors or engineering tools.

For a multi-repository change with all siblings under `../`:

```sh
python scripts/validate.py --checkouts ../ --today 2026-10-07
python scripts/discover.py --checkouts ../ --output discovered.json
python scripts/build_registry.py --checkouts ../ --output-dir staging
```

Explicit files are also supported: `python scripts/validate.py ../AIPE-Core/aipe.yaml
aipe.yaml`. Include the complete dependency set. Local checkout validation checks
documentation and evidence files remain within the repository and actually exist.
Snapshot-only validation checks path safety but cannot establish file existence.

## Refresh sources and provenance

[`sources/repositories.yaml`](sources/repositories.yaml) declares every canonical
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
Dirty snapshots are labeled, never falsely attributed to that commit. Every
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
specialized tools are never deleted automatically.

```sh
python scripts/validate.py --checkouts ../ --stale-days 365 --today 2026-10-07
python scripts/validate.py --check-links
```

Network link checks are opt-in, bounded per request, and report HTTP/transport
failures as warnings; authentication, anti-bot rules and rate limits can cause
false positives. Offline CI does not depend on third-party uptime. `--warnings-as-errors`
enables stricter audit policy. Each CLI supports `--help`. Future agents may propose
changes through reviewed PRs; no discovery or audit command rewrites source repos.
