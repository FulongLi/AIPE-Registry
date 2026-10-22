# AIPE — Registry

AIPE Registry is the capability index of **AI for Power Engineering**. Every
canonical AIPE repository describes itself in an `aipe.yaml` manifest; Registry
validates those manifests against one JSON Schema, pins the exact bytes it read,
and builds a deterministic machine-readable index (`generated/aipe.json`) and an
agent-readable index (`generated/aipe.md`) that the AIPE website and coding
agents consume. Engineering schemas belong to
[AIPE-Core](https://github.com/FulongLi/AIPE-Core); the wider open-source tool
landscape is curated separately in the
[awesome catalogue](https://github.com/FulongLi/awesome-open-source-power-electronics).

## Features

- Normative capability-manifest schema (JSON Schema 2020-12, version 0.1.0)
  with namespaced extensions
- Offline, deterministic build: no timestamps, machine paths or network
  responses in the generated index
- Fail-closed validation: missing files, duplicate IDs, unknown or cyclic
  dependencies, incompatible versions and tampered snapshots stop the build
  before anything is written
- SHA-256-pinned manifest snapshots (`sources/snapshots.lock.json`) with
  recorded commit and dirty-tree provenance
- Read-only audit diagnostics: stale repositories, unresolved licences,
  documentation drift, connector versions and opt-in link checks
- Never executes connectors or engineering tools and never rewrites a source
  repository

## Installation

Python 3.10 or newer.

```sh
python -m pip install -r requirements-dev.txt
```

## Usage

Validate the checked-in manifest snapshots, confirm that the generated index is
current, and run the tests. The normal build performs no network requests.

```sh
python scripts/validate.py
python scripts/build_registry.py --check
python -m pytest -q
```

Rules for writing an `aipe.yaml`, validating a multi-repository change against
sibling checkouts, refreshing snapshots and auditing the index are in the
documentation below.

## Project Information

- Version: 0.1.0 (capability-manifest schema version and `aipe.yaml`
  `schema_version`; there is no packaged release)
- Status: Prototype (`aipe.yaml`: status `experimental`, maturity `prototype`)
- Developer: Fulong Li
- Organisation: Spirit Connect / AIPE Labs
- License: MIT ([LICENSE](LICENSE)); indexed repositories keep their own
  licences, recorded as SPDX identifiers or `NOASSERTION`

## Documentation

- [Authoring and validating a capability manifest](docs/manifest-authoring.md)
- [Building, refreshing and auditing the registry](docs/development.md)
- [Capability manifest schema](schema/capability-manifest.schema.json)
- [Source repositories](sources/repositories.yaml) and
  [snapshot lock](sources/snapshots.lock.json)
- Generated index: [aipe.json](generated/aipe.json) · [aipe.md](generated/aipe.md)
- [CONTRIBUTING.md](CONTRIBUTING.md)
