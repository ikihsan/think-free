"""E020 A5 (run properly): structural attribution over authoritative trees.

A copied `.claude/` directory is detected by content that is byte-identical
across repositories. This needs no credit to be given, which matters because
configuration is anonymous by construction and README attribution returned 0 of
31 -- see the protocol's Amendment 1.

Three measures, kept apart because they answer different questions:
  share  -- fraction of a repo's .claude/ bytes that also appear in another repo
  files  -- how many distinct files are shared at all
  bundle -- how many repos share their MAJORITY of .claude/ with one other repo,
            which is the signature of a wholesale copy rather than a shared file
"""

import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(HERE, "raw")


def main():
    trees = json.load(open(os.path.join(RAW_DIR, "trees.json")))["trees"]
    repos = sorted(trees)
    populated = [r for r in repos if trees[r]["state"] == "PRESENT" and trees[r]["n_files"] > 1]

    # hash -> set of repos
    by_hash = defaultdict(set)
    for r in repos:
        t = trees[r]
        if t["state"] != "PRESENT":
            continue
        for rel, meta in t["files"].items():
            by_hash[meta["sha256"]].add(r)

    shared = {h: s for h, s in by_hash.items() if len(s) > 1}
    shared_files = []
    for r in repos:
        t = trees[r]
        if t["state"] != "PRESENT":
            continue
        sh_bytes = sum(meta["bytes"] for rel, meta in t["files"].items()
                       if len(by_hash[meta["sha256"]]) > 1)
        tot = sum(meta["bytes"] for meta in t["files"].values())
        shared_files.append({
            "repo": r,
            "n_files": t["n_files"],
            "total_bytes": tot,
            "shared_bytes": sh_bytes,
            "shared_byte_share": round(sh_bytes / tot, 4) if tot else None,
            "shared_file_share": round(
                sum(1 for meta in t["files"].values() if len(by_hash[meta["sha256"]]) > 1)
                / t["n_files"], 4) if t["n_files"] else None,
        })

    # bundle: for each repo, the largest set of its files that are byte-identical
    # to files in ONE other repo.
    bundles = {}
    for r in populated:
        t = trees[r]
        mine = {meta["sha256"]: meta["bytes"] for meta in t["files"].values()}
        tot_b = sum(mine.values())
        best = {"repo": None, "bytes": 0, "share": 0.0}
        for other in repos:
            if other == r or trees[other]["state"] != "PRESENT":
                continue
            theirs = {m["sha256"] for m in trees[other]["files"].values()}
            shared_b = sum(b for h, b in mine.items() if h in theirs)
            if shared_b > best["bytes"]:
                best = {"repo": other, "bytes": shared_b,
                        "share": round(shared_b / tot_b, 4) if tot_b else 0.0}
        bundles[r] = best

    multi_repo_files = len(shared)
    total_distinct_files = len(by_hash)

    # the single most widely shared file, and who holds it
    widest = max(shared.items(), key=lambda kv: len(kv[1])) if shared else (None, set())

    out = {
        "method": "git clone --depth 1, sha256 per file under .claude/",
        "n_repos": len(repos),
        "n_populated": len(populated),
        "total_file_instances": sum(trees[r]["n_files"] for r in repos),
        "distinct_file_hashes": total_distinct_files,
        "hashes_shared_by_2plus_repos": multi_repo_files,
        "share_of_distinct_files_shared": round(multi_repo_files / total_distinct_files, 4)
            if total_distinct_files else None,
        "widest_shared_hash_repos": sorted(widest[1]),
        "widest_shared_hash_n_repos": len(widest[1]) if widest[1] else 0,
        "per_repo_shared_bytes": sorted(shared_files, key=lambda x: -(x["shared_byte_share"] or 0)),
        "bundles": bundles,
        "n_repos_with_bundle_share_ge_0_5": sum(1 for b in bundles.values() if b["share"] >= 0.5),
        "n_repos_with_bundle_share_ge_0_8": sum(1 for b in bundles.values() if b["share"] >= 0.8),
    }
    with open(os.path.join(HERE, "results_a5.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)

    print("repos %d (populated %d), file instances %d, distinct hashes %d"
          % (out["n_repos"], out["n_populated"], out["total_file_instances"],
             out["distinct_file_hashes"]))
    print("hashes shared by 2+ repos: %d (%.1f%% of distinct)"
          % (multi_repo_files, 100 * (out["share_of_distinct_files_shared"] or 0)))
    print("widest shared file held by %d repos: %s" % (out["widest_shared_hash_n_repos"],
                                                      out["widest_shared_hash_repos"][:6]))
    print("\ntop bundles (share of one repo's .claude/ matching ONE other repo):")
    for r, b in sorted(bundles.items(), key=lambda kv: -kv[1]["share"])[:10]:
        if b["repo"]:
            print("  %-46s %.0f%% <- %s" % (r[:46], 100 * b["share"], b["repo"]))
    print("\nrepos whose .claude/ is >=50%% one other repo: %d; >=80%%: %d"
          % (out["n_repos_with_bundle_share_ge_0_5"], out["n_repos_with_bundle_share_ge_0_8"]))


if __name__ == "__main__":
    main()