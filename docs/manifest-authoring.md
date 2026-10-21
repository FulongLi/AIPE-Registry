# Authoring and validating a capability manifest

Each AIPE repository owns an `aipe.yaml`. The normative contract is
[`schema/capability-manifest.schema.json`](../schema/capability-manifest.schema.json),
JSON Schema 2020-12, version `0.1.0`. Unknown fields are errors; domain additions
use a namespaced `extensions` key. YAML must use JSON-compatible scalar values,
unique string keys and quoted dates. Custom tags, recursive aliases and nonfinite
numbers are rejected.

## Identity and licence

`repository` always names the canonical upstream, even in a fork. `license` is an
SPDX identifier/expression or `NOASSERTION` where rights are unresolved. The
validator does not claim to audit SPDX expressions or legal ownership. Registry
code is MIT; other repositories' rights are not changed by being indexed.

## Compatibility and dependencies

`compatibility.core` and `compatibility.engineering_state` identify the understood
`0.1.x` contract family. `integration` is `native`, `mapped`, or `none`:
documentation mapping alone is `mapped`; `none` does not claim state IO. A matching
version is not proof of an executed adapter or physically validated result.

Dependencies reference Registry IDs with version `0.1.x`; external tools and
connectors belong in their dedicated arrays. Required dependencies must be acyclic;
optional dependencies still need known IDs.

## Tools and connectors

Tool `licence_class` distinguishes `open_source`, `free_proprietary`, `commercial`.
Proprietary integrations are optional at repository level. Skill-specific required
licences must be stated in the skill's own metadata. Capability overlap does not
establish physical fidelity or a one-to-one tool replacement. Connector `evaluated`
does not mean installed, trusted, or supported; record licence, versions, platforms
and security notes. Registry never executes connectors or engineering tools.

## Validating manifests

The checked-in snapshots:

```sh
python scripts/validate.py
```

For a multi-repository change with all sibling checkouts under `../` (the layout
used by the AIPE workspace), or with explicit files:

```sh
python scripts/validate.py --checkouts ../ --today 2026-10-07
python scripts/discover.py --checkouts ../ --output discovered.json
python scripts/build_registry.py --checkouts ../ --output-dir staging
python scripts/validate.py ../AIPE-Core/aipe.yaml aipe.yaml
```

Include the complete dependency set. Local checkout validation checks that
documentation and evidence files remain within the repository and actually exist.
Snapshot-only validation checks path safety but cannot establish file existence.
Each CLI supports `--help`.
