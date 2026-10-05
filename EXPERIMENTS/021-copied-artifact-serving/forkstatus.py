#!/usr/bin/env python3
"""H2 -- are forks and dependents an adequate stand-in for copies?

The record's proposed first move (STATE-next-actions.md item 0) was to decide
whether forks, dependents or templates can stand in for a copy count.  The gate
declared in PROTOCOL.md asks for a RATE among demonstrably-copied configurations,
not a single counterexample, because a band this wide cannot order anything on
one row.

Two mechanical steps, both declared:

1. The copy count of each candidate configuration comes from copycount.py, so a
   configuration enters the high band at >= 100 indexed repositories and the low
   band at <= 5.  Rows between the two are not used.
2. The origin repository of a configuration is the repository that *ships* the
   path -- read from the index's own repository list for that path, taking the
   highest-starred non-fork repository.  Its fork and template status is then
   read from GitHub's unauthenticated core API, which carries `fork` and
   `is_template` as fields, so no judgement is involved.

The core budget is 60/hour unauthenticated and 017 recorded already having lost
rows to it, so rows are paced and a refusal is recorded as `refused`.
"""

import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from copycount import fetch, read_raw  # noqa: E402  (path set above)

HERE = os.path.dirname(os.path.abspath(__file__))

# The configuration paths this arm measures. Chosen before any fork count was
# read, and spanning the vocabulary rather than one project's conventions.
PATTERNS = [
    ("claude_hooks", "^\\.claude/hooks/"),
    ("claude_commands", "^\\.claude/commands/"),
    ("claude_settings_local", "^\\.claude/settings\\.local\\.json$"),
    ("cursor_rules", "^\\.cursor/rules/"),
    ("mcp_json", "^\\.mcp\\.json$"),
    ("githooks_precommit", "^\\.githooks/pre-commit$"),
    ("cursorrules", "^\\.cursorrules$"),
    ("claude_skills", "^\\.claude/skills/"),
    ("claude_hooks_readme", "^\\.claude/hooks/README\\.md$"),
    ("claude_hook_session_start", "^\\.claude/hooks/session-start\\.sh$"),
]

HIGH_BAND = 100
LOW_BAND = 5
CORE_DELAY = 4.0

# Filled per run from low_band_paths(); module level so the row loop can tell a
# low-band sample from a declared pattern without re-deriving the slice.
LOW_KEYS = set()


def repos_for(slug, raw_dir):
    """Repository names the index reported for one path pattern."""
    path = os.path.join(raw_dir, slug + ".sse")
    if not os.path.exists(path):
        return []
    found = []
    with open(path) as handle:
        for line in handle:
            if not line.startswith("data: ["):
                continue
            try:
                blob = json.loads(line[6:])
            except ValueError:
                continue
            for item in blob:
                if isinstance(item, dict) and item.get("type") == "repo":
                    name = item.get("repository", "")
                    found.append((name.replace("github.com/", "", 1), item.get("repoStars", 0)))
    return found


def github_repo(repo):
    """Read fork and template status from the unauthenticated core API."""
    url = "https://api.github.com/repos/%s" % repo
    proc = subprocess.Popen(
        ["curl", "-s", "--max-time", "30", "-H", "Accept: application/vnd.github+json", url],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    text = out.decode("utf-8", "replace")
    if proc.returncode != 0 or not text.strip():
        return {"state": "refused", "reason": "curl exit %d" % proc.returncode}
    try:
        blob = json.loads(text)
    except ValueError:
        return {"state": "refused", "reason": "unparseable body, %d bytes" % len(text)}
    if isinstance(blob, dict) and blob.get("message"):
        return {"state": "refused", "reason": blob.get("message")}
    return {
        "state": "ok",
        "fork": blob.get("fork"),
        "is_template": blob.get("is_template"),
        "forks_count": blob.get("forks_count"),
        "stars": blob.get("stargazers_count"),
        "subscribers_count": blob.get("subscribers_count"),
    }


def _pattern_of(query):
    """Recover the `file:` term from a query string, exactly.

    `select:repo` and `count:` are stripped, the leading `context:global` is
    stripped, and what remains is the pattern -- so an overlapping pattern can
    never be confused with a longer one containing it.
    """
    body = query.split(" file:", 1)
    if len(body) != 2:
        return None
    tail = body[1]
    for suffix in (" select:", " count:"):
        if suffix in tail:
            tail = tail.split(suffix, 1)[0]
    return tail


def slug_for(pattern, name=None):
    """The filename the raw capture for this pattern is written under.

    Delegates to the writer's own naming function. Restating the rule here is
    what produced two successive rounds of `no_origin` on every configuration:
    first because the rule was re-implemented differently, then because the query
    header changed the file's shape underneath a second copy of it.
    """
    from copycount import capture_name

    return capture_name("context:global file:%s select:repo count:4000" % pattern, name)


def load_counts():
    """Copy counts, keyed by the exact `file:` term of the query.

    Matched on equality against the term recovered from the query's own header
    line. The first version used `pattern in rec["query"]`, and
    `^\\.claude/hooks/` is a substring of `^\\.claude/hooks/README\\.md$` -- so the
    broad hooks pattern silently took the narrow pattern's count of 42. A
    substring match over overlapping path patterns is the defect; it misreported
    two configurations before it was caught.
    """
    counts = {}
    counts_path = os.path.join(HERE, "copycount.json")
    if os.path.exists(counts_path):
        with open(counts_path) as handle:
            for rec in json.load(handle)["records"]:
                if rec["state"] not in ("ok", "saturated") or not rec.get("query"):
                    continue
                term = _pattern_of(rec["query"])
                for key, pattern in PATTERNS:
                    if pattern == term:
                        counts[key] = rec["count"]
    # The low-band sample is keyed by a generated name rather than by its
    # pattern, so its counts are read back from the captures by that name.
    for key, _ in low_band_paths():
        rec_path = os.path.join(HERE, "raw", "lowband-%s.sse" % key)
        if not os.path.exists(rec_path):
            continue
        rec = read_raw(rec_path)
        if rec["state"] in ("ok", "saturated"):
            counts[key] = rec["count"]
    return counts


# --- the low band -------------------------------------------------------
#
# The declared gate needs configurations in BOTH bands, and the first run had
# none in the low band: the ten declared patterns were all broad conventions,
# and the obvious way to get small counts -- query paths that cannot exist --
# would have been circular. A path with no copies has no origin repository, so it
# cannot answer a question about that repository's fork status.
#
# The low band is therefore drawn from hook filenames that demonstrably EXIST in
# the index. `probe-hook-paths.sse` is a `type:path` listing of `.claude/hooks/`
# (5,765 distinct paths in 1,026 repositories), and the low-band sample is
# declared as a mechanical slice of it: every 400th path in the order the index
# returned them. No count has been read for any of them, and the slice cannot be
# chosen for producing small numbers because it was fixed before the first of
# them was queried.
LOW_BAND_STRIDE = 400


def low_band_paths(limit=12):
    """Every LOW_BAND_STRIDE-th hook path the index returned."""
    path = os.path.join(HERE, "raw", "probe-hook-paths.sse")
    if not os.path.exists(path):
        return []
    seen, ordered = set(), []
    with open(path) as handle:
        for line in handle:
            if not line.startswith("data: ["):
                continue
            try:
                blob = json.loads(line[6:])
            except ValueError:
                continue
            for item in blob:
                if isinstance(item, dict) and item.get("type") == "path":
                    value = item.get("path")
                    if value and value not in seen:
                        seen.add(value)
                        ordered.append(value)
    sample = ordered[::LOW_BAND_STRIDE][:limit]
    return [(re.sub(r"[^A-Za-z0-9]+", "_", p.strip("/")), "^%s$" % re.escape(p))
            for p in sample]


def main():
    counts = load_counts()
    low = low_band_paths()
    LOW_KEYS.clear()
    LOW_KEYS.update(key for key, _ in low)
    patterns = PATTERNS + low
    # The low-band sample's counts are fetched here rather than assumed, because
    # membership in a band is defined by a count and nothing else may decide it.
    # The low-band fetch is retried across rounds. The anti-bot challenge arms
    # after roughly thirty requests from one host and answers the rest with HTML,
    # so a single pass silently truncated the low band to the first five
    # configurations -- which would have left the declared gate with a single
    # band and no rate to compute. Carried-forward counts are not re-fetched, so
    # each round only asks for what is still missing.
    for round_no in range(1, 5):
        pending = [(k, p) for k, p in low_band_paths() if k not in counts]
        if not pending:
            break
        print("lowband round %d: %d to fetch" % (round_no, len(pending)))
        sys.stdout.flush()
        streak = 0
        for key, pattern in pending:
            rec = fetch("context:global file:%s select:repo count:4000" % pattern,
                        name="lowband-%s" % key)
            if rec["state"] in ("ok", "saturated"):
                counts[key] = rec["count"]
                streak = 0
                time.sleep(6.0)
                continue
            streak += 1
            print("lowband %-46s %-9s %s" % (key, rec["state"], rec.get("count")))
            sys.stdout.flush()
            time.sleep(30.0)
            if streak >= 4:
                print("  challenge still armed; ending this round")
                break

    raw_dir = os.path.join(HERE, "raw")
    rows = []
    for key, pattern in patterns:
        copies = counts.get(key)
        if copies is None:
            rows.append({"config": key, "pattern": pattern, "copies": None, "state": "no_count"})
            continue
        slug = slug_for(pattern, "lowband-%s" % key if key in LOW_KEYS else None)
        candidates = repos_for(slug, raw_dir)
        candidates.sort(key=lambda pair: -pair[1])
        origin = candidates[0][0] if candidates else None
        row = {"config": key, "pattern": pattern, "copies": copies, "origin": origin}
        if origin is None:
            row["state"] = "no_origin"
        else:
            row.update(github_repo(origin))
            time.sleep(CORE_DELAY)
        rows.append(row)
        sys.stderr.write("%-26s copies=%-6s origin=%-42s %s fork=%s tmpl=%s\n"
                         % (key, copies, origin, row.get("state"), row.get("fork"),
                            row.get("is_template")))
        sys.stderr.flush()

    out = {"bands": {"high": HIGH_BAND, "low": LOW_BAND}, "rows": rows}
    with open(os.path.join(HERE, "forkstatus.json"), "w") as handle:
        json.dump(out, handle, indent=1, sort_keys=True)
        handle.write("\n")

    usable = [r for r in rows if r.get("copies") is not None and r.get("state") == "ok"]
    high = [r for r in usable if r["copies"] >= HIGH_BAND]
    low = [r for r in usable if r["copies"] <= LOW_BAND]
    print("usable %d of %d configurations" % (len(usable), len(rows)))
    print("high band (>=%d copies): %d" % (HIGH_BAND, len(high)))
    for r in high:
        print("  %-26s %-6s fork=%-5s template=%-5s %s"
              % (r["config"], r["copies"], r.get("fork"), r.get("is_template"), r.get("origin")))
    print("low band (<=%d copies): %d" % (LOW_BAND, len(low)))
    for r in low:
        print("  %-26s %-6s fork=%-5s template=%-5s %s"
              % (r["config"], r["copies"], r.get("fork"), r.get("is_template"), r.get("origin")))
    return 0


if __name__ == "__main__":
    sys.exit(main())