"""E020: validate the marker-file probe against GitHub's authoritative listing.

`.claude/agents/README.md` returning 404 does NOT prove `.claude/agents/` is
absent -- the directory may hold files without a README. A5's and the surface
result both rest on this probe, so it is falsified here against the one
instrument that is authoritative: the contents API. 017's `placebo.py` and F037's
`rootlisting._complete` both record that a probe reading a convenient marker is
not a directory listing.
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "raw")
API = "https://api.github.com/repos/{repo}/contents/.claude"
UA = "think-free-research"

# The repos whose marker probe said ABSENT for everything but settings.json,
# sampled in the population's own order (declared, not chosen after seeing).
CHECK = [
    "ursisterbtw/ccprompts",
    "alirezarezvani/claude-skills",
    "laboqaba935-jpg/super",
    "FragmentedPacket/test-claude-settings-repo",
    "Donchitos/Claude-Code-Game-Studios",
    "disler/pi-vs-claude-code",
    "pedrohcgs/claude-code-my-workflow",
    "shintaro-sprech/agent-orchestrator-template",
]


def api(repo):
    req = urllib.request.Request(API.format(repo=repo), headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return "PRESENT", json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return "ABSENT", []
        return "UNDECIDABLE", []
    except Exception:
        return "UNDECIDABLE", []


def main():
    surface = json.load(open(os.path.join(RAW_DIR, "surface.json")))["rows"]
    rows = {}
    disagree = 0
    for repo in CHECK:
        state, entries = api(repo)
        listing = sorted(e["name"] for e in entries) if state == "PRESENT" else []
        probe = {k for k, v in surface[repo].items() if v == "PRESENT"}
        # The probe claims `settings.json` present and everything else absent.
        claimed = {"settings"} if probe == {"settings"} else probe
        # What the authoritative listing says exists as a directory.
        actual_dirs = set()
        for e in entries if state == "PRESENT" else []:
            if e.get("type") == "dir":
                actual_dirs.add(e["name"])
        ok = (claimed & actual_dirs) == claimed
        if not ok:
            disagree += 1
        rows[repo] = {"api_state": state, "listing": listing,
                      "dirs": sorted(actual_dirs), "probe_claimed": sorted(claimed),
                      "probe_missed_a_dir": sorted(actual_dirs - claimed), "agrees": ok}
        sys.stderr.write("%-46s dirs=%-30s probe_missed=%s\n" % (
            repo, ",".join(sorted(actual_dirs)) or "-", rows[repo]["probe_missed_a_dir"]))
        time.sleep(1.0)

    out = {"checked": CHECK, "n_disagree": disagree, "rows": rows,
           "note": "probe claims a directory exists only if its marker file returned 200"}
    with open(os.path.join(RAW_DIR, "probe_validation.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print("\nchecked %d repos against the contents API: %d disagreements" % (len(CHECK), disagree))


if __name__ == "__main__":
    main()