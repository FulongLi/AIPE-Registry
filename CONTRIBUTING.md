# Contributing

1. Change the canonical repository's `aipe.yaml` in a reviewed PR. Preserve honest
   maturity, validation evidence and tool limitations; never fabricate measurements.
2. Validate the complete dependency set against the Registry manifest schema.
3. Add or update a source record and explicitly refresh snapshots. Review every
   provenance/hash change; use immutable upstream SHAs once related PRs merge.
4. Run `python -m pytest -q`, `python scripts/validate.py`, and
   `python scripts/build_registry.py --check`. If generation should change, first
   run without `--check` and review both JSON and Markdown.
5. Open a PR; do not auto-merge. Generated artifacts are derivatives, not authority
   for rewriting a repository's source manifest.

Schema evolution must remain explicit. Core owns engineering data structures;
Registry owns capability metadata. Keep network access optional and generation
deterministic. CI runs only the checked-in snapshot set, independent of mutable
remote branches and local checkout layout.
