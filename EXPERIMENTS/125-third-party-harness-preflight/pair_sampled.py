"""E125 step 6 -- M3 and M4 over the sampled population, not the path-matched
candidate list.

`probe.py` proposed pairs from files selected by *name*, and found none. The
coverage pass classified files by their *fields* across a deterministic sample of
857 data files, and found committed prediction artefacts (`model_output`,
`actual_output`) that the name filter never saw. This step runs the pairing and
the C1 measurement over the whole sample, so the zero and the pairs are measured
on the same population.

M4 is unchanged: a shared identifier-shaped field **name** and row counts within
an order of magnitude. Every qualified pair is handed to `preflight.concordance`
unmodified, at **zero adapter lines** -- `adapter_lines` is recorded per pair and
is 0 for all of them, which is what makes this the measurement of the zero-adapter
path rather than an assertion about it.

A "both"-sided file -- one record set carrying labels and outputs together -- is
recorded in `single_file_sides`. C1 has nothing to join there, and that fact is
itself a row in the result rather than a missing one.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from probe import blob, concordance, load_rows, m4_qualifies  # noqa: E402


def main():
    with open(os.path.join(HERE, "sample.json")) as fh:
        sample = json.load(fh)

    by_repo = {}
    for rec in sample["records"]:
        by_repo.setdefault(rec["full_name"], []).append(rec)

    qualified, refused, single = [], [], []
    for repo, recs in sorted(by_repo.items()):
        commit = None
        with open(os.path.join(HERE, "trees.json")) as fh:
            for r in json.load(fh)["repositories"]:
                if r["full_name"] == repo:
                    commit = r.get("commit")
        readable = [r for r in recs if r["readable"]]
        keys = [r for r in readable if r["side"] == "key-ish"]
        outs = [r for r in readable if r["side"] == "output-ish"]
        single.extend({"full_name": repo, "path": r["path"], "n": r["n"],
                       "key_fields": r["key_fields"], "output_fields": r["output_fields"]}
                      for r in readable if r["side"] == "both")
        for k in keys:
            for o in outs:
                ok, why = m4_qualifies(k, o)
                if not ok:
                    refused.append({"full_name": repo, "key": k["path"], "output": o["path"],
                                    "reason": why})
                    continue
                krows, _ = load_rows(blob(repo, commit, k["path"]), k["path"])
                orows, _ = load_rows(blob(repo, commit, o["path"]), o["path"])
                primary = concordance(krows, orows)
                swapped = concordance(orows, krows)
                qualified.append({
                    "full_name": repo,
                    "key": {"path": k["path"], "how": k["how"], "n": k["n"],
                            "id_fields": k["id_fields"], "key_fields": k["key_fields"]},
                    "output": {"path": o["path"], "how": o["how"], "n": o["n"],
                               "id_fields": o["id_fields"], "output_fields": o["output_fields"]},
                    "adapter_lines": 0, "m4": why,
                    "verdict": primary["verdict"], "best_rate": primary["best_rate"],
                    "reason": primary["reason"], "type_conflicts": primary["type_conflicts"],
                    "n_pairings": len(primary["pairings"]),
                    "swapped_verdict": swapped["verdict"],
                    "swapped_best_rate": swapped["best_rate"],
                })
                print("QUALIFIED %-30s %s (%d) | %s (%d) -> %s"
                      % (repo, k["path"][:44], k["n"], o["path"][:44], o["n"], primary["verdict"]))

    out = {"experiment": "E125",
           "population": "the 857-file deterministic sample in sample.json",
           "qualified_pairs": qualified,
           "refused_pairs": refused,
           "single_file_both_sides": single}
    with open(os.path.join(HERE, "pairs-sampled.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)

    print("\nqualified %d, refused %d, single-file both-sided %d"
          % (len(qualified), len(refused), len(single)))
    for r in refused:
        print("  refused %-28s %-40s | %-40s : %s"
              % (r["full_name"][:28], r["key"][:40], r["output"][:40], r["reason"][:50]))


if __name__ == "__main__":
    sys.exit(main())