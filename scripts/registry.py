"""Shared discovery/validation. No network calls happen without an explicit flag."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"


class RegistryError(ValueError):
    """Input cannot produce a complete, trustworthy registry."""


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys instead of silently taking the last one."""


# YAML 1.2 treats words such as on/off/yes/no as strings, not booleans.
UniqueLoader.yaml_implicit_resolvers = {
    key: [(tag, pattern) for tag, pattern in values if tag != 'tag:yaml.org,2002:bool']
    for key, values in yaml.SafeLoader.yaml_implicit_resolvers.items()
}
UniqueLoader.add_implicit_resolver('tag:yaml.org,2002:bool', re.compile(r'^(?:true|True|TRUE|false|False|FALSE)$'), list('tTfF'))


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise RegistryError("YAML object keys must be strings")
        if key in result:
            raise RegistryError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _json_values(value, seen=None):
    seen = set() if seen is None else seen
    if isinstance(value, (list, dict)):
        if id(value) in seen:
            raise RegistryError("recursive YAML aliases are unsupported")
        seen.add(id(value))
        for item in (value.values() if isinstance(value, dict) else value):
            _json_values(item, seen)
        seen.remove(id(value))
    elif value is not None and type(value) not in (str, bool, int, float):
        raise RegistryError("only JSON-compatible YAML values are supported; quote dates")
    elif isinstance(value, float) and not math.isfinite(value):
        raise RegistryError("non-finite numbers are unsupported")


def parse_yaml(data, label="input"):
    try:
        value = yaml.load(data, Loader=UniqueLoader)
        _json_values(value)
        return value
    except (yaml.YAMLError, RegistryError) as exc:
        raise RegistryError(f"{label}: {exc}") from exc


def read_yaml(path):
    try:
        return parse_yaml(Path(path).read_text(encoding="utf-8-sig"), str(path))
    except OSError as exc:
        raise RegistryError(str(exc)) from exc


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def confined(root, relative):
    """Do not permit manifest paths, symlinks, or documentation to escape a root."""
    if not isinstance(relative, str) or re.match(r"^[A-Za-z]+:", relative) or "\\" in relative:
        raise RegistryError(f"not a repository-relative path: {relative}")
    root = Path(root).resolve()
    candidate = (root / unquote(relative)).resolve()
    if not candidate.is_relative_to(root):
        raise RegistryError(f"path escapes repository: {relative}")
    return candidate


def source_records(path=ROOT / "sources/repositories.yaml"):
    document = read_yaml(path)
    if not isinstance(document, dict) or set(document) != {"schema_version", "repositories"} or document["schema_version"] != VERSION:
        raise RegistryError("invalid sources document or schema_version")
    records = document["repositories"]
    if not isinstance(records, list) or not records:
        raise RegistryError("sources must contain at least one repository")
    ids, repos = set(), set()
    for record in records:
        required = {"id", "repository", "ref", "state", "path"}
        if not isinstance(record, dict) or set(record) != required or not all(isinstance(v, str) for v in record.values()):
            raise RegistryError(f"invalid source record: {record}")
        if not re.fullmatch(r"[a-z][a-z0-9-]*(\.[a-z][a-z0-9-]*)+", record["id"]):
            raise RegistryError(f"invalid source ID: {record['id']}")
        if not re.fullmatch(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", record["repository"]):
            raise RegistryError(f"invalid source repository: {record['repository']}")
        if record["state"] not in {"pinned", "pending_pr"} or not record["ref"]:
            raise RegistryError("source must declare pinned or pending_pr state and a ref")
        if record["state"] == "pinned" and not re.fullmatch(r"[a-f0-9]{40}", record["ref"]):
            raise RegistryError("pinned source ref must be an immutable 40-character commit")
        confined(Path(path).parent, record["path"])
        if record["id"] in ids or record["repository"] in repos:
            raise RegistryError(f"duplicate source ID or repository: {record['id']}")
        ids.add(record["id"])
        repos.add(record["repository"])
    return sorted(records, key=lambda item: item["id"])


def git_info(root, manifest_path):
    def git(*args):
        completed = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)
        if completed.returncode:
            raise RegistryError(f"cannot inspect Git provenance in {root}: {completed.stderr.strip()}")
        return completed.stdout.strip()
    return {"commit": git("rev-parse", "HEAD"),
            "committed_at": git("log", "-1", "--format=%cI"),
            "manifest_dirty": bool(git("status", "--porcelain", "--", manifest_path))}


def discover(sources=ROOT / "sources/repositories.yaml", checkouts=None):
    records = source_records(sources)
    result = []
    lock = None
    if checkouts is None:
        lock_path = Path(sources).parent / "snapshots.lock.json"
        lock = read_yaml(lock_path)
        if not isinstance(lock, dict) or lock.get("schema_version") != VERSION or not isinstance(lock.get("sources"), list):
            raise RegistryError("invalid snapshot lock")
        required_lock_fields = {'id', 'repository', 'ref', 'state', 'path', 'commit', 'committed_at', 'manifest_dirty', 'origin', 'snapshot', 'sha256'}
        for item in lock['sources']:
            if not isinstance(item, dict) or set(item) != required_lock_fields:
                raise RegistryError('invalid snapshot provenance fields')
            if not isinstance(item['commit'], str) or not re.fullmatch(r'[a-f0-9]{40}', item['commit']):
                raise RegistryError('snapshot provenance requires an immutable commit')
            if not isinstance(item['sha256'], str) or not re.fullmatch(r'[a-f0-9]{64}', item['sha256']):
                raise RegistryError('snapshot provenance requires a SHA-256 digest')
            if type(item['manifest_dirty']) is not bool or item['origin'] not in {'local_checkout', 'remote'}:
                raise RegistryError('invalid snapshot origin/dirty flag')
        locked = {item["id"]: item for item in lock["sources"]}
        if len(locked) != len(lock["sources"]) or set(locked) != {r["id"] for r in records}:
            raise RegistryError("snapshot lock does not exactly cover configured sources")
    for source in records:
        if checkouts is not None:
            root = Path(checkouts).resolve() / source["repository"].rsplit("/", 1)[1]
            path = confined(root, source["path"])
            manifest = read_yaml(path)
            provenance = {**source, **git_info(root, source["path"])}
        else:
            root = None
            provenance = locked[source["id"]]
            for field in ("repository", "ref", "path", "state"):
                if provenance.get(field) != source[field]:
                    raise RegistryError(f"source/lock {field} drift: {source['id']}; refresh snapshots")
            path = confined(Path(sources).parent, provenance["snapshot"])
            try:
                data = path.read_bytes()
            except OSError as exc:
                raise RegistryError(str(exc)) from exc
            if sha256(data) != provenance.get("sha256"):
                raise RegistryError(f"snapshot hash mismatch: {source['id']}")
            manifest = parse_yaml(data.decode("utf-8-sig"), str(path))
        if not isinstance(manifest, dict) or manifest.get("id") != source["id"] or manifest.get("repository") != source["repository"]:
            raise RegistryError(f"manifest/source identity mismatch: {source['id']}")
        result.append({"manifest": manifest, "root": root, "provenance": provenance})
    return result


def validate(entries, today=None, stale_days=365, check_links=False):
    schema = json.loads((ROOT / "schema/capability-manifest.schema.json").read_text(encoding="utf-8"))
    checker = FormatChecker()
    if 'uri' not in checker.checkers:
        raise RegistryError('URI format validation is unavailable; install requirements-dev.txt with jsonschema[format]')
    validator = Draft202012Validator(schema, format_checker=checker)
    diagnostics = []

    def report(severity, code, ident, message):
        diagnostics.append({"severity": severity, "code": code, "id": ident, "message": message})

    valid = []
    for entry in entries:
        manifest = entry["manifest"]
        ident = manifest.get("id", "<unknown>") if isinstance(manifest, dict) else "<unknown>"
        errors = list(validator.iter_errors(manifest))
        for error in errors:
            pointer = "/" + "/".join(str(part) for part in error.absolute_path)
            report("error", "schema", ident, f"{pointer}: {error.message}")
        if not errors:
            valid.append(entry)
    ids, repos, capabilities, graph = {}, {}, {}, {}
    today = today or dt.date.today()
    urls = {}
    for entry in valid:
        manifest, root = entry["manifest"], entry.get("root")
        ident = manifest["id"]
        if ident in ids:
            report("error", "duplicate_id", ident, "capability IDs must be unique")
        if manifest["repository"] in repos:
            report("error", "duplicate_repository", ident, "one canonical manifest per repository is required")
        ids[ident], repos[manifest["repository"]] = manifest, ident
        graph[ident] = [d["id"] for d in manifest["dependencies"] if not d["optional"]]
        for capability in manifest["capabilities"]:
            capabilities.setdefault(capability, []).append(ident)
        for kind in ("tools", "connectors", "dependencies"):
            values = [item["id"] for item in manifest[kind]]
            if len(values) != len(set(values)):
                report("error", "duplicate_member", ident, f"duplicate IDs in {kind}")
        tool_ids = {t["id"] for t in manifest["tools"]}
        open_capabilities = {c for t in manifest["tools"] if t["licence_class"] == "open_source" for c in t["capabilities"]}
        for tool in manifest["tools"]:
            urls.setdefault(tool["url"], []).append(ident)
            if not tool["interfaces"]:
                report("warning", "unsupported_tool", ident, f"{tool['id']} declares no automation interface")
            if tool["licence_class"] != "open_source":
                missing = sorted(set(tool["capabilities"]) - open_capabilities)
                if missing:
                    report("warning", "missing_open_alternative", ident, f"{tool['id']}: {', '.join(missing)}; review fidelity and limitations")
        for connector in manifest["connectors"]:
            if connector["tool"] not in tool_ids:
                report("error", "unsupported_connector_tool", ident, f"{connector['id']} references unknown tool {connector['tool']}")
            urls.setdefault(connector["repository"], []).append(ident)
            if connector["status"] == "supported" and not connector["supported_versions"]:
                report("warning", "unversioned_connector", ident, connector["id"])
        references = manifest["documentation"] + manifest["validation"]["evidence"]
        for reference in references:
            if reference.startswith("https://"):
                urls.setdefault(reference, []).append(ident)
            else:
                try:
                    # Even snapshots reject traversal; existence needs a checkout.
                    reference_path = urlsplit(reference).path
                    path = confined(root or ROOT, reference_path)
                    if root and not path.is_file():
                        report("error", "documentation_drift", ident, f"missing file: {reference}")
                except RegistryError as exc:
                    report("error", "unsafe_reference", ident, str(exc))
        provenance = entry.get("provenance", {})
        if provenance.get("committed_at"):
            try:
                committed = dt.datetime.fromisoformat(provenance["committed_at"].replace("Z", "+00:00")).date()
                if (today - committed).days > stale_days:
                    report("warning", "stale_repository", ident, f"last observed commit {committed}; review activity, do not auto-delete")
            except ValueError:
                report("error", "invalid_provenance", ident, "invalid committed_at timestamp")
        if provenance.get("manifest_dirty"):
            report("warning", "uncommitted_snapshot", ident, "manifest bytes are hash-pinned but not committed at the observed Git revision")
        if manifest["status"] == "deprecated":
            report("warning", "legacy_replacement", ident, "review replacement/migration documentation before use")
        if manifest["license"] == "NOASSERTION":
            report("warning", "unresolved_license", ident, "rights remain unconfirmed; no open-source licence inferred")
    for ident, manifest in sorted(ids.items()):
        for dependency in manifest["dependencies"]:
            target = ids.get(dependency["id"])
            if target is None:
                report("error", "unknown_dependency", ident, dependency["id"])
            elif not target["schema_version"].startswith(dependency["version"].removesuffix("x")):
                report("error", "dependency_conflict", ident, f"incompatible dependency: {dependency['id']}")
    # Detect required-dependency cycles once per cycle component.
    visited, active, cycles = set(), [], set()

    def visit(ident):
        if ident in active:
            cycles.add(tuple(sorted(active[active.index(ident):])))
            return
        if ident in visited:
            return
        active.append(ident)
        for target in sorted(graph.get(ident, [])):
            visit(target)
        active.pop()
        visited.add(ident)

    for ident in sorted(graph):
        visit(ident)
    for cycle in sorted(cycles):
        report("error", "dependency_cycle", cycle[0], ", ".join(cycle))
    for capability, owners in sorted(capabilities.items()):
        if len(owners) > 1:
            report("warning", "duplicate_capability", owners[0], f"{capability}: {', '.join(sorted(owners))}; may be intentional alternatives")
    if check_links:
        for url, owners in sorted(urls.items()):
            try:
                request = Request(url, headers={"User-Agent": "AIPE-Registry/0.1", "Range": "bytes=0-0"})
                with urlopen(request, timeout=10) as response:
                    response.read(1)
            except Exception as exc:  # Maintenance failures are reported, never rewritten.
                report("warning", "dead_link", sorted(owners)[0], f"{url}: {type(exc).__name__}: {exc}")
    return sorted(diagnostics, key=lambda d: (d["severity"], d["id"], d["code"], d["message"]))


def require_valid(entries, **kwargs):
    diagnostics = validate(entries, **kwargs)
    errors = [d for d in diagnostics if d["severity"] == "error"]
    if errors:
        raise RegistryError("validation failed; no output written:\n" + "\n".join(f"{d['id']} [{d['code']}] {d['message']}" for d in errors))
    return diagnostics


def document(entries):
    return {"schema_version": VERSION, "capabilities": sorted([e["manifest"] for e in entries], key=lambda m: m["id"])}


def markdown(payload, provenance=None):
    def escape(value):
        return str(value).replace("&", "&amp;").replace("<", "&lt;").replace("|", "\\|").replace("\n", " ")
    lines = ["# AIPE — AI for Power Engineering", "", "Generated from validated capability manifests. Open-source first, commercial compatible.", "", "| Capability | Type | Maturity | Integration | Canonical repository |", "| --- | --- | --- | --- | --- |"]
    for m in payload["capabilities"]:
        lines.append(f"| {escape(m['name'])} (`{m['id']}`) | {m['type']} | {m['maturity']} | {m['compatibility']['integration']} | [Repository]({m['repository']}) |")
    for m in payload["capabilities"]:
        lines += ["", f"## {escape(m['name'])}", "", escape(m["description"]), "", f"Capabilities: {', '.join(m['capabilities'])}.", "", f"Licence: `{escape(m['license'])}`. Validation: `{m['validation']['status']}`.", ""]
        for tool in sorted(m["tools"], key=lambda t: t["id"]):
            lines.append(f"- [{escape(tool['name'])}]({tool['url']}): {tool['licence_class']}; {'optional' if tool['optional'] else 'required'}; interfaces: {', '.join(tool['interfaces']) or 'none declared'}.")
        for limitation in m["validation"]["limitations"]:
            lines.append(f"- Limitation: {escape(limitation)}")
        for ref in m["documentation"]:
            source = (provenance or {}).get(m['id'])
            if not ref.startswith('https://') and source and source.get('state') == 'pending_pr' and not source.get('ref', '').startswith('refs/pull/'):
                lines.append(f"- Documentation staged locally (publication pending): `{escape(ref)}`")
                continue
            revision = source['commit'] if source else 'HEAD'
            url = ref if ref.startswith("https://") else f"{m['repository']}/blob/{revision}/{ref}"
            lines.append(f"- [Documentation: {escape(ref)}]({url})")
    return "\n".join(lines).rstrip() + "\n"
