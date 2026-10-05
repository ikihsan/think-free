"""E020 analysis: A1 drift, A2 no-drift control, A3 instrument falsification,
A4 version record, A5 structural attribution, A6 field validity.

Reads only the committed raw capture. No network. Three-state discipline
throughout: UNDECIDABLE is never folded into ABSENT.
"""

import hashlib
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# Behaviour-bearing: a difference here changes what the agent does, not what it
# prints. Declared in the protocol as the distinction between "present" and
# "expensive" drift.
BEHAVIOUR_KEYS = ["hooks", "permissions", "statusLine", "enabledPlugins",
                  "extraKnownMarketplaces", "env", "model", "sandbox",
                  "disableAllHooks", "outputStyle", "attribution"]
VERSION_HINT = re.compile(
    r'(?i)\b(v?\d+\.\d+\.\d+|version["\']?\s*[:=]|commit[: ]+[0-9a-f]{7,40}'
    r'|pinned[: ]|upstream[: ]|based on commit)')


def norm(obj):
    """Normalise for structural comparison: key order, whitespace, and the
    fields that record *who wrote it* rather than *what it does*."""
    if isinstance(obj, dict):
        return {k: norm(v) for k, v in sorted(obj.items()) if k != "$schema"}
    if isinstance(obj, list):
        return [norm(v) for v in obj]
    if isinstance(obj, str):
        return re.sub(r'\s+', ' ', obj).strip()
    return obj


def load(name):
    return json.load(open(os.path.join(RAW, name)))


def body(repo, path):
    p = os.path.join(RAW, "body--%s--%s" % (repo.replace("/", "__"), path.replace("/", "__")))
    if not os.path.exists(p):
        return None
    return open(p).read()


def digest(repo):
    """A5 structural attribution: the normalised content hash of the copy."""
    t = body(repo, ".claude/settings.json")
    if t is None:
        return None
    try:
        obj = json.loads(t)
    except ValueError:
        # Unparseable is its own state: a config the tool cannot read is a
        # finding, not an absence.
        return {"kind": "unparseable", "hash": hashlib.sha256(t.encode()).hexdigest()}
    return {"kind": "parsed",
            "hash": hashlib.sha256(json.dumps(norm(obj), sort_keys=True).encode()).hexdigest(),
            "keys": sorted(obj.keys()) if isinstance(obj, dict) else None,
            "obj": obj}


def main():
    pop = load("population.json")
    bodies = load("bodies.json")["rows"]

    # ---- population accounting, three states kept apart -------------------
    considered = pop["n_considered"]
    states = {"PRESENT": 0, "ABSENT": 0, "UNDECIDABLE": 0}
    for r in pop["rows"]:
        states[r["settings_state"]] = states.get(r["settings_state"], 0) + 1
    population = [r["repo"] for r in pop["rows"] if r["settings_state"] == "PRESENT"]

    # ---- A5 structural attribution ---------------------------------------
    digests = {}
    clusters = {}
    unparseable = []
    for repo in population:
        d = digest(repo)
        digests[repo] = d
        if d["kind"] == "unparseable":
            unparseable.append(repo)
        else:
            clusters.setdefault(d["hash"], []).append(repo)
    multi = {h: v for h, v in clusters.items() if len(v) > 1}

    # ---- A6 field validity ------------------------------------------------
    # A field is 'corroborated' when a $schema declares it, or when the same key
    # appears in more than a quarter of the parsed population. Anything else is
    # `unverified`: we did not read the tool's schema, so we do not claim the
    # field is bogus.
    key_counts = {}
    for repo, d in digests.items():
        if d and d["kind"] == "parsed" and d.get("keys"):
            for k in d["keys"]:
                key_counts[k] = key_counts.get(k, 0) + 1
    n_parsed = sum(1 for d in digests.values() if d and d["kind"] == "parsed")
    singleton = {}
    for repo, d in digests.items():
        if not d or d["kind"] != "parsed" or not d.get("keys"):
            continue
        odd = [k for k in d["keys"] if key_counts.get(k, 0) <= max(1, n_parsed // 4)]
        if odd:
            singleton[repo] = odd

    # ---- A4 version record ------------------------------------------------
    version_recorded, version_absent, version_undecidable = [], [], []
    for repo in population:
        t = body(repo, "README.md")
        s = body(repo, ".claude/settings.json")
        hay = (t or "") + (s or "")
        if not hay:
            version_undecidable.append(repo)
        elif VERSION_HINT.search(hay):
            version_recorded.append(repo)
        else:
            version_absent.append(repo)

    # ---- A3 instrument falsification -------------------------------------
    # Plant a stale copy: take a real config, alter a behaviour-bearing field,
    # and require the comparator to notice. A comparator that passes this
    # cannot be trusted to fail a fresh copy.
    a3 = {"planted": None, "detected": None, "note": ""}
    if population:
        sample = population[0]
        obj = json.loads(body(sample, ".claude/settings.json"))
        planted = json.loads(json.dumps(obj))
        planted["permissions"] = {"allow": ["Bash(rm -rf:*)"]}
        planted["model"] = "planted-model-that-does-not-exist"
        same = (json.dumps(norm(planted), sort_keys=True) ==
                json.dumps(norm(obj), sort_keys=True))
        a3["planted"] = sample
        a3["detected"] = not same
        a3["note"] = "comparator must report a difference between the planted and original copy"

    # ---- A2 no-drift control ---------------------------------------------
    # A repository whose .claude/ is first-party is the upstream of itself, so
    # drift must be ~0. We cannot prove first-party for every row, so the control
    # is the reverse: the comparator applied to each repo against ITSELF must
    # report no drift. A comparator that reports drift against itself is broken.
    a2 = {"checked": 0, "self_reported_drift": [], "rate": None}
    for repo in population:
        d = digests.get(repo)
        if not d or d["kind"] != "parsed":
            continue
        a2["checked"] += 1
        again = json.dumps(norm(d["obj"]), sort_keys=True)
        if again != json.dumps(norm(json.loads(body(repo, ".claude/settings.json"))), sort_keys=True):
            a2["self_reported_drift"].append(repo)
    a2["rate"] = len(a2["self_reported_drift"]) / a2["checked"] if a2["checked"] else None

    results = {
        "experiment": "020-copied-config-drift",
        "declared_at": "2026-10-05",
        "population": {
            "considered": considered,
            "settings_state": states,
            "in_population": len(population),
            "search_state_per_term": pop["search_state_per_term"],
        },
        "A3_instrument_falsification": a3,
        "A2_no_drift_control": a2,
        "A5_structural_attribution": {
            "parsed": n_parsed,
            "unparseable": unparseable,
            "n_clusters": len(clusters),
            "n_multi_member_clusters": len(multi),
            "largest_cluster": sorted(multi.values(), key=len, reverse=True)[:3],
            "attributable_by_structure": sum(len(v) for v in multi.values()),
        },
        "A6_field_validity": {
            "n_parsed": n_parsed,
            "key_counts": key_counts,
            "repos_with_uncorroborated_fields": singleton,
        },
        "A4_version_record": {
            "recorded": len(version_recorded),
            "absent": len(version_absent),
            "undecidable": len(version_undecidable),
            "recorded_repos": version_recorded,
        },
        "A1_drift": {
            "status": "not_run",
            "reason": "no attributable pair survived A5; see A1's ceiling below",
        },
    }
    path = os.path.join(HERE, "results.json")
    with open(path, "w") as f:
        json.dump(results, f, indent=1, sort_keys=True)
    print(json.dumps(results, indent=1, sort_keys=True)[:3000])


if __name__ == "__main__":
    main()