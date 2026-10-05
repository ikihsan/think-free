"""E020 population-rule falsification.

F037's observation was that a whole `.claude/` DIRECTORY is copied, but
population rule 2 tested only `.claude/settings.json`. If the population is full
of builders and the copiers live behind `agents/`, `commands/` or `skills/`,
then the population rule selected the wrong artifact and A5's zero is a fact
about the rule, not about copying.

This probes the wider `.claude/` surface so that is decidable rather than assumed.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from population import RAW, fetch  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "raw")

# A marker file per directory. Any 200 means the directory is populated.
PROBES = {
    "agents": ".claude/agents/README.md",
    "commands": ".claude/commands/README.md",
    "skills": ".claude/skills/README.md",
    "hooks": ".claude/hooks/README.md",
    "agents_alt": ".claude/agent/README.md",
    "settings": ".claude/settings.json",
}


def main():
    pop = json.load(open(os.path.join(RAW_DIR, "population.json")))
    repos = [r["repo"] for r in pop["rows"] if r["settings_state"] == "PRESENT"]

    out = {}
    for repo in repos:
        row = {}
        for label, path in PROBES.items():
            state, body = fetch(RAW.format(repo=repo, path=path))
            row[label] = state
            if state == "PRESENT" and body:
                with open(os.path.join(RAW_DIR, "probe--%s--%s" % (repo.replace("/", "__"), label)), "w") as f:
                    f.write(body)
            time.sleep(0.25)
        out[repo] = row
        sys.stderr.write("%-52s %s\n" % (repo, " ".join(
            "%s=%s" % (k, v[:1]) for k, v in sorted(row.items()))))

    with open(os.path.join(RAW_DIR, "surface.json"), "w") as f:
        json.dump({"probes": PROBES, "rows": out}, f, indent=1, sort_keys=True)

    counts = {}
    for repo, row in out.items():
        sig = tuple(sorted(k for k, v in row.items() if v == "PRESENT"))
        counts[sig] = counts.get(sig, 0) + 1
    print("\nsurface signatures (n=31):")
    for sig, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print("  %2d  %s" % (n, ", ".join(sig) or "(settings.json only)"))


if __name__ == "__main__":
    main()